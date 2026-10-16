# Architecture summary

Short version of the design. Details live in the Technical Implementation Addendum.

## Content format

Every file in `content/` is Markdown with YAML front matter, validated in CI.

```yaml
---
title: vCenter Management Cluster
doc_type: c4-container
domain: infrastructure-architecture
priority: high
access_scope: it-ops
sources:
  - type: confluence
    id: "<page id>"
    version: "<version>"
last_ingested: "<ISO timestamp>"
reviewed_by: ""
---
```

## Pipeline

- Connectors write raw payloads and source metadata to a staging area. Staging is never committed.
- Sources: Confluence (REST API), email (IMAP or Microsoft Graph), Zoom or Teams transcripts (webhook), Office files (share watcher).
- The AI step chunks by structure, extracts entities and decisions, and drafts Markdown from per-type prompt templates.
- Output is validated against the front matter schema and a heading linter. Mermaid diagrams must parse.
- The pipeline opens a pull request. It never writes to `main`. A person approves.

## Site

- Next.js App Router with Tailwind CSS. Markdown is read from Git at build time. No headless CMS.
- Static generation for every page. Mermaid renders in a client component.
- Sidebar from the folder tree, table of contents from headings, lineage from front matter and `git log`.
- Middleware checks the SSO session and maps `access_scope` to directory groups.

## Search

- Self-hosted only. Pagefind to start. Meilisearch or Typesense if results must be filtered by `access_scope`.

## Assistant (Ask mode)

- Flow: embed the question, retrieve passages filtered by the viewer's access scope, build a prompt of 2,000 to 3,000 tokens of passages, stream the answer with source links.
- Model: local mixture-of-experts model with 3 to 4B active parameters, served by `llama-server` (llama.cpp) on a CPU-only Linux VM.
- VM: 16 vCPU, 128 GB RAM, 100% memory reservation, one NUMA node, virtual hardware version 20 or later.

## Hosting and CI/CD

- On-premises VM or Kubernetes. No public cloud host.
- A merge to `main` triggers CI: schema check, heading lint, Mermaid parse, policy scan, build, container image, deploy, search reindex.
- SSO through an OIDC or SAML identity provider federated to Active Directory.
