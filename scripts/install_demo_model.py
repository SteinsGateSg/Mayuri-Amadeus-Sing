#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


def link_or_copy(source: Path, dest: Path, copy_files: bool) -> None:
    if not source.exists():
        raise FileNotFoundError(f"missing source: {source}")

    if dest.exists() or dest.is_symlink():
        if dest.is_symlink() or dest.is_file():
            dest.unlink()
        else:
            shutil.rmtree(dest)

    dest.parent.mkdir(parents=True, exist_ok=True)
    if copy_files:
        shutil.copy2(source, dest)
        print(f"[copy] {dest}")
    else:
        dest.symlink_to(source)
        print(f"[link] {dest} -> {source}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Expose the bundled demo model inside Applio logs/.")
    parser.add_argument("--copy", action="store_true", help="copy files instead of symlinking")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    source_dir = repo_root / "models" / "mayuri_rvc_v1"
    applio_log_dir = repo_root / "third_party" / "Applio" / "logs" / "mayuri_rvc_v1"

    if not (repo_root / "third_party" / "Applio").exists():
        print("[error] Applio source tree is missing", file=sys.stderr)
        return 1

    try:
        for name in ["mayuri_rvc_v1_200e_55200s.pth", "mayuri_rvc_v1.index"]:
            link_or_copy(source_dir / name, applio_log_dir / name, args.copy)
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print("[done] demo model prepared inside Applio logs/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
