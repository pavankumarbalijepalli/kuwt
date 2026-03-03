# TODO (Project Improvements)

This file captures suggested improvements discovered during a repo-wide review. Items are prioritized by likelihood of causing failures and by developer/user impact.

## P0 — Fix “can’t run / can’t ship” issues

- [ ] **Standardize run mode (CWD/PYTHONPATH) across local + CI**
  - Decide one supported invocation and make *everything* match it:
    - **Option A**: `cd src && python main.py`
    - **Option B**: `PYTHONPATH=src python src/main.py`
  - Align `.github/workflows/kuwt.yml` and `README.md` to the chosen option.
  - Files: `src/main.py`, `.github/workflows/kuwt.yml`, `README.md`

- [ ] **Fix agent retry recursion bugs (crash on first retry)**
  - Retry branches currently call the method with the wrong signature.
  - Files: `src/agents/researchers.py` (confirmed), also check `src/agents/teachers.py`, `src/agents/enthusiasts.py`

- [ ] **Fix Teacher model/schema mismatch (Pydantic validation risk)**
  - `TeachersResponse` fields are `List[...]`, but `src/agents/teachers.py` passes a single object for each platform.
  - Files: `src/models/fundamentals.py`, `src/agents/teachers.py`

- [ ] **Harden Redis configuration + missing-key behavior**
  - Avoid `os.environ["REDIS_URL"]` at import time; prefer runtime creation and clear error messages if missing.
  - Handle missing Redis keys (`fundamentals`, `covered`) gracefully (avoid `json.loads(None)`).
  - Files: `src/tools/fetch_topics.py`, `src/tools/fetch_tools_and_news.py`

- [ ] **Add HTTP timeouts + status handling to external requests**
  - Add `timeout=...`, `raise_for_status()`, and minimal retry/backoff where appropriate.
  - Files: `src/tools/fetch_papers.py`, `src/tools/fetch_tools_and_news.py`

- [ ] **Fix `prepare_body()` unpacking safety**
  - `prepare_enthusiast()` may return `None`, but `prepare_body()` unpacks unconditionally.
  - File: `src/main.py`

## P1 — Docs/config correctness (prevent user misconfiguration)

- [ ] **Fix README repo name + architecture snippets**
  - README says `cd air-kai-content` but repo is `air-kuwt`.
  - README architecture tree uses `air-kai-content/`.
  - File: `README.md`

- [ ] **Make README env vars match real code**
  - Code uses `EMAIL_FROM`, `EMAIL_PASSWORD`, `EMAIL_TO` (and hardcodes Gmail SSL), but README documents `SMTP_*` + `SENDER_*`.
  - Also document required variables used by tools: `REDIS_URL`, `HF_TOKEN` (and any LLM keys).
  - Files: `README.md`, `src/utils/email_handler.py`, `src/tools/fetch_papers.py`, `.github/workflows/kuwt.yml`

- [ ] **Fix Web UI run instructions**
  - README says `python src/app.py`, but `src/app.py` uses `Path("agents")` relative to CWD.
  - Document the correct command (likely `cd src && streamlit run app.py`) *or* adjust UI to resolve paths robustly.
  - Files: `README.md`, `src/app.py`

- [ ] **Clarify “JSON inputs vs Redis” and add a seeding story**
  - README points to `src/assets/input/fundamentals.json` / `covered.json`, but runtime tools use Redis keys `fundamentals` and `covered`.
  - Decide: Redis-only, file-only, or file fallback; document and provide a seed step/script.
  - Files: `README.md`, `src/tools/fetch_topics.py`, `src/tools/fetch_tools_and_news.py`, `src/assets/input/*`

- [ ] **Replace brittle `.env` loading**
  - `src/tools/fetch_papers.py` does `load_dotenv('../../.env')` (CWD-dependent).
  - Prefer loading `.env` once in the entrypoint (or resolve path relative to the repo root).
  - File: `src/tools/fetch_papers.py`

## P1 — Dependencies reproducibility

- [ ] **Make `requirements.txt` accurate**
  - Add missing runtime deps (at least): `streamlit` (used by `src/app.py`), `langchain-openai` (used by `src/brains/github_openai.py`).
  - Consider moving optional features to separate extras files (e.g., `requirements-ui.txt`, `requirements-stt.txt`).
  - Remove duplicate `Markdown==3.10` line.
  - Files: `requirements.txt`, `src/app.py`, `src/brains/github_openai.py`, `src/utils/stt.py`

## P2 — Pathing, structure, and maintainability

- [ ] **Make file paths robust (stop relying on CWD)**
  - Resolve `assets/` and `logs/` relative to a single base directory (e.g., repo root or module location).
  - Files: `src/main.py`, `src/agents/*.py`, `src/utils/logger.py`, `src/app.py`

- [ ] **Choose a packaging direction**
  - **Minimal**: document `PYTHONPATH=src` (or enforce `cd src`) and keep current layout.
  - **Best long-term**: add `pyproject.toml`, make a proper package (e.g., `src/kuwt/...`), expose `python -m kuwt` / `kuwt` console entrypoints.
  - Files: new `pyproject.toml` (if chosen), imports across `src/**`

- [ ] **Make `src/app.py` actually run agents**
  - Today it looks for a module-level `run` function that your agent modules don’t expose.
  - Options: (a) add adapters with a `run()` function per agent module; (b) make UI instantiate the agent classes; (c) redesign UI around orchestrator.
  - Files: `src/app.py`, `src/agents/*.py`

## P3 — Quality, testing, and operational hardening

- [ ] **Add minimal test coverage**
  - Unit tests for: orchestrator content assembly (`prepare_*`), “no content” flows, parsing of fetched data (with HTTP mocking).
  - Files: add `tests/` (new), target `src/main.py`, `src/tools/*`

- [ ] **Add lint/format tooling**
  - Add `ruff` + `pytest` (+ optional `pre-commit`) to prevent regressions like the retry bug and to standardize formatting.

- [ ] **Improve logging robustness**
  - Use context manager for file writes; ensure log directory is consistent regardless of CWD.
  - File: `src/utils/logger.py`

## Notes / quick audit pointers

- The GitHub Actions workflow currently runs `python src/main.py` (repo root CWD). If you keep relative `assets/...` paths, that’s a consistent source of “writes to wrong folder” bugs.
- External HTTP calls currently have no timeouts. This is a common CI flake/hang source.

