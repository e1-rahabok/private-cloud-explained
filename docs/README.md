# Documentation

Complete plan for the Private Cloud Explained template. No code exists yet. **Start with document 0.** Then read in order, or jump to a topic.

| # | Document | Covers |
| --- | --- | --- |
| 0 | [How to use this template](00-how-to-use-this-template.md) | Private copy, what to adapt, checklist |
| 1 | [Vision and audiences](01-vision-and-audiences.md) | Goals, non-goals, audiences, principles, success measures |
| 2 | [Requirements](02-requirements.md) | Functional, non-functional, infrastructure, security; traceability to the strategy |
| 3 | [Architecture](03-architecture.md) | Components, diagrams, interfaces, technology choices |
| 4 | [Content model](04-content-model.md) | Domains, doc types, front matter schema, lifecycle, derived assets |
| 5 | [Ingestion and AI conversion](05-ingestion-and-ai-conversion.md) | Connectors, safety scan, chunking, AI drafting, review |
| 6 | [Site design](06-site-design.md) | Information architecture, routes, page anatomy, accessibility, performance |
| 7 | [Learning modes](07-learning-modes.md) | Read, search, ask, listen, watch, quiz, play |
| 8 | [Assistant and local LLM](08-assistant-and-llm.md) | Retrieval, prompts, model choice, sizing, vSphere settings |
| 9 | [Security and governance](09-security-and-governance.md) | Threats, auth, scopes, review, retention |
| 10 | [Deployment and CI/CD](10-deployment-and-cicd.md) | CI/CD explained, 9-stage pipeline, hosting, monitoring |
| 11 | [Testing and quality](11-testing-and-quality.md) | Test layers, evaluation set, requirement-to-test map |
| 12 | [Design considerations](12-design-considerations.md) | Evidence-based design choices (DC-01 to DC-22) |
| 13 | [Roadmap](13-roadmap.md) | Phases, exit criteria, lab track |
| 14 | [Risks and open decisions](14-risks-and-open-decisions.md) | R-01 to R-20, D-001 to D-031 |
| 15 | [Documentation set](15-documentation-set.md) | What to document about the private cloud, audience tiers, checklist |
| - | [Reference](reference.md) | Diagram index, ID index, cross-checks |
| - | [Glossary](glossary.md) | Terms |
| - | [Source: strategy PDF](source/AI-Powered_Private_Cloud_Documentation_Platform_-_Strategy__Architecture.pdf) | Original strategy document |

## Where the technical addendum went

The addendum was one long document. Its content is now split by topic.

| Addendum section | Now in |
| --- | --- |
| Intro | [Vision](01-vision-and-audiences.md) |
| Requirements | [Requirements](02-requirements.md) |
| 1 Ingestion | [Ingestion](05-ingestion-and-ai-conversion.md) |
| 2 AI processing | [Ingestion](05-ingestion-and-ai-conversion.md), section 5 |
| 3 Next.js | [Site design](06-site-design.md), [Content model](04-content-model.md) |
| 4 Search | [Architecture](03-architecture.md), [Site design](06-site-design.md) |
| 5 Hosting and CI/CD | [Deployment and CI/CD](10-deployment-and-cicd.md) |
| 6 Local LLM | [Assistant and local LLM](08-assistant-and-llm.md) |

The text was restructured and extended, not copied verbatim. Where the addendum and these documents differ, these documents are current.

## Conventions

- **Proposed** marks a recommendation not yet confirmed.
- **Spec** and **Addendum** mark items from the original documents.
- Mermaid diagrams were not rendered or validated when written.
- Performance numbers for the target hardware are not stated because none were measured.
