# TODO (Project Improvements)

This file captures prioritized tasks and suggested improvements for the KUWT project.

## 🔴 P0 — Critical (Stability & Accuracy)

- [ ] **Fix Agent Retry Recursion Bug**
  - Fix wrong method signature on retry in agent classes to prevent recursion errors.
- [ ] **Fix `TeachersResponse` Pydantic Model**
  - Resolve schema mismatch between the agent output and the Pydantic model.
- [ ] **Harden Redis Configuration**
  - Avoid import-time `os.environ` failures; ensure robust connection handling.
- [ ] **AI Filter for GitHub Repos**
  - Implement filtering in `src/tools/fetch_tools_and_news.py` to fetch only AI-related repositories.
- [ ] **Add HTTP Timeouts & Error Handling**
  - Ensure all external requests have appropriate timeouts and use `raise_for_status()`.

## 🟡 P1 — Important (Reproducibility & DX)

- [ ] **Standardize Execution Mode**
  - Align `PYTHONPATH` and run modes between local development and CI/CD.
- [ ] **Fix `.env` Loading in Tools**
  - Avoid CWD-dependent relative paths for loading environment variables.
- [ ] **Add Redis Seeding Documentation/Scripts**
  - Create a script or guide for populating the `fundamentals` and `covered` keys.
- [ ] **Clean Up Requirements**
  - Remove duplicate entries (e.g., `Markdown`) and version conflicts.
- [ ] **Add source to all the outputs generated from their respective sources**
  - Files: `src/tools/fetch_tools_and_news.py`, `src/tools/fetch_papers.py`, `src/tools/fetch_repos.py`

## 🟢 P2–P3 — Improvements (Features & Polish)

- [ ] **Modularize Publishing Flow**
  - Make `save_markdown` configurable via `.env` or CLI flags instead of hardcoded in `main.py`.
- [ ] **Improve Notion Block Logic**
  - Enhance `notion_publisher.py` to handle more markdown elements (e.g., lists, nested blocks) more robustly.
- [ ] **Add Package Structure**
  - Implement a proper `pyproject.toml` and clean up the package exports.
- [ ] **Testing & Quality**
  - Add unit tests for the orchestrator and individual agents.
  - Implement `ruff` linting and `pre-commit` hooks.
- [ ] **Expansion**
  - Multi-modal support: Generate images for Instagram posts.
  - Content scheduling directly from Notion status changes.
  - Support for Twitter/X, Bluesky, and TikTok.

---

_Items are prioritized by likelihood of causing failures and by developer/user impact._
