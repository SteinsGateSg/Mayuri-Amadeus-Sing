# MVP Plan

Goal: verify one short Japanese chorus with `guide vocal -> Mayuri timbre conversion`.

Recommended first-pass setup:

- guide vocal: clean solo vocal, `15-30 sec`
- training sample rate: `32000`
- pitch extractor: `rmvpe`
- embedder: `contentvec`
- batch size: `4`
- total epoch: `200`

Validation order:

1. confirm the guide vocal is clean and timing-stable
2. run dry vocal conversion first
3. only then create a mix with the instrumental

Success signal:

- melody and rhythm survive
- the converted voice is recognizably closer to Mayuri than the guide singer
- artifacts stay local instead of dominating the entire clip
