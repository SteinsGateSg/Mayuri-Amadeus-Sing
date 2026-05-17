#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


HF_DATASET_URL = "https://huggingface.co/datasets/SteinsGateSg/mayuri-voice-dataset"


def run(cmd: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return 127, ""
    return proc.returncode, proc.stdout.strip()


def check_tool(name: str) -> dict[str, str | bool | None]:
    path = shutil.which(name)
    return {"present": bool(path), "path": path}


def probe_gpu() -> dict[str, object]:
    code, out = run(
        [
            "nvidia-smi",
            "--query-gpu=name,driver_version,memory.total",
            "--format=csv,noheader",
        ]
    )
    if code != 0 or not out:
        return {"present": False, "info": []}
    return {"present": True, "info": out.splitlines()}


def build_report(repo_root: Path) -> dict[str, object]:
    model_dir = repo_root / "models" / "mayuri_rvc_v1"
    applio_dir = repo_root / "third_party" / "Applio"
    dataset_link = repo_root / "data" / "source" / "mayuri_speech_16k"
    demo_audio_dir = repo_root / "docs" / "assets" / "audio"

    return {
        "repo_root": str(repo_root),
        "python": sys.version.split()[0],
        "hf_dataset": HF_DATASET_URL,
        "tools": {
            "git": check_tool("git"),
            "python3": check_tool("python3"),
            "ffmpeg": check_tool("ffmpeg"),
            "conda": check_tool("conda"),
            "nvidia-smi": check_tool("nvidia-smi"),
        },
        "gpu": probe_gpu(),
        "paths": {
            "applio_dir": str(applio_dir),
            "model_dir": str(model_dir),
            "dataset_link": str(dataset_link),
            "music_placeholder": str(repo_root / "Music"),
            "demo_audio_dir": str(demo_audio_dir),
        },
        "status": {
            "applio_present": applio_dir.exists(),
            "demo_model_present": (model_dir / "mayuri_rvc_v1_200e_55200s.pth").exists(),
            "demo_index_present": (model_dir / "mayuri_rvc_v1.index").exists(),
            "dataset_link_present": dataset_link.exists(),
            "music_placeholder_present": (repo_root / "Music").exists(),
            "demo_audio_present": all(
                [
                    (demo_audio_dir / "sirius_mayuri_vocal.mp3").exists(),
                    (demo_audio_dir / "sirius_mayuri_full.mp3").exists(),
                ]
            ),
        },
    }


def print_human(report: dict[str, object]) -> None:
    print("== Mayuri-Amadeus-Sing Release Doctor ==")
    print(f"repo_root: {report['repo_root']}")
    print(f"python: {report['python']}")
    print(f"hf_dataset: {report['hf_dataset']}")

    print("\n[tools]")
    for name, info in report["tools"].items():
        state = "ok" if info["present"] else "missing"
        print(f"- {name}: {state} {info['path'] or ''}".rstrip())

    print("\n[gpu]")
    gpu = report["gpu"]
    if gpu["present"]:
        for line in gpu["info"]:
            print(f"- {line}")
    else:
        print("- not detected")

    print("\n[release assets]")
    status = report["status"]
    print(f"- applio_present: {status['applio_present']}")
    print(f"- demo_model_present: {status['demo_model_present']}")
    print(f"- demo_index_present: {status['demo_index_present']}")
    print(f"- demo_audio_present: {status['demo_audio_present']}")
    print(f"- music_placeholder_present: {status['music_placeholder_present']}")
    print(f"- dataset_link_present: {status['dataset_link_present']}")

    print("\n[next step]")
    if not status["dataset_link_present"]:
        print("- download the HF dataset and run scripts/link_existing_dataset.py --raw-source /path/to/wav")
    else:
        print("- dataset link is ready for local training")
    print("- run bash scripts/run_applio.sh to expose the demo model in the UI")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check release-repo prerequisites and bundled assets.")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    report = build_report(repo_root)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
