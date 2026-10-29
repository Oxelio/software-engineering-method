import importlib.util
import json
import shutil
import subprocess
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "package_plugin", Path(__file__).resolve().parents[1] / "scripts/package_plugin.py")
package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repository"
        self.root.mkdir()
        config = json.loads((package.ROOT / "plugin/build.json").read_text(encoding="utf-8"))
        for name in [*config["method_files"], ".gitignore", ".gitattributes"]:
            shutil.copyfile(package.ROOT / name, self.root / name)
        shutil.copytree(package.ROOT / "plugin", self.root / "plugin")
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Package Test", "-c", "user.email=test@example.invalid",
                 "commit", "-qm", "fixture")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True).strip()

    def change_manifest(self, change):
        path = self.root / "plugin/plugin.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        change(value)
        path.write_bytes(package.json_bytes(value))

    def snapshot(self):
        return {"next_offset": None, "plugin": {
            "plugin_id": "plugin_09c6c2b682e8819196aed461ea8279d8",
            "version": "0.11.2+github.1", "current_release_id": "previous-release"},
            "files": [{"path": name} for name in ["plugin.json", ".app.json",
                      "skills/instructions/lookup/knowledge-index.json"]]}

    def test_reproducible_archive_preserves_method_and_provenance(self):
        first, receipt = package.build(self.root)
        original = first.read_bytes()
        second, repeated = package.build(self.root)
        self.assertEqual(original, second.read_bytes())
        self.assertEqual(receipt, repeated)
        files = package.archive_files(first)
        provenance = json.loads(files["provenance.json"])
        self.assertFalse(provenance["dirty"])
        self.assertEqual("review", provenance["build_kind"])
        self.assertIsNone(provenance["release_tag"])
        self.assertTrue(first.name.endswith("-review.zip"))
        with self.assertRaisesRegex(ValueError, "Only tagged release"):
            package.publication_plan(first, self.snapshot())
        self.assertEqual(self.git("rev-parse", "HEAD"), provenance["source_commit"])
        for target, source in provenance["method_sources"].items():
            self.assertEqual((self.root / source).read_bytes(), files[target])
        for name, digest in provenance["files"].items():
            self.assertEqual(package.sha256(files[name]), digest)
        manifest = json.loads(files["plugin.json"])
        compatibility = json.loads(files[".codex-plugin/plugin.json"])
        self.assertEqual(manifest["version"], compatibility["version"])
        self.assertEqual(manifest["extensions"]["com.openai"]["interface"], compatibility["interface"])
        self.assertNotIn(".app.json", files)
        self.assertNotIn("apps", compatibility)

    def test_dirty_source_requires_explicit_preview_and_cannot_publish(self):
        (self.root / "core-model.md").write_text("changed\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "clean checkout"):
            package.build(self.root)
        archive, receipt = package.build(self.root, allow_dirty=True)
        self.assertTrue(receipt["dirty"])
        self.assertIn("preview", archive.name)
        with self.assertRaisesRegex(ValueError, "Preview"):
            package.publication_plan(archive, self.snapshot())

    def test_undeclared_provider_binding_is_rejected(self):
        self.change_manifest(lambda value: value["extensions"]["com.openai"].update(apps="./.app.json"))
        with self.assertRaisesRegex(ValueError, "external apps"):
            package.source_files(self.root)

    def test_invalid_frontmatter_and_long_subtitle_are_rejected(self):
        skill = self.root / "plugin/skills/instructions/SKILL.md"
        original = skill.read_bytes()
        skill.write_text("---\nname: [broken\n---\n", encoding="utf-8")
        with self.assertRaises(package.yaml.YAMLError):
            package.source_files(self.root)
        skill.write_bytes(original)
        self.change_manifest(lambda value: value["extensions"]["com.openai"]["interface"].update(
            shortDescription="x" * 31))
        with self.assertRaisesRegex(ValueError, "30 characters"):
            package.source_files(self.root)

    def test_unclassified_root_markdown_is_rejected(self):
        (self.root / "new-normative-document.md").write_text("# New method rule\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Unclassified root Markdown"):
            package.source_files(self.root)

    def test_broken_method_link_and_committed_reference_copy_are_rejected(self):
        method = self.root / "README.md"
        original = method.read_bytes()
        method.write_bytes(original + b"\n[Missing](missing.md)\n")
        with self.assertRaisesRegex(ValueError, "Broken link"):
            package.source_files(self.root)
        method.write_bytes(original)
        copied = self.root / "plugin/skills/instructions/references/core-model.md"
        copied.parent.mkdir()
        copied.write_text("second editable copy", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "generated references"):
            package.source_files(self.root)

    def test_plan_requires_full_inventory_identity_release_and_new_version(self):
        self.git("tag", "v0.12.0")
        archive, _ = package.build(self.root, release=True)
        plan = package.publication_plan(archive, self.snapshot())
        self.assertEqual([".app.json", "skills/instructions/lookup/knowledge-index.json"],
                         plan["retained_legacy_files"])
        self.assertEqual("previous-release", plan["expected_release_id"])
        for update, message in [
            (lambda value: value.update(next_offset=50), "complete"),
            (lambda value: value["plugin"].update(plugin_id="other-plugin"), "Wrong target"),
            (lambda value: value["plugin"].update(current_release_id=None), "release guard"),
            (lambda value: value["plugin"].update(version="0.12.0"), "Bump release"),
            (lambda value: value["files"].append({"path": "unknown-leftover.txt"}), "Unexpected existing"),
        ]:
            with self.subTest(message=message):
                snapshot = self.snapshot()
                update(snapshot)
                with self.assertRaisesRegex(ValueError, message):
                    package.publication_plan(archive, snapshot)

    def test_release_requires_tag_pointing_to_head(self):
        with self.assertRaisesRegex(ValueError, "local v0.12.0 tag"):
            package.build(self.root, release=True)
        self.git("tag", "v0.12.0")
        archive, receipt = package.build(self.root, release=True)
        self.assertEqual("release", receipt["build_kind"])
        self.assertEqual("v0.12.0", receipt["release_tag"])
        self.assertEqual("0.12.0", package.publication_plan(archive, self.snapshot())["version"])
        (self.root / "README.md").write_text("temporary preview\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "dirty previews"):
            package.build(self.root, release=True, allow_dirty=True)

    def test_verification_supports_wrapped_tar_and_manifest_reserialization(self):
        expected, _ = package.build(self.root)
        files = package.archive_files(expected)
        files["plugin.json"] = json.dumps(json.loads(files["plugin.json"]), sort_keys=True).encode()
        published = self.root / "dist/published.tar.gz"
        import io
        with tarfile.open(published, "w:gz") as archive:
            for name, data in files.items():
                member = tarfile.TarInfo("wrapper/" + name)
                member.size = len(data)
                archive.addfile(member, io.BytesIO(data))
        package.verify(expected, published)

    def test_verification_accepts_only_inert_legacy_overlay_files(self):
        expected, _ = package.build(self.root)
        original = package.archive_files(expected)
        retained = {**original,
                    ".app.json": b'{"apps":{"github":{"id":"old"}}}',
                    "skills/instructions/lookup/knowledge-index.json": b'{"files":[]}'}
        published = self.root / "dist/published.zip"
        with zipfile.ZipFile(published, "w") as archive:
            for path, data in retained.items():
                archive.writestr(path, data)
        package.verify(expected, published)
        for name, data in [
            ("skills/instructions/references/core-model.md", b"tampered"),
            ("unexpected-other-file.txt", b"unrecognized"),
        ]:
            with self.subTest(name=name):
                changed = {**retained, name: data}
                with zipfile.ZipFile(published, "w") as archive:
                    for path, content in changed.items():
                        archive.writestr(path, content)
                with self.assertRaisesRegex(ValueError, "differs|Inventory mismatch"):
                    package.verify(expected, published)

    def test_publication_plan_rejects_an_archive_changed_after_build(self):
        self.git("tag", "v0.12.0")
        expected, _ = package.build(self.root, release=True)
        files = package.archive_files(expected)
        files["skills/instructions/references/core-model.md"] += b"tampered\n"
        changed = self.root / "dist/changed.zip"
        with zipfile.ZipFile(changed, "w") as archive:
            for name, data in files.items():
                archive.writestr(name, data)
        with self.assertRaisesRegex(ValueError, "Provenance checksum differs"):
            package.publication_plan(changed, self.snapshot())

    def test_unsafe_or_duplicate_archive_members_are_rejected(self):
        for names in (("plugin.json", "../outside"), ("plugin.json", "plugin.json")):
            with self.subTest(names=names):
                archive = self.root / "dist/unsafe.zip"
                archive.parent.mkdir(exist_ok=True)
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    with zipfile.ZipFile(archive, "w") as target:
                        for name in names:
                            target.writestr(name, b"{}")
                with self.assertRaisesRegex(ValueError, "Unsafe|Duplicate"):
                    package.archive_files(archive)


if __name__ == "__main__":
    unittest.main()
