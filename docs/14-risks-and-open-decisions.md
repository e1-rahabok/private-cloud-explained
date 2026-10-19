# 14. Risks and open decisions

## Risks

Likelihood and impact are Proposed judgments (L, M, H), not measurements.

| ID | Risk | L | I | Mitigation | Owner |
| --- | --- | --- | --- | --- | --- |
| R-01 | AI draft states something false and a reviewer misses it | M | H | Source beside draft, faithfulness rules, checklist, monthly accuracy sampling | Platform owner |
| R-02 | Restricted content visible through search or Ask | M | H | Scope filter before retrieval, scope matrix and leak tests | Security |
| R-03 | Secret or sensitive data enters Git or the model | M | H | Pre- and post-AI scans, push protection, quarantine | Security |
| R-04 | Ask is too slow or low quality on 16 vCPU | M | H | Phase 0 measurement, MoE model, short context, resize path | Platform owner |
| R-05 | A student commits real organizational data to the public template, an issue or a pull request | M | H | Work only in a private copy; disable push to the template remote; checklist in [how to use](00-how-to-use-this-template.md) | Student |
| R-06 | Generation of media competes with Ask for CPU | M | M | Off-hours batch, separate instance, throttle | Platform owner |
| R-07 | Content goes stale and trust is lost | H | H | Cadence, banners, owners, freshness report | Domain owners |
| R-08 | Reviewer capacity too low, backlog grows | H | M | Prioritise by `priority`, batch reviews, auto-reject low-signal drafts | Domain owners |
| R-09 | Prompt injection through ingested content | L | M | Passages as data, no tools, no outbound access, tests | Security |
| R-10 | Model licence or provenance problem | L | M | Review before adoption, record checksums | Platform owner |
| R-11 | Model or tool versions change quickly and break assumptions | H | M | Pin versions, evaluation regression, written decision records | Platform owner |
| R-12 | Scope creep into games and media before core is solid | H | M | Phase order, exit criteria, usage gates | Platform owner |
| R-13 | Source access refused by data owners | M | M | Early approval requests, start with Confluence | Platform owner |
| R-14 | Static-site access control implemented wrongly | M | H | Server-side checks, automated bypass tests, security review | Security |
| R-15 | Executive view mistaken for live monitoring | M | M | Explicit wording; no live indicators (DC-09) | Platform owner |
| R-16 | Single-VM web tier fails | M | M | Rebuild from Git, documented recovery, test | Platform owner |
| R-17 | Accessibility gaps in generated media | M | M | Captions and transcripts required, manual pass | Platform owner |
| R-18 | AI voice or video misunderstood as a real person or authoritative | L | M | Labelling, synthetic voice | Platform owner |
| R-19 | A hypervisor setting (EVC, NUMA, reservations) wipes out expected performance | M | M | Configuration checklist, verification step in Phase 0 | Virtualisation team |
| R-20 | Team lacks skills for the stack | M | M | Lab track, pairing, simple technology choices | Platform owner |

## Open decisions

Status: **Open** unless stated. "Needed by" is the phase before which a decision is required.

| ID | Decision | Options | Recommendation | Needed by |
| --- | --- | --- | --- | --- |
| D-001 | Does AskIO at isvara.io send the whole guide or retrieve passages? | Ask the isvara.io owners; infer from behaviour | Not needed to proceed. Local design uses retrieval regardless | Info only |
| D-002 | Which chat model? | Gemma 4 26B-A4B, Qwen3.6-35B-A3B, gpt-oss-20b, Qwen3-30B-A3B | Start with Gemma 4 26B-A4B. Decide by bake-off | Phase 0 |
| D-003 | Model licence acceptable? | Review each candidate's licence | Legal review of the chosen model | Phase 0 |
| D-004 | Embedding model | A small local multilingual or English model | Choose in Phase 0 with retrieval tests | Phase 0 |
| D-005 | Inference engine | llama.cpp `llama-server`, Ollama, vLLM CPU | llama.cpp | Phase 0 |
| D-006 | Sizing: keep 16 vCPU and 128 GB, or increase | Keep; 32 vCPU; add second VM | Keep, test, decide on measurements | Phase 0 |
| D-007 | Search engine | Pagefind, Meilisearch, Typesense, OpenSearch | Pagefind if scope pages can be filtered at the proxy; otherwise Meilisearch or Typesense | Phase 0 |
| D-008 | Vector store | Inside search engine; separate | Same engine if it supports it | Phase 0 |
| D-009 | Handling manual edits vs regeneration | Overwrite; propose diff only | Propose diff only | Phase 1 |
| D-010 | Where AI conversion runs | Same LLM VM; separate instance | Separate or off-hours | Phase 1 |
| D-011 | Review quorum for sensitive domains | One; two | Two for security baselines | Phase 1 |
| D-012 | Text-to-speech engine | A local open-source engine | Choose in Phase 3 by listening tests | Phase 3 |
| D-013 | Audio format | Single narrator; two-voice discussion | Single narrator first | Phase 3 |
| D-014 | Video production approach | Diagram animation via headless browser and encoder | As proposed | Phase 3 |
| D-015 | Quiz and game result storage and analytics | None; private per user; aggregate only | Private per user, aggregate by topic, no names | Phase 3 |
| D-016 | Which game concept | Incident desk, Change window, Architecture builder, Baseline hunt | Branching text scenario (Incident desk) first | Phase 4 |
| D-017 | CI system | Existing organization system | Use whatever exists | Phase 0 |
| D-018 | Hosting | Docker Compose on a VM; Kubernetes | Compose first | Phase 1 |
| D-019 | Identity provider path | ADFS; Keycloak federated to AD; other existing | Existing IdP | Phase 1 |
| D-020 | Classification of the corpus | Internal; restricted; per domain | Restricted until the data owner decides | Phase 0 |
| D-021 | Granularity of access scope | Per page; per section | Per page | Phase 1 |
| D-022 | Diagram source | Mermaid only; Mermaid plus SVG with source | Mermaid plus SVG with source | Phase 1 |
| D-023 | Content language | English only; add languages | English only | Phase 1 |
| D-024 | Regulatory or works-council review of logging and analytics | Organization confirms | Required before Phase 2 logging | Phase 2 |
| D-025 | Team size and capacity | Unknown | Provide to set phase durations | Phase 0 |
| D-026 | Names: portal, assistant | Open | Pick a name for the assistant | Phase 1 |
| D-027 | Repository model | Public template plus one private copy per student | **Decided.** This repository is the public template. Each student keeps a private copy with their own content and configuration | Closed |
| D-028 | Visibility of this GitHub repository | Public; private | **Decided: public.** It is a template with no private data. Students' copies are private | Closed |
| D-029 | Guest OS for the LLM VM | Ubuntu 24.04 LTS; Photon OS; a VKS node pool | **Decided: Ubuntu Server 24.04 LTS on a plain VM, with `open-vm-tools`.** llama.cpp builds and guides target Ubuntu. A plain VM keeps memory reservation, NUMA and hardware version under direct control | Closed |
| D-030 | Operational domains beyond the strategy's six | Keep six; add team structure, runbooks, operations, decisions | Add all four. Remove any not needed | Phase 0 |

## Assumptions to validate in Phase 0

- Hosts under the VM are Intel Xeon (4th generation or later) or AMD EPYC with fully populated memory channels.
- The IdP exposes group claims.
- Source systems allow read-only service accounts.
- Reviewers exist for each domain.
- 2 to 3 concurrent Ask users is enough at launch.

## Known unknowns

- Measured tokens per second and first-token time on the target host.
- How isvara.io implements AskIO.
- Volume and quality of the source material.
- Reviewer time available.
- Whether any source contains data that cannot be sent even to a local model.
