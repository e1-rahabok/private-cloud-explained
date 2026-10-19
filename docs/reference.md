# Reference

Indexes and cross-checks. Use this to find an item and to confirm the documents agree.

## 1. Diagram index

8 Mermaid diagrams. GitHub renders them in **Preview** view of each file. In **Code** view they show as text.

| # | Diagram | Type | Where | What it shows |
| --- | --- | --- | --- | --- |
| 1 | Overview | Flowchart | [03 Architecture, "Overview diagram"](03-architecture.md#overview-diagram) | Sources to pipeline to Git to CI to site, search, chat, LLM, media |
| 2 | Page lifecycle | State diagram | [04 Content model, "Lifecycle"](04-content-model.md#lifecycle) | Staged, drafted, in review, published, stale, retired |
| 3 | Ingestion flow | Flowchart | [05 Ingestion, "Flow"](05-ingestion-and-ai-conversion.md#flow) | Trigger, fetch, scan, tag, chunk, draft, validate, pull request |
| 4 | Information architecture | Flowchart | [06 Site design, "Information architecture"](06-site-design.md#information-architecture) | Home, domains, modes hub, Ask, Search |
| 5 | Derived-asset pipeline | Flowchart | [07 Learning modes, "Generation pipeline for derived assets"](07-learning-modes.md#generation-pipeline-for-derived-assets) | Page to script or questions to review to asset, plus out-of-date marking |
| 6 | Ask request flow | Sequence diagram | [08 Assistant, "Request flow"](08-assistant-and-llm.md#request-flow) | User, site, authorization, retrieval, LLM |
| 7 | Build and deploy | Flowchart | [10 Deployment, "Build and deploy flow"](10-deployment-and-cicd.md#build-and-deploy-flow) | The 9 CI/CD stages |
| 8 | Phases | Flowchart | [13 Roadmap (top)](13-roadmap.md) | Phase 0 to Phase 4 |
| 9 | Executive page layout | Flowchart | [16 Executive summary, "Page layout"](16-executive-summary.md#page-layout) | Tiles, decisions, system map, themed sections |
| 10 | System map | Flowchart | [16 Executive summary, "System map"](16-executive-summary.md#system-map) | Seven layers with status words |
| 11 | Capacity runway | XY chart | [16 Executive summary, "Capacity runway"](16-executive-summary.md#capacity-runway) | CPU use against threshold |
| 12 | Operations health | XY chart | [16 Executive summary, "Operations health"](16-executive-summary.md#operations-health) | Incidents per month |
| 13 | Lifecycle roadmap | Gantt | [16 Executive summary, "Lifecycle roadmap"](16-executive-summary.md#lifecycle-roadmap) | End of support, planned work, renewals |
| 14 | Top risks | Quadrant chart | [16 Executive summary, "Top risks"](16-executive-summary.md#top-risks) | Likelihood by impact |

Verification status:

| # | Parses and renders (Mermaid CLI 11, headless Chromium) | Seen in GitHub Preview |
| --- | --- | --- |
| 1 | Yes | Yes (author's screenshot) |
| 2 to 8 | Yes | Not yet confirmed |
| 9 to 14 | Yes (Mermaid 11.x, headless Chromium) | Not yet confirmed |

Diagram rules for contributors:

- Every diagram is followed by text that says what it shows (accessibility, N6).
- Diagrams are Mermaid source in Markdown, so they diff and review like text.
- Add a new diagram to this table in the same commit.

## 2. Requirement index

Where each ID prefix is defined and used.

| Prefix | Meaning | Defined in | Tested in |
| --- | --- | --- | --- |
| G1 to G6 | Goals | [01](01-vision-and-audiences.md) | n/a |
| F1 to F14 | Functional | [02](02-requirements.md) | [11, requirement-to-test map](11-testing-and-quality.md) |
| N1 to N10 | Non-functional | [02](02-requirements.md) | [11](11-testing-and-quality.md) |
| I1 to I7 | Infrastructure | [02](02-requirements.md) | [11](11-testing-and-quality.md) |
| S1 to S6 | Security | [02](02-requirements.md), detail in [09](09-security-and-governance.md) | [11](11-testing-and-quality.md) |
| T1 | Hands-on lab | [02](02-requirements.md), track in [13](13-roadmap.md) | n/a |
| DC-01 to DC-22 | Design considerations | [12](12-design-considerations.md) | n/a |
| R-01 to R-20 | Risks | [14](14-risks-and-open-decisions.md) | n/a |
| D-001 to D-032 | Decisions | [14](14-risks-and-open-decisions.md) | n/a |

## 3. Figures that appear in more than one document

If one changes, change all of them.

| Figure | Value | Documents |
| --- | --- | --- |
| LLM VM size | 16 vCPU, 128 GB RAM | 00, 02 (I1), 08, 10, 14 |
| First-word target | 20 s (N5) | 02, 08, 11, 13 |
| Ask concurrency | 2 to 3 users | 02, 08, 11, 12, 13, 14 |
| Accessibility target | WCAG 2.2 AA (N6) | 02, 06, 12 |
| CI/CD stages | 9 | 10 (definition), 00 |
| Staging retention | 30 days (Proposed) | 05, 09 |
| Chat log retention | 90 days (Proposed) | 09 |
| Front matter fields | See table | 04 (definition), 05 (validation), 11 (checks), 10 (stage 2) |
| Domains | 14 (6 from strategy, 8 Proposed) | 04 (definition), 06 (navigation), 15, 00, content/README |
| Doc types | 17 (7 original, 10 Proposed) | 04 (definition), 15, 00 |
| Audience tiers | 2: `colleagues`, `infra-team`; leadership reads all | 04, 09 (definition), 15, 06, config/access-scopes.example.yaml |

## 4. Source to documentation map

| Source | Now in |
| --- | --- |
| Strategy PDF | [source/](source/) and all documents. Traceability table in [02](02-requirements.md) |
| Technical addendum | Mapping table in [README](README.md) |
| Sizing and model research | [08](08-assistant-and-llm.md), [12 DC-06](12-design-considerations.md) |
| Learning-style and retrieval-practice evidence | [12 DC-01, DC-02](12-design-considerations.md) |

## 5. Cross-check procedure

Run before each release of the template. Steps 1 to 3 can be scripted (Phase 1 task).

1. **Links.** Every relative Markdown link resolves.
2. **IDs.** Every F, N, I, S, T, DC, R and D ID used in a document is defined once.
3. **Diagrams.** Every Mermaid block parses. The diagram table above lists every block.
4. **Figures.** Section 3 values match in every listed document.
5. **Requirements to tests.** Every requirement in [02](02-requirements.md) appears in the [test map](11-testing-and-quality.md).
6. **Decisions.** Every "Open" decision has a "Needed by" phase in [14](14-risks-and-open-decisions.md).
7. **Terms.** New terms are in the [glossary](glossary.md).
8. **No private data.** The public template contains only invented samples.

Cross-check of this commit (author's run): links, D-xxx IDs and diagram parsing were checked. Steps 4 to 7 were checked by reading, not by script.

## 6. Glossary

See [glossary](glossary.md).
