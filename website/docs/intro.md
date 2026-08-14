---
id: intro
title: Overview
sidebar_label: Overview
slug: /
---

# minicloud Agent

**LangGraph ReAct research agent** exposed as an OpenAI-compatible FastAPI service. Registered as `model: research-agent` in the minicloud LiteLLM proxy — accessible from Open WebUI and any OpenAI-compatible client without any additional configuration.

## Responsibility

| In scope | Out of scope |
|---|---|
| ReAct agent loop (LangGraph `create_react_agent`) | LiteLLM configuration (minicloud-gitops) |
| `rag_search` tool — queries `rag-ingest` internal KB | RAG ingestion pipeline (ai namespace manifests) |
| `web_search` tool — DuckDuckGo public search | Model serving (vLLM / LiteLLM) |
| OpenAI-compatible `/v1/chat/completions` + streaming | Open WebUI model registration |

## Stack

| Concern | Choice |
|---|---|
| Runtime | Python 3.12 |
| Framework | FastAPI + uvicorn |
| Agent | LangGraph `create_react_agent` (ReAct) |
| LLM routing | LiteLLM proxy — `mistral-small` default |
| Tools | `rag_search` (internal KB) + `web_search` (DuckDuckGo) |
| Container | `python:3.12-slim`, non-root UID 1000 |
| Registry | `harbor.10.0.0.200.nip.io/library/minicloud-agent` |
| Namespace | `ai` (shared AI services namespace) |

## Request flow

```
Client (Open WebUI / curl)
    │  POST /v1/chat/completions
    │  model: research-agent
    ▼
LiteLLM proxy  ──routes──►  minicloud-agent:8080
                                │
                    ┌───────────┴───────────┐
                    │  LangGraph ReAct loop  │
                    │  (max 6 iterations)    │
                    └───────────┬───────────┘
                                │  calls tools
                    ┌───────────┴───────────┐
                    ▼                       ▼
             rag_search              web_search
             rag-ingest:8001         DuckDuckGo
             (internal KB)           (public web)
                    │
                    └──► LiteLLM → mistral-small (tool-calling LLM)
```

## GitOps location

```
minicloud-gitops/services/minicloud-agent/
  base/
    deployment.yaml      # no namespace, no image tag
    service.yaml
    kustomization.yaml
  minicloud-1/
    prod/
      kustomization.yaml  # namespace: ai, images.newTag bumped by CI on main push
      certificate.yaml    # agent.10.0.0.200.nip.io TLS
      ingress.yaml        # internal-only (nip.io); LiteLLM is the external entry point
```

## Links

- [GitHub repository](https://github.com/andrelair-platform/minicloud-agent)
- [LiteLLM](https://litellm.devandre.sbs)
- [Open WebUI](https://chat.devandre.sbs)
- [Platform documentation](https://andrelair-platform.github.io/minicloud-platform-docs/)
