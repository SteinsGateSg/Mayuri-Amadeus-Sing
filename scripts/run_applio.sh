#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APPLIO_DIR="${REPO_ROOT}/third_party/Applio"
ENV_NAME="${1:-mayuri-sing}"
PORT="${APPLIO_PORT:-6969}"
SERVER_NAME="${APPLIO_SERVER_NAME:-127.0.0.1}"

if ! command -v conda >/dev/null 2>&1; then
  echo "conda not found in PATH"
  exit 1
fi

if [[ ! -d "${APPLIO_DIR}" ]]; then
  echo "Applio not found at ${APPLIO_DIR}"
  exit 1
fi

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "${ENV_NAME}"

python "${REPO_ROOT}/scripts/install_demo_model.py"
python "${REPO_ROOT}/scripts/prepare_applio_runtime.py"

# Gradio startup-events must hit localhost directly. If proxy vars are set and
# localhost is not exempted, Gradio can fail with 502 during startup.
export NO_PROXY="127.0.0.1,localhost,::1${NO_PROXY:+,${NO_PROXY}}"
export no_proxy="127.0.0.1,localhost,::1${no_proxy:+,${no_proxy}}"
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy

cd "${APPLIO_DIR}"
python -u app.py --server-name "${SERVER_NAME}" --port "${PORT}"
