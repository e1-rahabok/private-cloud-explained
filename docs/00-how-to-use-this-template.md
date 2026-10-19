# 0. How to use this template

Read this first.

## What this repository is

- A **public template**. It is a worked design for building a private-cloud documentation website with a local LLM.
- It contains instructions, design documents and (later) reference code. It contains **no private data**.
- The website you build from it is **100% private**. It runs only on your private cloud. It is not on the internet.
- The reference model is a site like isvara.io (read, search, ask, watch, listen, play, quiz), but hosted inside your network, with a local LLM instead of a hosted one.

## Who this is for

VMware administrators and infrastructure architects. You follow this repository, study it, and build **your own** application for **your own** organization.

## Two repositories, two roles

| | This repository (the template) | Your copy |
| --- | --- | --- |
| Visibility | Public | **Private** |
| Holds | Design docs, reference code, sample content | Your adapted code, your content, your config |
| Contains your data? | Never | Yes |
| Who writes to it | The course author | You |

## Step 1. Create your private copy

Do this before changing anything.

Option A, GitHub template (if the author has enabled it):
1. Click **Use this template**, then **Create a new repository**.
2. Set visibility to **Private**.
3. Clone your new repository.

Option B, manual copy (always works):
1. Create an empty **private** repository in your organization's Git service (GitHub, GitLab, Bitbucket, Azure DevOps or another).
2. Clone this template: `git clone <template-url> my-private-cloud-docs`
3. Point it at your private repository: `git remote rename origin template`, then `git remote add origin <your-private-url>`
4. Push: `git push -u origin main`
5. Stop accidental pushes to the public template: `git remote set-url --push template DISABLED`

Notes:
- A GitHub **fork** of a public repository cannot be made private. Do not use Fork for this.
- To receive later updates from the template, run `git fetch template` and merge or cherry-pick what you want. Optional.

## Step 2. Rule: nothing from your organization goes back to the template

- Never push to the template remote.
- Never paste real hostnames, addresses, credentials, mail, meeting content or internal documents into this public repository, an issue, or a pull request.
- Report template problems using generic examples only.

## Step 3. Study the design

Read [docs/README.md](README.md) in order. The documents describe what to build and why. Decisions are listed in [risks and open decisions](14-risks-and-open-decisions.md). Make your own call on each and record it in your copy.

## Step 4. Adapt it to your organization

The template cannot know your systems. These are the parts you change.

| Area | Template assumption | What you do | Doc |
| --- | --- | --- | --- |
| Document sources | Confluence, email, Zoom/Teams transcripts, Office files | Keep the connectors you have. Replace others with connectors for your systems (SharePoint, Wiki, ServiceNow KB, Slack, file shares, etc.) | [Ingestion](05-ingestion-and-ai-conversion.md) |
| Email system | IMAP or Microsoft Graph | Choose the interface your mail system offers | [Ingestion](05-ingestion-and-ai-conversion.md) |
| Intranet / wiki | Confluence REST | Write a connector for yours | [Ingestion](05-ingestion-and-ai-conversion.md) |
| Login (identity) | OIDC or SAML to an IdP such as ADFS or Keycloak, federated to AD | Configure your IdP, client IDs, redirect URIs, group claims | [Security](09-security-and-governance.md) |
| Access scopes | `colleagues` and `infra-team`, mapped to AD groups | Define your scopes and your group names in `config/` | [Content model](04-content-model.md) |
| Taxonomy | Thirteen domains, sixteen doc types (seven domains and nine types Proposed) | Rename or add domains and types for your environment | [Content model](04-content-model.md) |
| CI/CD | Generic 9-stage pipeline | Implement the stages in the CI system you already run | [CI/CD](10-deployment-and-cicd.md) |
| Hosting | Docker Compose on a VM, or Kubernetes | Pick what your platform team supports | [CI/CD](10-deployment-and-cicd.md) |
| LLM hardware | 16 vCPU, 128 GB RAM, CPU only | Size to your hosts. Measure before you commit | [Assistant](08-assistant-and-llm.md) |
| Model | Shortlist of open-weight models | Run your own bake-off on your hardware | [Assistant](08-assistant-and-llm.md) |
| Policy scan | Secrets and configurable patterns | Add your classification markings and rules | [Security](09-security-and-governance.md) |
| Names and branding | Neutral | Name your portal and assistant | [Risks and decisions](14-risks-and-open-decisions.md), D-026 |

## Step 5. Build in phases

Follow the [roadmap](13-roadmap.md): measure first (Phase 0), then Read and Search, then Ask, then Listen/Watch/Quiz, then Play. Each phase has exit criteria.

## Step 6. Keep your site private

- Deploy only inside your network.
- No external SaaS and no external LLM API (N1).
- Review the [security and governance](09-security-and-governance.md) document before any real source is connected.
- Get the data owner's approval for each source before ingesting it.

## How to read the other documents

- The documents describe a **reference design for an internal, authenticated, private-cloud deployment**. SSO, access scopes and "no external SaaS" are requirements of *your* deployment, not of this template repository.
- Items marked **Proposed** are recommendations. Change them.
- Examples and sample content in this repository are invented.

## Checklist before you ingest real data

- [ ] My copy is a private repository.
- [ ] The template remote cannot be pushed to.
- [ ] My IdP is configured and unauthenticated access is blocked.
- [ ] Access scopes map to my groups. `colleagues` and `infra-team` exist.
- [ ] The policy scan has my patterns.
- [ ] The data owner approved the source.
- [ ] Raw staging storage is excluded from Git and has a retention limit.
- [ ] The LLM VM has no outbound internet access.
