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
docs/         Architecture notes and decision records.
```

## Status

Design phase. Nothing is built yet.

Design sources: the strategy document "AI-Powered Private Cloud Documentation Platform: Strategy and Architecture" and its "Technical Implementation Addendum". Both are kept outside this repository.

Open decisions:

- Local model: bake-off between Gemma 4 26B-A4B, Qwen3.6-35B-A3B and gpt-oss-20b on the real VM.
- CI system: reuse the existing one, or stand up a minimal one.
- Whether AskIO sends the whole guide to the model or only retrieved passages.
- Formats for the watch, listen and play modes.
