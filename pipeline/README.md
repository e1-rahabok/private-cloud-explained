# pipeline

Ingestion and AI conversion ("auto docs"). One component of the project, not the project itself.

Planned contents:

- `connectors/`: Confluence, email, transcripts, Office files.
- `convert/`: chunking, prompt templates per document type, validation.
- `staging/`: raw payloads. Git-ignored. Never committed.

Output: pull requests that add or change Markdown in `content/`.
