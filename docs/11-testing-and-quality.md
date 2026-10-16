# 11. Testing and quality

## Approach

Every requirement in [requirements](02-requirements.md) has at least one test or check. Content quality is tested like code.

## Test layers

| Layer | What | When |
| --- | --- | --- |
| Content checks | Schema, headings, Mermaid parse, policy scan, links | Every pull request |
| Unit tests | Parsers, chunker, scope mapping, prompt builder | Every pull request |
| Integration tests | Connector against a test source; pipeline end to end on sample sources | Nightly |
| Site tests | Routes, rendering, auth redirects, scope enforcement | Every pull request |
| Accessibility | Automated scan, keyboard walk-through, screen reader pass | Automated per pull request; manual per phase |
| Performance | Page weight, load timing against budget | Per build; baseline per phase |
| Assistant evaluation | Questions with expected answers and sources | Any change to model, prompt, chunking, index |
| Security tests | Scope bypass attempts, prompt injection, secret scan on samples | Per phase and on change |
| Load tests | 2 to 3 concurrent Ask users; page serving at expected concurrency | Phase 0 and before go-live |
| Recovery test | Rebuild from Git in a clean environment | Each phase |

## Requirement to test map

| Requirement | Test |
| --- | --- |
| F1, F2 | Connector integration tests; taxonomy tests |
| F3 | Conversion tests on gold sources; schema and heading validators |
| F4 | Search relevance set; lineage rendering test |
| F5 | Assistant evaluation set |
| F6, F7 | Manifest tests; caption and transcript presence; review sign-off check |
| F8, F9 | Quiz data validation; scenario validation; reviewer sign-off |
| F10 | Executive view build test; link-to-source check |
| F11 | Hash mismatch test marks asset out of date |
| F12 | Mode bar test per page |
| F13 | Pull request contents test |
| N1 | Network test: LLM VM has no outbound path; no external calls from the site |
| N2, S1 | Unauthenticated request test on all routes and media |
| N3 | Performance budget |
| N5 | Load test |
| N6 | Accessibility checks |
| N7 | Blame and history present; policy scan on seeded bad content |
| N8 | Webhook fires a build; nightly build runs |
| N9 | Alert test |
| N10 | Staging not tracked; secret scan on repo |
| I1, I2 | Instruction set check; local-only inference test |
| S2 | Scope matrix test across pages, nav, search, Ask |
| S3 | Injection test set |
| S4 | Seeded-secret test through the pipeline |
| S5 | Permission review of service accounts |

## Content quality rules

- Every published page has an owner and a reviewer.
- Facts match sources. Spot-check a sample of merged AI-drafted pages each month: compare against the source and score accuracy.
- Reviewer checklist is part of the pull request template.
- Pages past cadence appear on a freshness report.

## Gold set for conversion

- A set of real (or realistically synthetic) sources with human-written target pages.
- Used to compare prompt and model changes on conversion quality.
- Metrics: section coverage, factual accuracy, invented content rate, diagram validity.
- Size starts at 20 sources across all four source types and grows. (Proposed)

## Assistant evaluation set

| Category | Share (Proposed) | Example intent |
| --- | --- | --- |
| Single-fact lookup | 25% | "What is the supported upgrade path for X?" |
| Procedure | 25% | "How do I do Y?" |
| Multi-page synthesis | 15% | "What changes between A and B?" |
| Unanswerable | 15% | A question the docs do not cover; must refuse |
| Scope-restricted | 10% | Answer exists only in a restricted page |
| Ambiguous or follow-up | 10% | Needs a clarifying turn |

Each entry stores the question, the audience, the expected key facts, the expected source pages, and who wrote it. Questions come from real admin questions and from reviewers. Examples are not included here because none have been collected yet.

Scoring:

- Correctness: key facts present and no contradictions.
- Faithfulness: every claim supported by the cited passages.
- Citation validity: cited pages exist and support the claim.
- Refusal accuracy.
- Latency: time to first token and total time.

Thresholds are set after the first baseline. Release gate: no regression against the baseline on correctness or faithfulness, and zero scope leaks.

## Quiz and game quality

- Each question has one unambiguous correct answer verifiable in the cited section.
- A reviewer answers every question blind before seeing the key. Disagreement removes or fixes the question.
- Game scenarios are walked through by a domain expert.
- Feedback button on every question to report errors.

## Media quality

- Narration script read against the page by a reviewer.
- Pronunciation list checked.
- Captions timed and complete.
- Visuals match the page diagrams.

## Definition of done

For a content change: checks pass, reviewer approves, lineage correct.
For a code change: tests pass, docs updated, no new unreviewed dependency.
For a phase: exit criteria in the [roadmap](13-roadmap.md) are met and recorded.

## Metrics and review

Reviewed monthly by the platform owner:

- Freshness and coverage.
- Evaluation scores and trends.
- Usage by mode and audience.
- Feedback counts and top issues.
- Pipeline quarantine and rejection rates.
- Incidents.
