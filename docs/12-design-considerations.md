# 12. Design considerations

Each consideration states the question, the evidence or reasoning, and the decision it leads to. Evidence sources are listed at the end. Items marked **Reasoned** come from general engineering or design practice and were not checked against a source for this document.

## DC-01. Offer modes by context, not by "learning style"

- Question: do different people need different modes?
- Evidence: Pashler, McDaniel, Rohrer and Bjork (2008) reviewed the "learning styles" idea. They found no adequate evidence that matching instruction to a person's stated style improves learning. They noted that the design needed to test it properly was rarely used.
- Implication: do not classify users or promise to match their style.
- Reason to offer several modes anyway: tasks and situations differ (quick answer, deep study, on the move, practice), and some content suits some forms (diagrams suit a visual walkthrough; commands suit text). Different representations also help people with different access needs.
- Decision: build modes around tasks and contexts. Show them as choices. Do not profile users or store a "preferred style". See [learning modes](07-learning-modes.md).

## DC-02. Include retrieval practice

- Evidence: retrieving information from memory improves long-term retention more than restudying. Pastötter and Bäuml (2014) review this research, building on Roediger and Karpicke (2006).
- Implication: quizzes are not decoration. They support learning.
- Decision: quizzes give immediate feedback with a link to the supporting section, allow retries, and resurface earlier questions. Keep stakes low. Do not use scores for assessment of people.

## DC-03. The page is the source of truth. Other modes are views

- Reasoned: two sources of truth drift apart.
- Decision: every asset records `page_id` and `content_hash` and is marked out of date when the page changes (F11). See [content model](04-content-model.md).

## DC-04. Trust is the product

- Reasoned: an executive or admin who finds one wrong statement stops using the portal.
- Decision: show provenance on every page (sources, origin, reviewer, dates). Require human review. Show a stale banner. Ask cites sources and refuses when unsure.

## DC-05. Static speed versus per-user access

- Tension: static pages load fast (N3) but are identical for all viewers. Access control (S2) varies by user.
- Options:
  - Enforce scope in a reverse proxy or middleware before serving static files. Simple and fast. Needs correct mapping.
  - Render per user on the server. Flexible. Slower, more load.
  - Separate sites per scope. Simple isolation. Duplication.
- Decision: proxy or middleware enforcement, with navigation and search built from the same scope set. Revisit if scopes become fine-grained (D-021).

## DC-06. CPU-only inference limits the experience

- Evidence from the sizing work: decode speed depends on memory bandwidth; prompt processing is the bottleneck; reasoning models are slow.
- Implications: short retrieved context, mixture-of-experts model, concurrency of 2 to 3, queue with visible state, caching.
- Decision: design the Ask experience for patience (streaming, status messages, queue position) and avoid features that need long prompts. See [assistant and LLM](08-assistant-and-llm.md).

## DC-07. Retrieval over whole-document prompts

- Reason: a long prompt would take minutes before the first word on CPU. Retrieval also supports citations and scope filtering.
- Decision: retrieval-first design. Whole-guide prompts are not used.

## DC-08. Executive needs differ from admin needs

- Reasoned: executives want a verified overview with the ability to drill in; admins want exact steps.
- Decision: summary-first page structure, an executive view, `audience` in front matter, and links from every executive figure to its source page.

## DC-09. Do not imply live status

- Risk: a dashboard with green indicators is read as monitoring.
- Decision: executive views show content review status only, and say so. There is no connection to live systems (I5).

## DC-10. Accessibility as a foundation

- Reasoned and required by N6: multiple modes help only if each is itself accessible. A video without captions fails some readers.
- Decision: WCAG 2.2 AA target; transcripts and captions; keyboard operation; reduced-motion respect; untimed play by default.

## DC-11. AI-generated media needs a gate

- Risks: invented details in a script; mispronounced product names; a voice that sounds like a real person.
- Decision: scripts are generated from the page only, reviewed by a person, labelled as AI-generated; use a synthetic voice that does not imitate a real person; keep a pronunciation list.

## DC-12. Keep the games honest and small

- Risk: Play can consume the project.
- Decision: proposals only until Phase 3 usage shows demand; begin with branching text scenarios; simulations never connect to live systems.

## DC-13. Gamification can distort

- Reasoned: leaderboards and streaks can turn learning into competition, pressure staff, and raise privacy concerns.
- Decision: no leaderboard by default; scores private; aggregate topic difficulty only (D-015).

## DC-14. Content freshness is the operational risk

- Reasoned: documentation decays.
- Decision: `review_cadence_days`, stale banners, freshness report, owners on every page, automated refresh from sources.

## DC-15. AI draft versus human edit

- Problem: regenerating a page can overwrite a reviewer's improvements.
- Decision: propose diffs against the published page and never overwrite (D-009).

## DC-16. Reuse the organization's tools

- Reasoned: a new CI or identity system adds cost and approval.
- Decision: reuse existing CI and IdP where they exist (I3). Document a minimal fallback.

## DC-17. Keep boring technology at the core

- Reasoned: a small team must operate this.
- Decision: static generation, Git, Markdown, one search engine, one inference engine. Add services only when a measured need appears.

## DC-18. Performance budgets

- Reasoned: sub-second loads are a stated goal (N3), and lazy loading keeps heavy modes from slowing plain reading.
- Decision: budgets in [site design](06-site-design.md); lazy-load Mermaid, search, chat, quiz and game.

## DC-19. Public repository versus private content

- Fact: this GitHub repository is currently public.
- Risk: production content pushed here would be exposed.
- Decision: this repository holds code, docs and synthetic samples only (D-027); production content stays in an internal repository; a check blocks suspicious content. Visibility of this repository is the owner's decision.

## DC-20. Measure before claiming

- Reasoned: sizing statements about speed vary by host.
- Decision: no performance claim for this hardware until Phase 0 measurements exist. Targets are labelled Proposed.

## DC-21. Language and tone

- Decision: plain English, short sentences, defined terms, a glossary. Executive pages avoid acronyms without expansion. See [glossary](glossary.md).

## DC-22. Feedback loop

- Decision: feedback on every page, answer, question and asset; feeds the evaluation set and the backlog.

## Evidence sources

- Pashler, H., McDaniel, M., Rohrer, D., and Bjork, R. (2008). Learning styles: Concepts and evidence. *Psychological Science in the Public Interest*, 9(3), 105 to 119. https://digitalcommons.usf.edu/psy_facpub/1765/
- Pastötter, B., and Bäuml, K.-H. T. (2014). Retrieval practice enhances new learning: the forward effect of testing. *Frontiers in Psychology*. https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00286/pdf . This article discusses Roediger and Karpicke (2006), which was not opened directly.

CPU inference reasoning in DC-06 comes from the sizing analysis in this project. It has not been measured on the target hardware.
