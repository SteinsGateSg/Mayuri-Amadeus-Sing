#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
import sys


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    applio_dir = repo_root / "third_party" / "Applio"

    if not applio_dir.exists():
        print(f"[error] Applio not found: {applio_dir}", file=sys.stderr)
        return 1

    os.chdir(applio_dir)
    sys.path.insert(0, str(applio_dir))

    from core import run_prerequisites_script  # noqa: PLC0415

    print("[prepare] ensuring Applio runtime prerequisites are present")
    run_prerequisites_script(
        pretraineds_hifigan=True,
        models=True,
        exe=(os.name == "nt"),
    )
    print("[done] Applio runtime prerequisites are ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
