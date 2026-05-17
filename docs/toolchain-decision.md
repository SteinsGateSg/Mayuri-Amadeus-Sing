# Toolchain Decision

This release stays on the `RVC` family.

Chosen path:

- backend family: `RVC`
- frontend implementation: `Applio 3.5.1`
- demo training target: `Shiina Mayuri`

Why:

- guide-vocal cover workflows are the main goal here
- RVC remains the most practical route for small-to-medium character timbre experiments
- `so-vits-svc` mainline is archived and `so-vits-svc-fork` is no longer maintained

Repository policy:

- ship the backend source tree in stripped form
- do not ship downloaded backend prerequisites
- do not ship raw dataset WAVs
- keep one release-ready model + index for reproducible demo inference
