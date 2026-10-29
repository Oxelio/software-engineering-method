"""Build and verify the method distribution; never publish or mutate an account."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tarfile
import zipfile
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = "skills/instructions/references/"
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
# Explicitly authorized removal paths for the first migration from the legacy GPT.
APPROVED_DELETE_PATHS = frozenset({
    ".app.json",
    "skills/instructions/lookup/knowledge-index.json",
})


def require(condition, message):
    if not condition:
        raise ValueError(message)


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(name):
    path = PurePosixPath(name)
    require(bool(name) and "\\" not in name and not path.is_absolute()
            and ".." not in path.parts and ":" not in name,
            f"Unsafe package path: {name}")
    return path


def check_links(files):
    for name, data in files.items():
        if not name.endswith(".md"):
            continue
        # Only inline local file destinations are checked; external URLs and
        # fragment-only references are outside this filesystem check.
        for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", data.decode("utf-8")):
            target = target.split("#", 1)[0]
            if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            parts = list(PurePosixPath(name).parent.parts)
            for part in PurePosixPath(target).parts:
                if part == "..":
                    require(bool(parts), f"Link escapes package: {name}: {target}")
                    parts.pop()
                elif part != ".":
                    parts.append(part)
            resolved = "/".join(parts)
            require(resolved in files, f"Broken link: {name}: {target}")


def source_files(root=ROOT):
    source = root / "plugin"
    config = json.loads((source / "build.json").read_text(encoding="utf-8"))
    manifest = json.loads((source / "plugin.json").read_text(encoding="utf-8"))
    require(manifest.get("$schema") == SCHEMA, "Invalid portable manifest schema")
    require(re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", manifest.get("version", "")),
            "Use a stable major.minor.patch release version")
    require(manifest.get("repository") == config["repository"], "Repository mismatch")
    require(not any(key in manifest for key in ("apps", "mcpServers", "skills", "interface")),
            "Portable components must use the standard layout")
    extension = manifest["extensions"]["com.openai"]
    require(set(extension) == {"interface"}, "The method must not bind external apps")
    interface = extension["interface"]
    require(0 < len(interface["shortDescription"]) <= 30, "Subtitle exceeds 30 characters")
    require(interface["displayName"] == "Software Engineering Method", "Unexpected identity")
    require(isinstance(interface["defaultPrompt"], (str, list)), "Invalid defaultPrompt")
    require(interface["defaultPrompt"], "Empty defaultPrompt")
    if isinstance(interface["defaultPrompt"], list):
        require(len(interface["defaultPrompt"]) <= 3 and all(
            isinstance(item, str) and item.strip() for item in interface["defaultPrompt"]),
            "Invalid starter prompts")
    require(interface["category"] == "Developer Tools", "Unexpected category")

    files = {"plugin.json": json_bytes(manifest)}
    for directory in ("skills", "assets"):
        for path in sorted((source / directory).rglob("*")):
            require(not path.is_symlink(), f"Symlink in source: {path}")
            if path.is_file():
                name = path.relative_to(source).as_posix()
                require(not name.startswith(REFERENCE_ROOT), "Do not commit generated references")
                files[name] = path.read_bytes()
    skills = [name for name in files if name.endswith("/SKILL.md")]
    require(skills == ["skills/instructions/SKILL.md"], "Expected the instructions skill")
    require(len(files[skills[0]]) <= 1024 * 1024, "Skill exceeds 1 MiB")
    skill = files[skills[0]].decode("utf-8").replace("\r\n", "\n")
    require(skill.startswith("---\n"), "Skill must start with YAML frontmatter")
    sections = skill.split("---", 2)
    require(len(sections) == 3, "Skill needs closing frontmatter")
    header = yaml.safe_load(sections[1])
    require(isinstance(header, dict) and header.get("name") == "instructions"
            and isinstance(header.get("description"), str) and header["description"].strip(),
            "Invalid skill frontmatter")
    agent = yaml.safe_load(files["skills/instructions/agents/openai.yaml"].decode("utf-8"))
    require(isinstance(agent, dict) and isinstance(agent.get("interface"), dict),
            "Invalid agent metadata")
    for key in ("display_name", "short_description", "default_prompt"):
        require(isinstance(agent["interface"].get(key), str) and agent["interface"][key].strip(),
                f"Missing agent metadata: {key}")
    for field in ("logo", "composerIcon"):
        name = str(safe_path(interface[field].removeprefix("./")))
        require(name in files, f"Missing asset: {name}")

    methods = config["method_files"]
    require(isinstance(methods, list) and methods and len(methods) == len(set(methods)),
            "Method inventory must be nonempty and unique")
    for name in methods:
        require(str(safe_path(name)) == name and "/" not in name and name.endswith(".md"),
                "Method sources must be root Markdown files")
        require(not (root / name).is_symlink(), f"Symlink in method: {name}")
        files[REFERENCE_ROOT + name] = (root / name).read_bytes()
    require("README.md" in methods and "core-model.md" in methods, "Missing method entry points")
    excluded = config.get("non_method_root_files", [])
    require(isinstance(excluded, list) and len(excluded) == len(set(excluded)),
            "Non-method document inventory must be unique")
    for name in excluded:
        require(isinstance(name, str) and str(safe_path(name)) == name
                and "/" not in name and name.endswith(".md"),
                f"Invalid non-method document: {name}")
    require(not set(methods) & set(excluded), "Document cannot be method and non-method")
    root_markdown = {path.name for path in root.glob("*.md") if path.is_file()}
    require(root_markdown == set(methods) | set(excluded),
            f"Unclassified root Markdown: {sorted(root_markdown - set(methods) - set(excluded))}; "
            f"missing root Markdown: {sorted((set(methods) | set(excluded)) - root_markdown)}")
    # Generate the compatibility overlay from the same manifest; never edit two
    # independent copies of version, identity, presentation, or app declarations.
    compatibility = {key: manifest[key] for key in
                     ("name", "version", "description", "author", "repository")}
    compatibility.update(interface=interface, skills="./skills", keywords=manifest.get("keywords", []))
    files[".codex-plugin/plugin.json"] = json_bytes(compatibility)
    check_links(files)
    return config, manifest, files


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def build(root=ROOT, output=None, allow_dirty=False, release=False):
    config, manifest, files = source_files(root)
    commit = git(root, "rev-parse", "HEAD")
    dirty = bool(git(root, "status", "--porcelain", "--untracked-files=normal"))
    require(allow_dirty or not dirty, "Builds require a clean checkout; use --allow-dirty for preview")
    release_tag = None
    if release:
        require(not allow_dirty and not dirty, "Release builds cannot be dirty previews")
        release_tag = f"v{manifest['version']}"
        try:
            tagged_commit = git(root, "rev-parse", "--verify", f"refs/tags/{release_tag}^{{commit}}")
        except subprocess.CalledProcessError as error:
            raise ValueError(f"Release builds require the local {release_tag} tag") from error
        require(tagged_commit == commit, f"Release tag {release_tag} must point to HEAD")
        remote_main = "refs/remotes/origin/main"
        available = subprocess.run(
            ["git", "-C", str(root), "show-ref", "--verify", "--quiet", remote_main],
            capture_output=True, text=True, check=False,
        )
        require(available.returncode == 0, "Release builds require a fetched origin/main ref")
        ancestor = subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", commit, remote_main],
            capture_output=True, text=True, check=False,
        )
        require(ancestor.returncode == 0, "Release commit must be reachable from origin/main")
    provenance = {
        "schema_version": 1, "plugin_id": config["plugin_id"],
        "repository": config["repository"], "source_commit": commit,
        "dirty": dirty, "version": manifest["version"],
        "build_kind": "release" if release else "review", "release_tag": release_tag,
        "method_sources": {REFERENCE_ROOT + name: name for name in config["method_files"]},
        "files": {name: sha256(data) for name, data in sorted(files.items())},
    }
    files["provenance.json"] = json_bytes(provenance)
    output = Path(output) if output else root / "dist"
    # Outputs must not change any source input (including tracked dist files).
    output = output.resolve()
    require(output != root.resolve() and not output.is_relative_to((root / "plugin").resolve()),
            "Build output must be outside source directories")
    output.mkdir(parents=True, exist_ok=True)
    suffix = "-preview" if dirty else ("" if release else "-review")
    archive = output / f"software-engineering-method-{manifest['version']}{suffix}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as target:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            target.writestr(info, data)
    receipt = {
        "plugin_id": config["plugin_id"], "version": manifest["version"],
        "source_commit": commit, "dirty": dirty,
        "build_kind": "release" if release else "review", "release_tag": release_tag,
        "archive": archive.name, "archive_sha256": sha256(archive.read_bytes()),
    }
    archive.with_suffix(".json").write_bytes(json_bytes(receipt))
    return archive, receipt


def archive_files(path):
    result = {}
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for item in archive.infolist():
                if item.is_dir():
                    continue
                require((item.external_attr >> 16) & 0o170000 != 0o120000, "Archive contains symlink")
                require(item.filename not in result, "Duplicate archive member")
                result[item.filename] = archive.read(item)
    else:
        with tarfile.open(path, "r:gz") as archive:
            for item in archive.getmembers():
                if item.isdir():
                    continue
                require(item.isfile(), "Archive contains non-file member")
                name = item.name.removeprefix("./")
                require(name not in result, "Duplicate archive member")
                result[name] = archive.extractfile(item).read()
    for name in result:
        safe_path(name)
    if "plugin.json" not in result:
        prefixes = {name.split("/", 1)[0] for name in result}
        require(len(prefixes) == 1, "Archive must contain one plugin")
        prefix = next(iter(prefixes)) + "/"
        result = {name.removeprefix(prefix): data for name, data in result.items()}
    require("plugin.json" in result, "Archive has no root plugin manifest")
    return result


def verify(expected_path, published_path):
    expected, published = archive_files(expected_path), archive_files(published_path)
    checked_provenance(expected)
    missing, extra = set(expected) - set(published), set(published) - set(expected)
    require(not missing and not extra,
            f"Inventory mismatch: missing={sorted(missing)}, extra={sorted(extra)}")
    # A published plugin must no longer declare obsolete app bindings.
    require("apps" not in json.loads(published["plugin.json"]).get("extensions", {}).get("com.openai", {}),
            "Published plugin still declares an app binding")
    require("apps" not in json.loads(published[".codex-plugin/plugin.json"]),
            "Published compatibility manifest still declares an app binding")
    for name in expected:
        # Hosts may serialize manifests differently. Method text, assets, and
        # provenance must remain byte-identical.
        if name in ("plugin.json", ".codex-plugin/plugin.json"):
            equal = json.loads(expected[name]) == json.loads(published[name])
        else:
            equal = expected[name] == published[name]
        require(equal, f"Published content differs: {name}")


def checked_provenance(files):
    provenance = json.loads(files["provenance.json"])
    require(provenance.get("schema_version") == 1, "Unsupported provenance schema")
    require(re.fullmatch(r"[a-f0-9]{40}", provenance.get("source_commit", "")),
            "Invalid source commit")
    require(set(provenance["files"]) == set(files) - {"provenance.json"},
            "Provenance inventory differs")
    for name, digest in provenance["files"].items():
        require(sha256(files[name]) == digest, f"Provenance checksum differs: {name}")
    manifest = json.loads(files["plugin.json"])
    require(provenance["version"] == manifest["version"], "Provenance version differs")
    kind = provenance.get("build_kind")
    require(kind in ("review", "release"), "Unknown build kind")
    require(provenance.get("release_tag") == (
        f"v{manifest['version']}" if kind == "release" else None
    ), "Release tag does not match build kind and version")
    return provenance


def publication_plan(archive_path, snapshot):
    files = archive_files(archive_path)
    provenance = checked_provenance(files)
    require(provenance["dirty"] is False, "Preview builds cannot be published")
    require(provenance["build_kind"] == "release",
            "Only tagged release builds can be published; review builds are not publishable")
    require("next_offset" in snapshot and snapshot["next_offset"] is None,
            "Use a complete current plugin inventory")
    plugin = snapshot["plugin"]
    require(plugin["plugin_id"] == provenance["plugin_id"], "Wrong target plugin")
    require(plugin.get("current_release_id"), "Missing current release guard")
    old_version = re.match(r"^(\d+)\.(\d+)\.(\d+)", plugin.get("version", ""))
    require(old_version, "Current plugin version must be resolved")
    new_version = tuple(map(int, provenance["version"].split(".")))
    require(new_version > tuple(map(int, old_version.groups())), "Bump release version before publishing")
    previous = [item["path"] for item in snapshot["files"]]
    require(len(previous) == len(set(previous)), "Duplicate current inventory entries")
    for name in previous:
        safe_path(name)
    delete_paths = sorted(set(previous) - set(files))
    unapproved = set(delete_paths) - APPROVED_DELETE_PATHS
    require(not unapproved, f"Unapproved deletion paths: {sorted(unapproved)}")
    return {
        "plugin_id": provenance["plugin_id"],
        "expected_release_id": plugin["current_release_id"],
        "archive": str(Path(archive_path).resolve()),
        "archive_sha256": sha256(Path(archive_path).read_bytes()),
        "source_commit": provenance["source_commit"],
        "version": provenance["version"],
        "delete_paths": delete_paths,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check")
    package = sub.add_parser("build")
    package.add_argument("--output", type=Path)
    package.add_argument("--allow-dirty", action="store_true")
    package.add_argument("--release", action="store_true",
                         help="Build publishable content only from the matching local version tag")
    compare = sub.add_parser("verify")
    compare.add_argument("expected", type=Path)
    compare.add_argument("published", type=Path)
    plan = sub.add_parser("plan")
    plan.add_argument("archive", type=Path)
    plan.add_argument("snapshot", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "check":
            _, _, files = source_files()
            print(f"Validated {len(files)} package files and their local Markdown links")
        elif args.command == "build":
            _, receipt = build(output=args.output, allow_dirty=args.allow_dirty, release=args.release)
            print(json.dumps(receipt, indent=2))
        elif args.command == "verify":
            verify(args.expected, args.published)
            print("Published inventory and contents match the expected package")
        else:
            snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
            print(json.dumps(publication_plan(args.archive, snapshot), indent=2))
    except (ValueError, KeyError, OSError, yaml.YAMLError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
