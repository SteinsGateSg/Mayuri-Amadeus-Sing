<div align="center">

  <img src="docs/assets/hero/mayuri-sirius-hero.png" alt="Mayuri-Amadeus-Sing hero artwork" width="100%" />

  <h1>Mayuri-Amadeus-Sing</h1>

  <p><em>A moonlit singing voice conversion framework for Mayuri-style AI covers.</em></p>

  <p>
    <a href="https://steinsgatesg.github.io/Mayuri-Amadeus-Sing/">
      <img alt="Project Page" src="https://img.shields.io/badge/✦%20Project%20Page-Moonlit%20Showcase-44556B?style=for-the-badge&logo=githubpages&logoColor=F6F1E8" />
    </a>
    <a href="https://github.com/SteinsGateSg/Mayuri-Amadeus-Sing">
      <img alt="GitHub Repository" src="https://img.shields.io/badge/☾%20GitHub-SteinsGateSg%2FMayuri--Amadeus--Sing-2A3140?style=for-the-badge&logo=github&logoColor=F6F1E8" />
    </a>
    <a href="https://huggingface.co/datasets/SteinsGateSg/mayuri-voice-dataset">
      <img alt="Dataset on Hugging Face" src="https://img.shields.io/badge/❖%20Dataset-Mayuri%20Voice%20Archive-CF9F55?style=for-the-badge&logo=huggingface&logoColor=1A1410" />
    </a>
  </p>

</div>

`Mayuri-Amadeus-Sing` is a focused singing voice conversion workspace for building Shiina Mayuri AI covers.

The repository is organized as a reusable training/inference framework with one concrete example:

- target character: `Shiina Mayuri`
- backend family: `RVC`
- reference implementation: stripped `Applio 3.5.1`
- example song case: `シリウスの心臓 / Sirius no Shinzou`

This release does **not** ship the raw training dataset or the source song stems.

## What Is Included

- release-ready training/inference scripts
- a stripped `Applio` backend tree without downloaded runtime weights
- one demo Mayuri model pair:
  - `models/mayuri_rvc_v1/mayuri_rvc_v1_200e_55200s.pth`
  - `models/mayuri_rvc_v1/mayuri_rvc_v1.index`
- demo audio for the Sirius example:
  - converted full vocal
  - aligned full mix
- a static project page in `docs/`

## What Is Not Included

- raw local speech WAVs
- the original song vocal/instrumental stems
- training cache, extracted features, TensorBoard logs, intermediate checkpoints
- downloaded `Applio` prerequisite weights

Dataset download:

- https://huggingface.co/datasets/SteinsGateSg/mayuri-voice-dataset

## Demo

Project page:

- [Moonlit Showcase](https://steinsgatesg.github.io/Mayuri-Amadeus-Sing/)

Direct demo files:

- vocal only: [docs/assets/audio/sirius_mayuri_vocal.mp3](docs/assets/audio/sirius_mayuri_vocal.mp3)
- full mix: [docs/assets/audio/sirius_mayuri_full.mp3](docs/assets/audio/sirius_mayuri_full.mp3)

## Quick Start

### 1. Create an environment

```bash
bash scripts/bootstrap_env.sh
```

### 2. Install backend dependencies

```bash
bash scripts/install_backend_deps.sh
```

### 3. Check local readiness

```bash
python scripts/doctor.py
```

### 4. Link a local copy of the dataset

After downloading the dataset from Hugging Face, point this repo at your local WAV folder:

```bash
python scripts/link_existing_dataset.py --raw-source /path/to/mayuri-voice-dataset/wav
```

This also mirrors file-level symlinks into `third_party/Applio/assets/datasets/mayuri_rvc/`, which is the layout Applio expects for training.

### 5. Launch the UI

```bash
bash scripts/run_applio.sh
```

The launcher will:

- sanitize localhost proxy variables
- expose the bundled demo model in Applio's `logs/` directory
- fetch Applio runtime prerequisite weights on first run
- start the local web UI

## Training Path

Recommended first-pass training settings:

- dataset path: `assets/datasets/mayuri_rvc`
- sample rate: `32000`
- pitch extractor: `rmvpe`
- embedder: `contentvec`
- batch size: `4`
- total epoch: `200`

Detailed notes:

- [docs/toolchain-decision.md](docs/toolchain-decision.md)
- [docs/mvp-plan.md](docs/mvp-plan.md)

## Inference Path

For the included demo model, a strong baseline is:

- pitch: `0`
- search feature ratio: `0.85`
- protect: `0.40`
- f0 method: `rmvpe`
- embedder: `contentvec`

For quick A/B inference sweeps:

```bash
python scripts/run_infer_sweep.py --input /path/to/guide_vocal.wav
```

The first UI launch or first CLI inference may download Applio runtime prerequisites such as `rmvpe.pt` and `contentvec`.

## Repository Layout

```text
Mayuri-Amadeus-Sing/
  Music/                     # placeholder only, no source stems shipped
  configs/
  data/
    source/                  # optional local dataset links
  docs/
    index.html               # project page
    assets/audio/            # publishable demo audio
  inputs/                    # user-provided guide vocals / instrumentals
  models/
    mayuri_rvc_v1/           # kept demo model + index
  scripts/
  third_party/
    Applio/                  # stripped backend source tree
```

## Notes

- The bundled model is included for reproducible demo inference, not as a claim of final-quality singing identity.
- The Mayuri dataset linked above remains the canonical raw data source.
- `Music/` is kept as a placeholder only. Source song materials are intentionally not redistributed in this repo.
