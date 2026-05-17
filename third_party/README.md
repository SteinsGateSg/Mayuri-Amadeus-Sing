# Third-Party Tools

This release keeps a stripped `Applio 3.5.1` source tree in `third_party/Applio/`.

What was removed:

- downloaded prerequisite weights
- runtime `logs/`
- cached datasets and generated audios
- nested git metadata

Expected behavior:

- `scripts/install_backend_deps.sh` installs Python dependencies
- `scripts/run_applio.sh` prepares the bundled demo model inside `third_party/Applio/logs/`
- missing backend prerequisites are downloaded at runtime by Applio when needed
