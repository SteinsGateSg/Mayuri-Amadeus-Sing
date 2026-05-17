#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


SUPPORTED_SUFFIXES = {".wav", ".mp3", ".flac", ".m4a", ".ogg", ".opus"}


def ensure_link(source: Path, dest: Path, force: bool) -> None:
    if not source.exists():
        raise FileNotFoundError(f"source not found: {source}")

    if dest.exists() or dest.is_symlink():
        if dest.is_symlink() and dest.resolve() == source.resolve():
            print(f"[ok] already linked: {dest} -> {source}")
            return
        if not force:
            raise FileExistsError(f"destination exists: {dest}")
        if dest.is_symlink() or dest.is_file():
            dest.unlink()
        else:
            shutil.rmtree(dest)

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.symlink_to(source, target_is_directory=source.is_dir())
    print(f"[link] {dest} -> {source}")


def mirror_audio_links(source_dir: Path, dest_dir: Path, force: bool) -> int:
    dest_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for audio_file in sorted(source_dir.iterdir()):
        if not audio_file.is_file() or audio_file.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        dest = dest_dir / audio_file.name
        if dest.exists() or dest.is_symlink():
            if dest.is_symlink() and dest.resolve() == audio_file.resolve():
                count += 1
                continue
            if not force:
                raise FileExistsError(f"destination exists: {dest}")
            dest.unlink()
        dest.symlink_to(audio_file)
        count += 1
    return count


def resolve_default_source(repo_root: Path) -> Path | None:
    candidates = [
        Path.home() / "datasets" / "mayuri-voice-dataset" / "wav",
        repo_root.parent / "mayuri_voice" / "data" / "raw" / "wav",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Link a local Mayuri dataset directory and mirror it into Applio's dataset layout."
    )
    parser.add_argument("--raw-source", type=Path, default=None, help="local WAV directory")
    parser.add_argument("--dataset-name", default="mayuri_rvc", help="Applio dataset name")
    parser.add_argument("--force", action="store_true", help="replace existing links")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    raw_source = args.raw_source or resolve_default_source(repo_root)
    if raw_source is None:
        print(
            "[error] no dataset directory found. Pass --raw-source /path/to/wav",
            file=sys.stderr,
        )
        return 1

    raw_dest = repo_root / "data" / "source" / "mayuri_speech_16k"
    applio_dataset_dir = repo_root / "third_party" / "Applio" / "assets" / "datasets" / args.dataset_name

    try:
        ensure_link(raw_source, raw_dest, args.force)
        count = mirror_audio_links(raw_source, applio_dataset_dir, args.force)
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print(f"[done] linked dataset source and mirrored {count} audio files into {applio_dataset_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
