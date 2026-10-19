# 9. Security and governance

## Principles

- Inside the perimeter. No external SaaS, no external model API (N1).
- Least privilege for people and services.
- Nothing sensitive is committed. Nothing unreviewed is published.
- Authorization is enforced on the server for every route, search result and answer.
- Fail closed. A missing or unknown access scope blocks publication and access.

## Data classification

Content in the portal is derived from internal sources. The sensitivity of the production corpus is decided by the data owner (D-020). Until then, treat it as internal and restricted.

## Audience tiers

The site is internal documentation for colleagues. The infrastructure team also has its own documentation that only it can see (D-031).

| Scope | Readers | May contain | Never contains |
| --- | --- | --- | --- |
| `colleagues` | Every authenticated employee | Overviews, service catalog, user guides, team pages, summarised status | Internal addresses, hostnames, VLAN IDs, detailed procedures, vulnerability detail |
| `infra-team` | Infrastructure team AD group | Everything above, plus inventory, IP plans, procedures, runbooks, incident reviews, contract detail | Credentials, tokens, private keys, personal data |

- The policy scan runs per scope. Address and hostname patterns fail the build in `colleagues` pages and pass in `infra-team` pages.
- A page moving from `infra-team` to `colleagues` needs approval from the infrastructure team lead.
- Derived media, search records and Ask passages inherit the scope of their page.
- Executive views use `colleagues` pages only.
- Access to `infra-team` pages is logged (Proposed).

| Data | Where | Classification handling |
| --- | --- | --- |
| Raw ingested material | `pipeline/staging`, not in Git | Restricted. Retention-limited. Deleted after the retention period |
| Published Markdown | Internal Git | Per `access_scope` |
| Search and vector index | Server | Same scope controls as content |
| Chat logs | Application store | Restricted. Retention-limited |
| Derived media | Media store | Same scope as source page |
| Model files | LLM VM | Internal. Provenance recorded |
| Secrets | Secrets store | Never in Git or logs |

## Threat model

| Threat | Example | Control |
| --- | --- | --- |
| Credential in a source | Password in an email thread | Pre-AI scan, quarantine, post-AI scan, repository secret scanning |
| Over-exposure | Restricted page appears in search | Scope filter on pages, nav, search, retrieval |
| Prompt injection | A page contains "ignore previous instructions" | Passages treated as data, no tools, no outbound access, tests |
| Wrong AI content published | Invented control marked as compliant | Mandatory human review, faithfulness rules, source beside draft |
| Pipeline account abuse | Pipeline merges its own change | Branch protection, separate reviewers, read-only connectors |
| Stale content misleads | Old upgrade steps followed | Review cadence, stale banners, lineage |
| Model supply chain | Tampered model file | Checksums, trusted source, internal transfer, scan |
| Leakage via logs | Questions contain sensitive text | Log minimization, retention, access controls |
| Denial of service on Ask | Many queries exhaust CPU | Rate limits, queue, per-user caps |
| Insider browsing | Wide access to the full corpus | Scope model, audit of access to restricted scopes |

## Authentication

- OIDC or SAML to the corporate IdP (ADFS or Keycloak federated with AD).
- Session cookie with short lifetime and refresh.
- Middleware or reverse proxy rejects unauthenticated requests on every route including APIs and media files (S1).

## Authorization

- Each page has one `access_scope`. `config/access-scopes.yaml` maps scopes to AD groups.
- At request time the user's groups resolve to a set of scopes.
- Static HTML is the same for everyone, so access is enforced before it is served: the proxy or middleware checks the page's scope and returns not-found when denied.
- Navigation, search and retrieval are built from the same scope set so titles do not leak.
- Open design question: scope per page only, or also per section. Start with per page (D-021).
- Where the search engine cannot filter by scope, a server-side search with filters is required (see [architecture](03-architecture.md)).

## Service accounts and secrets

| Account | Rights | Notes |
| --- | --- | --- |
| Confluence connector | Read on listed spaces | Read-only token |
| Mailbox connector | Read on one shared mailbox | App registration with limited mailbox scope |
| Transcript connector | Read recordings or transcripts | Limited to listed meeting series |
| Share watcher | Read on one folder | Read-only |
| Pipeline Git user | Push to branches, open pull requests | Cannot merge to `main` |
| CI | Read repo, build, deploy | No access to staging |
| App runtime | Read content and index | No write |
| LLM VM | Receives requests only | No outbound access |

Secrets sit in the organization's secrets store. They are injected at runtime. Rotation is scheduled. A leaked secret triggers rotation, not just removal.

## Repository controls

- The deployment's repository is private. It is a private copy of the public template.
- Branch protection on `main`: required review, required checks, no force-push, signed commits where available.
- CODEOWNERS maps domains to reviewers.
- Secret scanning and push protection on.
- The public template holds only design, reference code and invented samples. Keep real content out of it (D-027). A check in your private copy can block pushes to the template remote.

## Policy scan in CI

Checks Markdown for:

- Credentials and key material.
- Configured sensitive patterns.
- Disallowed terms or classifications.
- External links to non-approved domains. (Proposed)
- Embedded scripts or raw HTML beyond an allowed set.

Failure blocks the build.

## Review and approval workflow

| Content | Who reviews | Evidence |
| --- | --- | --- |
| AI-drafted page | Domain owner or delegate | Pull request approval, checklist |
| Human-authored page | A second person | Pull request approval |
| Security baseline page | Security team plus owner | Two approvals |
| Team page | Lead of that team | Pull request approval (Proposed) |
| Runbook | Owning team plus on-call representative | Pull request approval (Proposed) |
| Scope change from `infra-team` to `colleagues` | Infrastructure team lead | Pull request approval (Proposed) |
| Derived media | Content owner | Manifest `reviewed_by` |
| Prompt or model change | Platform owner plus evaluation result | Pull request with evaluation attached |

## Auditability (N7)

- Git history and blame for every page.
- Pull request record for every approval.
- Access logs for restricted scopes. (Proposed)
- Pipeline run logs with counts and outcomes, without content.
- Model and prompt versions recorded per assistant answer in logs.

## Privacy

- Raw sources can contain personal data (names, emails, voices). Ingestion keeps only roles where practical and strips signatures and addresses.
- The portal is not a place for HR or personal data. The scan and reviewers block it.
- Chat logs can contain personal data typed by users. Retention limit (Proposed: 90 days) and access limited to platform owners.
- Quiz and game results are private to the user by default (D-015).
- Applicable regulation and works-council or similar requirements are for the organization to confirm (D-024).

## Governance model

| Role | Responsibility |
| --- | --- |
| Platform owner | Roadmap, platform health, model and prompt changes |
| Domain owner | Accuracy of their domain's pages, review cadence |
| Reviewer | Approves pull requests |
| Security | Baselines, policy scan rules, scope mapping |
| Data owner | Classification of sources, approval to ingest a source |
| Admin | Taxonomy, connectors, scopes |

Ingestion of a new source requires approval by its data owner. The approval is recorded in `config/sources.md`. (Proposed)

## Retention

| Item | Proposed retention |
| --- | --- |
| Staging | 30 days |
| Chat logs | 90 days |
| Pipeline logs | 1 year |
| Published content | In Git for as long as the repository exists |
| Derived media | While the source page exists, plus the previous version |

Values are Proposed and need approval from the data owner.

## Incident response

- Sensitive content published by mistake: revert the merge, rebuild, purge the index and caches, rotate any exposed secret, notify the data owner, record the cause.
- Wrong AI answer reported: add to the evaluation set, trace to page or prompt, fix.
- Model file suspected tampered: stop the service, restore from a verified copy.

## Compliance mapping

The security-baseline pages themselves map controls to the organization's frameworks. This platform inherits the organization's controls for hosting, identity and logging. A control mapping specific to the platform is a Phase 1 deliverable.
