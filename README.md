# Private Cloud Explained

One private-cloud knowledge base, many ways to learn it: read, search, ask, watch, listen, play, quiz.

Private Cloud Explained is an internal website that explains a VMware private cloud to its audiences: the CIO, senior leadership, and VMware administrators. People learn differently, so the same knowledge is offered in several forms.

The point is the consumption of the output, not the automation of the input. Automated ingestion keeps the content current. The site is what people use.

Modelled on the multi-mode approach of [isvara.io](https://isvara.io).

## Ways to consume

| Mode | What the reader gets | Status |
| --- | --- | --- |
| Read | Structured pages: architecture, connectivity diagrams, security, SOPs, user guides, install and upgrade guides | Planned |
| Search | Full-text search across all content | Planned |
| Ask | AskIO-style chat that answers from this content and links to the source pages, using a local LLM | Planned |
| Watch | Video explainers | Planned. Format to be decided |
| Listen | Podcast-style audio | Planned. Format to be decided |
| Play | A game that teaches the concepts | Planned. Concept to be decided |
| Quiz | Short quizzes generated from the content | Planned |

All modes draw from one source of truth: the Markdown in `content/`. Each mode is a view of that content, not a separate copy.

## How it works

1. **Ingest.** Connectors collect emails, meeting transcripts, Confluence pages, and Word, Excel and PowerPoint files. See `pipeline/`.
2. **Tag.** Admins and rules assign domain, priority and access scope.
3. **Convert.** A local AI model turns raw material into normalized Markdown (C4 model, TOGAF) with front matter. A person approves each change through a pull request.
4. **Build.** Next.js compiles `content/` into the site. See `site/`.
5. **Serve the other modes.** Search index, chat assistant (`assistant/`), and media (`media/`).

## Constraints

- Runs inside the corporate network. No external SaaS, public cloud host, or external LLM API.
- Corporate SSO and Active Directory authentication.
- Read-only. No connection to vCenter or live infrastructure telemetry.
- The chat model runs locally on a CPU-only Linux VM in vSphere (16 vCPU and 128 GB RAM planned).

## Repository layout

```text
content/      Normalized Markdown. The source of truth, one folder per domain.
pipeline/     Ingestion and AI conversion ("auto docs").
site/         Next.js web portal.
assistant/    Chat: retrieval and local LLM serving.
media/        Video, audio, game and quiz assets.
docs/         Complete design documentation. Start at docs/README.md.
config/       Taxonomy, access-scope mapping, connector settings (no secrets).
```

## Status

Design phase. Nothing is built yet. The plan is documented in [docs/](docs/README.md).

Design sources: the strategy document (PDF in [docs/source/](docs/source/)) and the Technical Implementation Addendum, whose content is restructured across the docs.

## Documentation

- [Vision and audiences](docs/01-vision-and-audiences.md)
- [Requirements](docs/02-requirements.md)
- [Architecture](docs/03-architecture.md)
- [Content model](docs/04-content-model.md)
- [Ingestion and AI conversion](docs/05-ingestion-and-ai-conversion.md)
- [Site design](docs/06-site-design.md)
- [Learning modes](docs/07-learning-modes.md)
- [Assistant and local LLM](docs/08-assistant-and-llm.md)
- [Security and governance](docs/09-security-and-governance.md)
- [Deployment and CI/CD](docs/10-deployment-and-cicd.md)
- [Testing and quality](docs/11-testing-and-quality.md)
- [Design considerations](docs/12-design-considerations.md)
- [Roadmap](docs/13-roadmap.md)
- [Risks and open decisions](docs/14-risks-and-open-decisions.md)
- [Glossary](docs/glossary.md)

Open decisions:

- Local model: bake-off between Gemma 4 26B-A4B, Qwen3.6-35B-A3B and gpt-oss-20b on the real VM.
- CI system: reuse the existing one, or stand up a minimal one.
- Whether AskIO sends the whole guide to the model or only retrieved passages.
- Formats for the watch, listen and play modes.
