#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


PRESETS = [
    {
        "name": "e200_ir075_p033",
        "checkpoint": "mayuri_rvc_v1_200e_55200s.pth",
        "index_rate": 0.75,
        "protect": 0.33,
    },
    {
        "name": "e200_ir085_p040",
        "checkpoint": "mayuri_rvc_v1_200e_55200s.pth",
        "index_rate": 0.85,
        "protect": 0.40,
    },
    {
        "name": "e200_ir090_p045",
        "checkpoint": "mayuri_rvc_v1_200e_55200s.pth",
        "index_rate": 0.90,
        "protect": 0.45,
    },
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a small Mayuri RVC inference sweep to compare identity-focused presets."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="input guide vocal wav",
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=None,
        help="index file; defaults to models/mayuri_rvc_v1/mayuri_rvc_v1.index",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="directory for sweep outputs; defaults to outputs/infer_sweeps/latest",
    )
    parser.add_argument(
        "--preset",
        action="append",
        default=[],
        help="run only the named preset(s); may be repeated",
    )
    return parser


def select_presets(names: list[str]) -> list[dict[str, object]]:
    if not names:
        return PRESETS

    selected = []
    available = {preset["name"]: preset for preset in PRESETS}
    for name in names:
        if name not in available:
            raise KeyError(f"unknown preset: {name}")
        selected.append(available[name])
    return selected


def main() -> int:
    args = build_parser().parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    applio_dir = repo_root / "third_party" / "Applio"
    model_dir = repo_root / "models" / "mayuri_rvc_v1"
    input_path = args.input.expanduser().resolve() if args.input is not None else None
    index_path = (args.index.expanduser().resolve() if args.index is not None else (model_dir / "mayuri_rvc_v1.index")).resolve()
    output_dir = (args.output_dir or (repo_root / "outputs" / "infer_sweeps" / "latest")).resolve()

    if input_path is None:
        print("[error] missing --input /path/to/guide_vocal.wav", file=sys.stderr)
        return 1
    if not input_path.exists():
        print(
            f"[error] input not found: {input_path}. Pass --input /path/to/guide_vocal.wav",
            file=sys.stderr,
        )
        return 1
    if not index_path.exists():
        print(f"[error] index not found: {index_path}", file=sys.stderr)
        return 1
    if not applio_dir.exists():
        print(f"[error] Applio not found: {applio_dir}", file=sys.stderr)
        return 1

    selected = select_presets(args.preset)
    output_dir.mkdir(parents=True, exist_ok=True)

    prepare_script = repo_root / "scripts" / "prepare_applio_runtime.py"
    subprocess.run([sys.executable, str(prepare_script)], check=True)

    os.chdir(applio_dir)
    sys.path.insert(0, str(applio_dir))

    from core import run_infer_script  # noqa: PLC0415

    summary: list[dict[str, object]] = []
    failures = 0

    for preset in selected:
        checkpoint = (model_dir / str(preset["checkpoint"])).resolve()
        if not checkpoint.exists():
            print(f"[skip] missing checkpoint: {checkpoint}")
            continue

        output_path = output_dir / f"{preset['name']}.wav"
        if output_path.exists():
            output_path.unlink()
        print(
            f"[run] {preset['name']} checkpoint={checkpoint.name} "
            f"index_rate={preset['index_rate']} protect={preset['protect']}"
        )
        status, exported = run_infer_script(
            pitch=0,
            index_rate=float(preset["index_rate"]),
            volume_envelope=1.0,
            protect=float(preset["protect"]),
            f0_method="rmvpe",
            input_path=str(input_path),
            output_path=str(output_path),
            pth_path=str(checkpoint),
            index_path=str(index_path),
            split_audio=False,
            f0_autotune=False,
            f0_autotune_strength=0.0,
            proposed_pitch=False,
            proposed_pitch_threshold=0.0,
            clean_audio=False,
            clean_strength=0.5,
            export_format="WAV",
            embedder_model="contentvec",
            embedder_model_custom=None,
            formant_shifting=False,
            post_process=False,
            sid=0,
        )
        ok = output_path.exists() and output_path.stat().st_size > 0
        if not ok:
            failures += 1
        summary.append(
            {
                "preset": preset["name"],
                "checkpoint": checkpoint.name,
                "index_rate": preset["index_rate"],
                "protect": preset["protect"],
                "ok": ok,
                "status": status,
                "output": exported,
            }
        )

    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[done] wrote {summary_path}")
    for item in summary:
        marker = "ok" if item["ok"] else "failed"
        print(f"- {item['preset']} [{marker}]: {item['output']}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
