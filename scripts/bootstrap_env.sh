#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="${1:-mayuri-sing}"

if ! command -v conda >/dev/null 2>&1; then
  echo "conda not found in PATH"
  exit 1
fi

source "$(conda info --base)/etc/profile.d/conda.sh"

if conda env list | awk '{print $1}' | grep -qx "${ENV_NAME}"; then
  echo "conda env '${ENV_NAME}' already exists"
else
  echo "creating conda env '${ENV_NAME}'"
  conda create -n "${ENV_NAME}" python=3.10 ffmpeg git pip portaudio -y
fi

conda activate "${ENV_NAME}"
python -m pip install -U pip wheel "setuptools<81" rich pyyaml soundfile librosa

cat <<'EOF'

Base environment is ready.

Recommended next steps:

  1. Install the vendored Applio backend dependencies:
     bash scripts/install_backend_deps.sh

  2. Link a local dataset copy:
     python scripts/link_existing_dataset.py --raw-source /path/to/wav

  3. Launch the UI:
     bash scripts/run_applio.sh

This script intentionally creates only the base environment.
The backend dependency install is separated so the repo can stay lightweight and publishable.
Keep `setuptools<81` for the Applio 3.5.1 path because `webrtcvad` still imports `pkg_resources`.
EOF
