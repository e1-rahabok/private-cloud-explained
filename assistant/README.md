# assistant

Ask mode: an AskIO-style chat that answers from the portal's own content.

Planned contents:

- Retrieval: embedding, hybrid search, access-scope filter.
- Prompt rules: answer only from the passages, cite page links, say so when the passages do not contain the answer.
- LLM serving: `llama-server` settings for the CPU-only VM. Model files are git-ignored.
  - Setup runbook: [llm/setup.md](llm/setup.md), with the [service unit](llm/llama-server.service) and [settings template](llm/llama-server.env.example).
  - Model provenance and checksums: [models.md](models.md).
- Bake-off notes: Gemma 4 26B-A4B, Qwen3.6-35B-A3B, gpt-oss-20b.
