# content

Normalized Markdown. This is the source of truth for every way of consuming the knowledge.

One folder per domain:

- `infrastructure-architecture/`
- `connectivity-diagrams/`
- `security/`
- `sops/`
- `user-guides/`
- `install-upgrade/`
- `team-structure/` (Proposed)
- `runbooks/` (Proposed)
- `operations/` (Proposed)
- `decisions/` (Proposed)

Rules:

- Every file has YAML front matter. See `docs/04-content-model.md`.
- Files are created or changed through pull requests from the pipeline or by a person.
- Raw source material (emails, transcripts, exports) is never committed here.
