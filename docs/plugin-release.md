# Plugin source, synchronization, and release

## Ownership and design

The canonical method and its plugin source have one active repository:
`Oxelio/software-engineering-method`. Method documents retain their root paths
to preserve existing adoption links. Moving them to `method/` would add link
migration without improving ownership, so this change keeps the current layout.

The plugin is a distribution, not another method owner. Its skill routes an
activity to packaged normative references and project-owned bindings. It does
not repeat a complete lifecycle, role catalog, or readiness policy. Project
owners may reside in Git or explicitly designated external operational systems.

`plugin/build.json` maps the complete method file inventory into the package.
The builder copies these files byte-for-byte to
`skills/instructions/references/`, generates `.codex-plugin/plugin.json` from
the portable manifest, and records the source commit and file hashes in
`provenance.json`. Generated files are never independent editable inputs.

ZIP entries use a fixed order, timestamp, file mode, and uncompressed content.
For the same clean commit and declared dependencies, repeated builds produce
the same bytes. The adjacent JSON receipt records the archive SHA-256. Its
checksum covers the entire package, including provenance.

The portable manifest retains the installed plugin's package name, display
name, icon, and starter prompts. Its account identity remains
`plugin_09c6c2b682e8819196aed461ea8279d8`; publication must update that identity.
Do not create a replacement plugin or change its scope or audience.

## Initial migration from 0.11.2+github.1

The initial target is `0.12.0`. The source baseline inspected for this migration
was release `pluginrel_6abd1894161081919868c571ed7c5629`.

This baseline is evidence, not a reusable release guard. Always re-read the
current plugin before publishing.

The migration:

- embeds the current canonical method, including Workflow Coordinator,
  operational ownership, permission boundaries, and current review semantics;
- replaces duplicated runtime rules with focused reference resolution;
- corrects the subtitle and removes project-branded examples;
- removes references to the optional GitHub app and provider-specific runtime
  instructions; integrations are selected by each adopting project;
- stops using the obsolete GPT upload-name lookup index;
- preserves the existing icon, identity, and starter prompt values.

The Plugin Creator update API overlays uploaded files and supports explicit
`delete_paths` for files omitted from the archive. This migration **must
delete** `.app.json` and `skills/instructions/lookup/knowledge-index.json`.
The replacement manifests remove the GitHub app binding, and the new skill
does not load the old GPT index.

The publication plan compares the fresh, complete account inventory with the
release archive and rejects any deletion not explicitly approved in
`scripts/package_plugin.py`. The two known historical files are the only
approved initial removals. Do not upload and delete the same path. Subsequent
releases should have an empty deletion list unless another removal is reviewed.

The old `software-engineering-method-gpt` repository stays archived. Its
OpenAPI action contract belongs to the historical Custom GPT and is not a new
MCP server or plugin dependency.

## Build and review

1. Update method or runtime sources through a pull request. Bump
   `plugin/plugin.json` to a higher stable `major.minor.patch` version whenever
   releasing changed content. A build metadata suffix is not a release bump.
2. Run `check`, the unit tests, and a review build. Review the method changes
   separately from packaging and operational changes. PR and manually dispatched
   CI builds produce `-review.zip` and are **never publishable**, even when clean.
   Dirty local previews produce `-preview.zip` and are likewise non-publishable.
3. After the source is reviewed and merged, check out the exact merged commit
   with a clean worktree and create tag `v<plugin-version>` under the repository's
   normal authorization. CI checks the tag/version correspondence and runs
   `build --release` only for tag events. This requires that the local version
   tag points to HEAD **and the commit is reachable from the fetched
   `origin/main`**. The tagged workflow fetches the full history and checks
   this ancestry before packaging; `build --release` independently enforces
   the same condition. A tag on an unmerged branch cannot produce a publishable
   archive. CI builds the package without publishing it.
4. Keep the exact ZIP and JSON checksum receipt, preferably as assets of a
   GitHub release associated with that tag. Verify that the receipt's
   `source_commit` is the intended reviewed revision and `dirty` is false.

Method adoption may pin a Git commit or release tag. The installed plugin keeps
applying its bundled revision until explicitly updated; it must not silently
mix its rules with a newer online branch.

## Prepare the account update

Use the existing Plugin Creator integration in an authorized chat:

1. Call `get_plugin_files` for the exact plugin ID, follow every `next_offset`,
   and inspect current metadata and relevant text. If the source changed from
   the reviewed baseline, reconcile it before continuing.
2. Save the normalized result as `dist/current-plugin.json`: an object with
   `plugin`, the complete combined `files` array, and `next_offset: null`.
   Do not save a paginated or truncated inventory as complete. Download the
   current archive when binary preservation or a backup requires it.
3. Generate a concrete update plan:

   ```sh
   python scripts/package_plugin.py plan dist/software-engineering-method-0.12.0.zip dist/current-plugin.json
   ```

4. Review its identity, source commit, checksum, version,
   `expected_release_id`, and explicit `delete_paths`. The initial migration
   must list exactly `.app.json` and
   `skills/instructions/lookup/knowledge-index.json`. If other files appear,
   reconcile them before publication rather than silently deleting them.
5. Call `update_plugin` with the reviewed archive, exact plugin ID, fresh
   `expected_release_id`, and the exact `delete_paths` returned by the plan.
   Ensure deleted paths are absent from the uploaded archive. Keep sharing unchanged.
   If the release guard conflicts, fetch and reconcile current source; do not
   replace the guard on an outdated candidate and retry blindly.

This is a manual publication procedure. CI creates reviewable artifacts and
does not store account credentials or automate Plugin Creator updates.

## Verify and record

After a successful update:

1. Read metadata and the complete file inventory again. Confirm the returned
   release ID, intended version, skill, unchanged identity and audience, and
   **absence of both deleted historical files**. Confirm neither the portable
   nor the compatibility manifest declares the removed app binding.
2. Retrieve that published release using `get_owned_plugin_archive` and save
   it outside source inputs, for example `dist/published.tar.gz`.
3. Compare the actual publication against the exact reviewed build:

   ```sh
   python scripts/package_plugin.py verify dist/software-engineering-method-0.12.0.zip dist/published.tar.gz
   ```

   Verification rejects all missing, changed, or additional files, including
   formerly retained historical files. Method text, assets, and provenance
   must be byte-identical; manifest JSON may be serialized differently only
   when its parsed content remains identical. Reconfirm that neither manifest
   declares an app binding.
4. Record plugin ID, published release ID, version, source commit, tag, archive
   checksum, verification result, and any host smoke-test limits in the GitHub
   release notes or a reviewed release receipt. That receipt refers back to the
   built source commit; it is a later record, not part of its own build inputs.
5. Exercise representative classification, context, and readiness requests in
   the host. Distinguish verified package contents from observed runtime behavior.

If publication fails, the reviewed Git source and build remain available and
the old installed release remains the last confirmed deployment. If read-back
fails, report the saved release separately from unverified synchronization.

## Recovery and exceptional edits

Keep the preceding release archive before updating. Recover by preparing its
content as a new, higher-version reviewed release; do not assume the backend
accepts a semantic version downgrade. Reference the originating and replacement
commits in the release record.

An urgent direct plugin edit must subsequently be reconciled into its proper
Git owner before the next normal release. Do not let a runtime edit become a
second normative method. No automated bidirectional synchronization is used.
