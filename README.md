# minicloud-agent

[![CI](https://github.com/andrelair-platform/minicloud-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/andrelair-platform/minicloud-agent/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://python.org)
[![Supply chain: cosign](https://img.shields.io/badge/supply%20chain-cosign%20signed-green)](https://github.com/sigstore/cosign)

> LangGraph ReAct research agent exposed as an OpenAI-compatible FastAPI service. Registered as `model: research-agent` in the minicloud LiteLLM proxy so it is available in Open WebUI and any OpenAI-compatible client. Runs on the self-hosted minicloud k8s platform (5-node k3s cluster) in the `ai` namespace alongside LiteLLM, RAG ingest, and vLLM.

**Live docs:** https://andrelair-platform.github.io/minicloud-agent/
**Platform docs:** https://andrelair-platform.github.io/minicloud-platform-docs/

---

## Table of Contents

- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [CI/CD Pipeline](#cicd-pipeline)
- [Endpoints](#endpoints)
- [Environment variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

---

## Architecture

```
Open WebUI / any OpenAI client
        │  model: research-agent
        ▼
  LiteLLM proxy (ai ns)
        │  routes to minicloud-agent:8080
        ▼
  minicloud-agent (FastAPI)
        │
        ├── rag_search ──► rag-ingest:8001 (internal KB)
        └── web_search ──► DuckDuckGo (public web)
        │
        ▼
  LiteLLM → mistral-small / vLLM
```

| Concern | Choice |
|---|---|
| Runtime | Python 3.12 |
| Framework | FastAPI + uvicorn |
| Agent | LangGraph `create_react_agent` (ReAct) |
| LLM routing | LiteLLM proxy (`mistral-small` default) |
| Tools | `rag_search` (internal KB) + `web_search` (DuckDuckGo) |
| Registry | `harbor.10.0.0.200.nip.io/library/minicloud-agent` |
| GitOps | `minicloud-gitops/services/minicloud-agent/` |
| Namespace | `ai` |

---

## Getting Started

```bash
# Prerequisites: Python 3.12
pip install -r requirements.txt

# Run locally (points to cluster LiteLLM via env var)
LITELLM_BASE_URL=https://litellm.devandre.sbs \
LITELLM_API_KEY=<your-key> \
uvicorn app.main:app --port 8080 --reload

# Lint + test
pip install -r requirements-test.txt
make lint
make test
```

---

## CI/CD Pipeline

| Step | Trigger | Tool |
|---|---|---|
| L0 lint | every push | ruff + mypy |
| L1 unit tests | every push | pytest (≥70% coverage) |
| Build + push | push to `main` | docker buildx → Harbor |
| Sign | push to `main` | cosign keyless |
| GitOps bump | push to `main` | `kustomize edit set image` in `services/minicloud-agent/minicloud-1/prod/` |

**Branch strategy:** `dev` direct push · `staging` PR required · `main` PR required

| Secret | Scope | Purpose |
|---|---|---|
| `TS_OAUTH_CLIENT_ID` | org | Tailscale CI tag |
| `TS_OAUTH_SECRET` | org | Tailscale CI tag |
| `MINICLOUD_CA_CERT` | org | Harbor TLS trust |
| `HARBOR_USER` | org | Harbor push |
| `HARBOR_PASSWORD` | org | Harbor push |
| `GITOPS_TOKEN` | org | GitOps overlay update |

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness — returns `{"status":"ok"}` |
| GET | `/ready` | Readiness — returns `{"status":"ready"}` |
| GET | `/v1/models` | Lists available agent models |
| POST | `/v1/chat/completions` | OpenAI-compatible chat; supports `stream: true` |

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `LITELLM_BASE_URL` | `http://litellm.ai.svc.cluster.local:4000` | LiteLLM proxy base URL |
| `LITELLM_API_KEY` | `sk-agent-internal` | LiteLLM master key |
| `RAG_INGEST_URL` | `http://rag-ingest.ai.svc.cluster.local:8001` | RAG query service URL |
| `AGENT_DEFAULT_MODEL` | `mistral-small` | Default LLM for tool-calling |
| `AGENT_MAX_ITERATIONS` | `6` | Max ReAct iterations per request |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
