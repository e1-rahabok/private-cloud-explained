# 15. Documentation set

What a complete private-cloud knowledge base contains. Use it as a checklist when you fill `content/`.

The goal: a colleague, a new admin or an auditor can understand the whole environment from the site. What exists, how it fits together, how it runs, who runs it, and why it is built that way.

All values here are Proposed. Remove what your environment does not need.

## Two audience tiers

The site is internal. Every reader is a signed-in colleague. Inside the site there are two tiers.

| Tier | `access_scope` | Who | Purpose |
| --- | --- | --- | --- |
| Colleagues | `colleagues` | Every authenticated employee | Understand the private cloud, use its services, know who to ask |
| Infrastructure team | `infra-team` | Members of the infrastructure team's AD group | Build, run, fix and change the private cloud |

The CIO and leadership delegates see both tiers. See [executive summary](16-executive-summary.md).

- Both tiers live on one site. Pages in `infra-team` are invisible to everyone else: in navigation, search, Ask and derived media (S2).
- A colleague who opens an `infra-team` URL gets the same response as for a missing page.
- More scopes can be added, for example `security-team` for vulnerability detail. See [`config/access-scopes.example.yaml`](../config/access-scopes.example.yaml).
- The full scope model is in [security and governance](09-security-and-governance.md#audience-tiers). The decision is D-031.

### What goes in each tier

| Colleagues | Infrastructure team only |
| --- | --- |
| What the private cloud is and what it offers | Exact inventory, hostnames, IP plans, VLAN IDs |
| Service catalog, service levels, how to request | Firewall rule intent and segment-level detail |
| User guides | SOPs, runbooks, install and upgrade procedures |
| Architecture overview: layers, sites, high-level diagrams | Detailed component designs and configuration standards |
| Team pages: who owns what, how to raise a ticket | On-call rotations, escalation contacts, vendor case procedures |
| Security baseline status, summarised | Vulnerability detail, exceptions, hardening steps |
| Planned maintenance windows | Change plans, rollback steps, post-incident reviews |
| Decision records with no sensitive detail | Licence keys locations, contract numbers, support entitlements |

Credentials, tokens and private keys go in neither tier. They stay in the secrets store. Pages say where a secret lives, never what it is.

### Two-layer pages

Most systems need both a colleague view and a team view. Write two pages and link them.

- `infrastructure-architecture/storage.md`, scope `colleagues`: what storage exists, which tiers, what it is for.
- `inventory/storage-arrays.md`, scope `infra-team`: models, firmware, datastores, replication pairs, support contracts.

The colleague page shows the link only to users who can open the target (Proposed). The executive summary draws on both tiers.

## The checklist

Each row says where the page lives, its usual doc type and its default tier. "C" is `colleagues`. "I" is `infra-team`.

### 1. What exists: environment facts

| Item | Domain | `doc_type` | Tier |
| --- | --- | --- | --- |
| Data centres, rooms, racks, power, cooling, out-of-band management | `inventory` | `component` | I |
| Bill of materials: every product and version, firmware included | `inventory` | `bom` | I |
| Version compatibility matrix and support status | `inventory` | `bom` | I |
| Compute: clusters, host models, CPU generation, memory, EVC, HA and DRS settings | `inventory` | `component` | I |
| Storage: arrays or vSAN, datastores, storage policies, replication | `inventory` | `component` | I |
| Network: physical fabric, virtual switches, NSX segments, routing, load balancers | `inventory`, `connectivity-diagrams` | `component`, `architecture` | I |
| IP address plan and VLAN register | `connectivity-diagrams` | `component` | I |
| Management plane: each appliance, what it does, what it depends on | `inventory` | `component` | I |
| Shared services: DNS, NTP, AD, certificate authority, SMTP, syslog, jump hosts | `inventory` | `component` | I |
| Licences, renewal dates, vendor contracts, support levels | `lifecycle` | `bom` | I |
| Naming and tagging standards | `infrastructure-architecture` | `overview` | C |

### 2. How it fits together: architecture

| Item | Domain | `doc_type` | Tier |
| --- | --- | --- | --- |
| System map: facility, hardware, hypervisor, network and storage, management, platform services, tenants | `infrastructure-architecture` | `architecture` | C |
| One page per layer of that map | `infrastructure-architecture` | `architecture` | C summary, I detail |
| Dependency map: what needs what | `infrastructure-architecture` | `architecture` | I |
| Failure domains: host, rack, cluster, site, and what survives each | `infrastructure-architecture` | `failure-mode` | I |
| Blast-radius matrix: if X fails, what breaks | `infrastructure-architecture` | `failure-mode` | I |
| Start-up and shutdown order for a full power event | `sops` | `sop` | I |
| Tenancy model: business units, projects, environments | `infrastructure-architecture` | `architecture` | C |
| Workload placement rules: affinity, licence-bound clusters, tiers | `infrastructure-architecture` | `architecture` | I |
| Design principles and configuration standards | `infrastructure-architecture` | `overview` | C principles, I standards |
| Capacity model: overcommit ratios, headroom, growth forecast | `operations` | `operations-plan` | I |
| Architecture decisions | `decisions` | `decision` | C or I |

### 3. How it runs: operations management

| Item | Domain | `doc_type` | Tier |
| --- | --- | --- | --- |
| Service catalog and service levels (SLA, SLO, support hours) | `user-guides` | `service` | C |
| Incident, problem, change, request and release processes | `service-management` | `operations-plan` | C process, I detail |
| Change advisory board: when it meets, what needs approval | `service-management` | `operations-plan` | C |
| Life of a request, for example "a VM from ticket to running" | `service-management` | `walkthrough` | C |
| Monitoring catalog: each alarm, threshold, who is paged, which runbook | `operations` | `operations-plan` | I |
| Runbook per alarm or failure | `runbooks` | `runbook` | I |
| Backup scope, retention and restore tests | `operations` | `operations-plan` | I |
| Disaster recovery: RTO and RPO per tier, failover steps, test history | `operations` | `operations-plan` | C summary, I steps |
| Patch and upgrade calendar, maintenance windows, freeze periods | `lifecycle` | `operations-plan` | C |
| Privileged access, break-glass accounts, access reviews | `security` | `security-baseline` | I |
| Certificate and secret expiry register (dates, not secrets) | `lifecycle` | `bom` | I |
| Automation inventory: scripts, infrastructure as code, scheduled jobs, owners | `inventory` | `component` | I |
| Known issues and workarounds | `service-management` | `runbook` | I |
| Post-incident reviews | `service-management` | `post-incident-review` | I |
| Operational measures: availability, change success rate, time to restore | `operations` | `overview` | C |

### 4. Security and compliance

| Item | Domain | `doc_type` | Tier |
| --- | --- | --- | --- |
| Trust zones and threat model | `security` | `architecture` | I |
| Segmentation and firewall policy intent | `security` | `security-baseline` | I |
| Control mapping to the organization's frameworks | `security` | `security-baseline` | C status, I evidence |
| Vulnerability management process and patch service levels | `security` | `operations-plan` | C process, I findings |
| Audit evidence index: where each proof lives | `security` | `security-baseline` | I |

### 5. People, money and history

| Item | Domain | `doc_type` | Tier |
| --- | --- | --- | --- |
| Teams, roles, RACI | `team-structure` | `team` | C |
| On-call rotation and escalation matrix | `team-structure` | `team` | I |
| Vendor and partner escalation | `team-structure` | `team` | I |
| Cost model, showback or chargeback | `lifecycle` | `overview` | C |
| Lifecycle roadmap: end of support, refresh, upgrades, technical debt | `lifecycle` | `overview` | C summary, I detail |
| Onboarding path for a new admin: week 1, 2, 3 | `user-guides` | `guide` | I |
| Skills matrix and training | `team-structure` | `team` | I |
| Timeline: build, migrations, major incidents, major upgrades | `decisions` | `overview` | C |

## Pages that explain the whole machine

Write these first. They give a reader the full picture fastest.

0. **Executive summary.** Visual, one screen, every tier. CIO and leadership. See [executive summary](16-executive-summary.md).
1. **System map.** One diagram, facility to tenants. Colleagues.
2. **Life of a VM request.** One end-to-end walkthrough through every layer and team. Colleagues.
3. **Dependency graph.** Infrastructure team.
4. **Failure-domain and blast-radius matrix.** Infrastructure team.
5. **Start-up and shutdown order.** Infrastructure team.
6. **Bill of materials with compatibility status.** Infrastructure team.
7. **Alarm-to-runbook map.** Infrastructure team.

## Structured data

Some facts are tables, not prose. Keep them as YAML next to the page and let the site render them. Ask can then answer exact questions ("which version of vCenter runs in site B?").

| Data | Suggested file | Tier |
| --- | --- | --- |
| Bill of materials | `content/inventory/bom.yaml` | I |
| Licence and contract register | `content/lifecycle/licences.yaml` | I |
| Certificate expiry register | `content/lifecycle/certificates.yaml` | I |
| Alarm catalog | `content/operations/alarms.yaml` | I |
| Executive metrics | `content/executive/metrics.yaml` | I |

The file carries the same front matter fields as a page, including `access_scope`. The schema check validates it (Proposed).

## Keeping facts current

- The portal has no live connection to vCenter (I5). Inventory comes from dated exports, such as RVTools or vCenter reports, ingested as Office files.
- Each inventory page shows the export date. Old exports show the stale banner.
- Inventory pages get a short review cadence, for example 30 days. Architecture pages can use 180.

## Related

- [Content model](04-content-model.md): domains, doc types, scopes.
- [Security and governance](09-security-and-governance.md): tiers and policy scan per scope.
- [Site design](06-site-design.md): navigation per tier.
