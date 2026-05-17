# Data Notes

Raw training audio is intentionally not committed here.

Canonical dataset:

- https://huggingface.co/datasets/SteinsGateSg/mayuri-voice-dataset

Expected workflow:

1. download the dataset locally
2. point `scripts/link_existing_dataset.py` at the local `wav/` directory
3. let the script create:
   - `data/source/mayuri_speech_16k`
   - `third_party/Applio/assets/datasets/mayuri_rvc`

This keeps the repo publishable while still supporting local training.
