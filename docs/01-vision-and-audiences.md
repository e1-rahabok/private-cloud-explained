# 1. Vision and audiences

## Vision

One private-cloud knowledge base, many ways to learn it.

People who need to understand the private cloud (the CIO, senior leaders, VMware administrators) get one trusted source. They choose how to consume it: read, search, ask, watch, listen, play, or take a quiz.

## The problem

From the original strategy document: architectural knowledge is spread across email threads, meeting records, Confluence pages, Office files, and static media. The result is knowledge silos and slower administrative work. It is also hard to show the architecture to senior leadership in a coherent form.

## What this project adds to the original strategy

The original strategy centres on the input: ingest artifacts, convert them to Markdown, build a Next.js site. This plan keeps all of that. It adds one shift of emphasis:

- Automation exists to keep the content current.
- Success is measured by how people consume and understand the content, not by how much was ingested.

The multiple ways to consume are therefore first-class requirements (F5 to F9 in [requirements](02-requirements.md)), not extras.

## Goals

| ID | Goal | Origin |
| --- | --- | --- |
| G1 | One trusted, searchable portal for private-cloud knowledge | Original strategy |
| G2 | Executive and CIO assurance: transparent architecture views, security baselines, operational guides | Original strategy |
| G3 | Several ways to consume the same content: read, search, ask, watch, listen, play, quiz | Project owner |
| G4 | Content stays current with low manual effort | Original strategy |
| G5 | A hands-on lab for VMware administrators using VS Code, Claude Code, Cursor and GitHub | Original strategy |
| G6 | Everything runs inside the corporate network, including the chat model | Original strategy, extended to the LLM |

## Non-goals

- Live monitoring or telemetry. The portal has no connection to vCenter or runtime state.
- Replacing the source systems. The portal is a derived, curated view of them.
- Public internet exposure of the deployed site. The site runs only inside the private cloud.
- Operating the private cloud. The assistant is read-only and takes no actions.
- A general-purpose chatbot. Ask answers only from portal content. (Proposed)

## Audiences

The people who **build** the site are VMware admins and infrastructure architects who follow this template ([how to use](00-how-to-use-this-template.md)). The people who **read** the site are the audiences below.

| Audience | Needs | Likely modes | Origin |
| --- | --- | --- | --- |
| CIO and senior leadership | A trustworthy overview, security baselines, evidence of operational control. Little time. Able to drill down. Sees every tier | Visual [executive summary](16-executive-summary.md), Listen, Watch | Original strategy |
| VMware and private cloud administrators | Exact procedures, installation and upgrade steps, quick answers, a way to keep skills current | Search, Ask, Read, Quiz, Play | Original strategy |
| New joiners and adjacent teams | A guided route into the environment | All modes | Proposed |
| Security and audit reviewers | Baselines, lineage, change history | Read, Search | Proposed |
| Content reviewers and owners | An efficient way to approve AI-drafted pages | Review pull requests | Proposed |

## Contexts of use

Modes are matched to the situation, not to a personality type. See [design considerations](12-design-considerations.md), DC-01.

| Situation | Modes that fit |
| --- | --- |
| "I need the answer now" | Search, Ask |
| "I need to understand how it fits together" | Read, Watch |
| "I want to learn while away from a screen" | Listen |
| "I want to test what I know" | Quiz, Play |
| "I need to brief someone" | Executive views, Read (summary) |
| "I need to show it is controlled" | Lineage, security baseline pages |

## Success measures (Proposed, targets set in Phase 0)

- Adoption: active readers per audience, and use of each mode.
- Answer quality: score on the assistant evaluation set ([testing](11-testing-and-quality.md)).
- Freshness: share of pages reviewed within their review cadence.
- Coverage: share of required document types present per domain.
- Findability: time and success rate on a fixed set of find-the-answer tasks.
- Leadership use: whether the portal is used in CIO briefings.

## Design principles

1. **Consumption first.** Decisions are judged by what helps a reader understand.
2. **One source of truth, many views.** Markdown in Git is the source. Video, audio, quizzes and games are derived and trace back to a page version.
3. **Provenance and trust.** Every page shows its sources, last ingestion, origin (human or AI) and reviewer.
4. **A person approves publication.** AI drafts. People merge.
5. **Inside the perimeter by default.** No external SaaS, no external LLM API.
6. **Decoupled components.** Ingestion, AI conversion, content, and frontend change independently.
7. **Fail visibly.** A failed validation blocks publication. Nothing degrades silently.
8. **Accessible by default.** Every audio and video asset has a text equivalent.
9. **Boring technology where possible.** Static generation, Git, Markdown.
10. **Right mode for the context.** The site offers modes. It does not profile users.
