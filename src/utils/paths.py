from __future__ import annotations

from pathlib import Path

# `src/` directory (this file lives in `src/utils/`).
SRC_DIR: Path = Path(__file__).resolve().parents[1]

# Repository root (parent of `src/`).
REPO_ROOT: Path = SRC_DIR.parent

# Project data directories (kept under `src/assets/` to match current layout).
ASSETS_DIR: Path = SRC_DIR / "assets"
ASSETS_INPUT_DIR: Path = ASSETS_DIR / "input"
ASSETS_OUTPUT_DIR: Path = ASSETS_DIR / "output"

# Logs directory (kept at repo root, regardless of CWD).
LOGS_DIR: Path = REPO_ROOT / "logs"

