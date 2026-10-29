# Maintaining Software Engineering Method

The method and plugin sources are maintained in this repository. Make changes
through a reviewed pull request. The archived Custom GPT repository remains
historical evidence; do not update it as a second active source.

## Source layout

- Root method documents remain canonical at their existing paths, preserving
  adoption links. The complete packaged inventory is in `plugin/build.json`.
  The build also rejects any new root Markdown file until it is explicitly
  classified as normative or non-method documentation.
- `plugin/plugin.json` owns package identity, version, and presentation.
- `plugin/skills/instructions/` owns the runtime entry point and agent metadata.
- `plugin/assets/` contains the existing icon, preserved from the current plugin.
- `scripts/package_plugin.py` generates references, the compatibility manifest,
  provenance, and a deterministic ZIP under ignored `dist/`.
- `docs/plugin-release.md` owns this repository's release procedure.

Do not commit generated references, a second compatibility manifest, or package
archives. Add a method document to `plugin/build.json` when it belongs in the
distribution. Keep method semantics in the method documents and use the skill
to resolve the relevant references. Tooling choices for this repository do not
become requirements for adopting projects.

## Local checks

Use Python 3.12 and install the development dependency in a local environment:

```sh
python -m venv .venv
# Activate .venv using your shell's normal activation command.
python -m pip install -r requirements-dev.txt
python scripts/package_plugin.py check
python -m unittest discover -s tests -v
python scripts/package_plugin.py build --allow-dirty
```

The preview flag is for local work only. Regular clean builds create
non-publishable `-review.zip` archives; dirty previews use `-preview.zip`.
To build a publishable release, use a clean checkout at a reviewed source
commit with its matching `v<version>` tag:

```sh
python scripts/package_plugin.py build --release
```

CI runs validation and tests on Linux and Windows, requires identical package
bytes across both platforms, and saves the package and its SHA-256 receipt.
It does not publish to the plugin account or cross a release gate.
See [the release procedure](docs/plugin-release.md) for publication and read-back.
