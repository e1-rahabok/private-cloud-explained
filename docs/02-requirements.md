# 2. Requirements

Status labels: **Spec** = original strategy document. **Addendum** = technical implementation addendum. **Request** = project owner's later requests. **Proposed** = recommended here, not yet confirmed.

## Functional requirements

| ID | Requirement | Origin |
| --- | --- | --- |
| F1 | Ingest email threads, meeting transcripts and minutes, Confluence pages, and Word, Excel and PowerPoint files | Spec |
| F2 | Admin-defined taxonomy, tags and access scope per document | Spec |
| F3 | Convert sources to normalized Markdown using the C4 model and TOGAF | Spec |
| F4 | Intranet search, navigation sidebar, table of contents, document lineage | Spec |
| F5 | Ask: chat assistant that answers from portal content and links to source pages, modeled on AskIO at isvara.io | Request |
| F6 | Watch: video explainers tied to pages | Request |
| F7 | Listen: audio (podcast-style) tied to pages | Request |
| F8 | Play: a game that teaches private-cloud concepts | Request |
| F9 | Quiz: quizzes generated from content | Request |
| F10 | Executive views: dashboards that give leadership architecture views, security baselines and operational guides. Content-derived, not live telemetry | Spec (deliverables) |
| F11 | Every derived asset (video, audio, quiz, game scenario) records its source page and version. Assets are flagged when the page changes | Proposed |
| F12 | Each page shows which modes exist for it and links to them | Proposed |
| F13 | A review workflow: AI drafts arrive as pull requests with the source shown beside the draft | Addendum |

## Non-functional requirements

| ID | Requirement | Origin |
| --- | --- | --- |
| N1 | Everything runs inside the corporate network: no external SaaS, no public cloud host, no external LLM API | Spec, extended to the LLM |
| N2 | Corporate SSO and Active Directory authentication | Spec |
| N3 | Sub-second page loads through static generation (SSG) or incremental static regeneration (ISR) | Spec |
| N4 | Ingestion, AI transformation and frontend stay decoupled | Spec |
| N5 | Ask shows its first words within 20 seconds and serves 2 to 3 simultaneous users | Proposed |
| N6 | WCAG 2.2 AA. Captions and transcripts for every video and audio asset | Proposed |
| N7 | Auditability: all content in Git with history and blame, plus automated checks against corporate IT policy | Spec |
| N8 | Automation: a rebuild when new content merges, by webhook, plus a nightly safety rebuild | Spec, Addendum |
| N9 | Observability: pipeline and site health visible to administrators | Proposed |
| N10 | Data minimization: raw ingested material is never committed. Secrets are never in the repository | Proposed |

## Infrastructure requirements

| ID | Requirement | Origin |
| --- | --- | --- |
| I1 | The local LLM runs CPU-only in a Linux VM on vSphere: 16 vCPU, 128 GB RAM, on Intel Xeon or AMD EPYC hosts | Request |
| I2 | The local LLM replaces Gemini. No question or document text leaves the network | Request |
| I3 | CI/CD reuses the organization's existing system. If none exists, a minimal one is stood up | Addendum. Availability varies by organization |
| I4 | One private Git repository holds all Markdown, with version history | Spec |
| I5 | No connection to vCenter or live infrastructure telemetry | Spec |
| I6 | At least a development and a production environment | Proposed |
| I7 | Production can be rebuilt from Git plus configuration, without restoring the web VM from backup | Proposed |

## Security requirements

| ID | Requirement | Origin |
| --- | --- | --- |
| S1 | SSO authentication on every page and API route | Spec |
| S2 | `access_scope` is enforced in pages, navigation, search results and Ask | Proposed |
| S3 | The assistant treats retrieved text as untrusted data and has no tools | Proposed |
| S4 | Ingested material is scanned for credentials and sensitive data before AI processing and before commit | Proposed |
| S5 | Connector service accounts are read-only and least-privilege. Credentials sit in a secrets store | Addendum |

## Project requirement

| ID | Requirement | Origin |
| --- | --- | --- |
| T1 | The build doubles as a hands-on lab for VMware administrators using VS Code, Claude Code, Cursor and GitHub | Spec |

## Constraints

- No external SaaS hosting for production content (N1). This repository on GitHub holds code, documentation and synthetic sample content. Production content lives in an internal Git repository (decision D-027).
- The portal is read-only toward the infrastructure (I5).
- CPU-only inference on a 16 vCPU, 128 GB VM (I1).
- The audience is mixed: executives and engineers.

## Assumptions

- The corporate identity provider supports OIDC or SAML and exposes group membership.
- Source systems expose APIs or exports that a service account may read.
- A reviewer pool exists to approve AI-drafted pages.
- English is the only content language. (Open: D-023)
- 2 to 3 simultaneous Ask users is the design target.

## Acceptance criteria (summary)

Each phase in the [roadmap](13-roadmap.md) lists testable exit criteria. Cross-cutting criteria:

- Every requirement above maps to a design section and a test in [testing](11-testing-and-quality.md).
- No page, search result or answer is visible to a user outside its `access_scope`.
- No published page lacks front matter, sources, owner and reviewer.
- Every derived asset has a text equivalent and a source link.

## Traceability to the original strategy

| Original strategy item | Requirement |
| --- | --- |
| Ingest emails, transcripts, Confluence, Office files | F1 |
| Taxonomy and role mapping | F2 |
| C4 and TOGAF conversion | F3 |
| Search, sidebar, table of contents, lineage | F4 |
| Executive dashboards and technical deep-dives | F10, F4 |
| Operate inside the intranet perimeter | N1 |
| SSO and Active Directory | N2, S1 |
| Sub-second loads via SSG or ISR | N3 |
| Decoupled ingestion, AI and frontend | N4 |
| Scheduled cron or webhook rebuilds | N8 |
| Git history, blame, compliance checks | N7, I4 |
| Hands-on lab with VS Code, Claude Code, Cursor, GitHub | T1 |
| No exposure of live infrastructure telemetry | I5 |
