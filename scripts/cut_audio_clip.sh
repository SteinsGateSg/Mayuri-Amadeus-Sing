#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 4 ]]; then
  echo "usage: $0 <input-audio> <start-hh:mm:ss> <duration-sec> <output-audio>"
  exit 1
fi

INPUT="$1"
START="$2"
DURATION="$3"
OUTPUT="$4"

FFMPEG_BIN="${FFMPEG_BIN:-}"

if [[ -z "${FFMPEG_BIN}" ]]; then
  if command -v ffmpeg >/dev/null 2>&1; then
    FFMPEG_BIN="$(command -v ffmpeg)"
  else
    echo "ffmpeg not found. Set FFMPEG_BIN or install ffmpeg."
    exit 1
  fi
fi

mkdir -p "$(dirname "${OUTPUT}")"

"${FFMPEG_BIN}" -y \
  -ss "${START}" \
  -i "${INPUT}" \
  -t "${DURATION}" \
  -ac 1 \
  -ar 44100 \
  "${OUTPUT}"

echo "wrote ${OUTPUT}"
