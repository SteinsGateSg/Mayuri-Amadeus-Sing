#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APPLIO_DIR="${REPO_ROOT}/third_party/Applio"
ENV_NAME="${1:-mayuri-sing}"

if ! command -v conda >/dev/null 2>&1; then
  echo "conda not found in PATH"
  exit 1
fi

if [[ ! -d "${APPLIO_DIR}" ]]; then
  echo "Applio source tree not found at ${APPLIO_DIR}"
  exit 1
fi

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "${ENV_NAME}"

conda install -n "${ENV_NAME}" -c conda-forge portaudio -y
python -m pip install -U pip wheel "setuptools<81"
python -m pip install -r "${APPLIO_DIR}/requirements.txt" --extra-index-url https://download.pytorch.org/whl/cu128
python -m pip install "setuptools<81"

echo "Backend dependencies installed for env '${ENV_NAME}'."
