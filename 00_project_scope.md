# Project Scope

## Title
Geometric De-entanglement and Information-Control Circuits in Large Language Models

## Core question
Can we design geometry-aware concept extraction and circuit-level interventions
that (1) produce disentangled control directions, and (2) reduce unstructured
leakage and steganographic capacity in LLMs without degrading language modeling
performance?

## Motivation and background
Recent work highlights three connected pathologies in current LLMs:

1. **Entangled concept directions.** Standard contrastive extraction produces
   concept directions that are heavily entangled. Nominally unrelated concepts
   like sentiment and country can have pairwise cosine similarity as high as
   ~0.98, so steering one silently steers the other.
2. **Induction heads are not the main leak source.** Induction heads account
   for ~65-72% of structured copying, but ablating them typically *increases*
   leakage and makes generation more repetitive and lower-entropy because MLP
   circuits and non-induction heads take over.
3. **The steg cliff.** Frontier LLMs do near-perfect acrostics (92-100%
   per-character), but almost any scheme requiring counting or long-range
   position tracking drops below ~31% accuracy. Blind detection of steganography
   by LLM-as-judge fails entirely.

These point to a deeper structural issue: we lack a **geometry-aware and
circuit-aware handle** on where concepts live, how they co-vary, and how
information is copied, leaked, or hidden inside the model. That makes both
alignment/steering and safety (leakage reduction, steg detection) ad hoc and
fragile.

## Primary research questions
1. **Geometric de-entanglement.** Can we specify a concept-direction extraction
   protocol that bounds pairwise cosine between unrelated concepts while
   preserving causal steering power on each concept?
2. **Information-control circuits.** Where does residual leakage live once
   induction heads are ablated? Can targeted MLP / non-induction-head
   interventions reduce leakage without hurting perplexity?
3. **Covert capacity under interventions.** Do geometric and circuit-level
   interventions that reduce leakage also reduce steganographic capacity, or
   do they shift covert capacity into harder-to-detect channels?
4. **Joint evaluation.** Is there a single evaluation suite that separates
   (a) intended steering effect, (b) collateral bleed-over, (c) leakage /
   copying, and (d) covert-channel capacity?

## Research assistants and workstreams
- **Alex (RA1)** — concept-direction geometry & disentanglement methods
  (contrastive extraction, orthogonalization / LEACE, SAE features,
  causal scrubbing).
- **Brent (RA2)** — circuit analysis: induction-head identification, path
  patching, MLP vs non-induction copying, leakage metrics.
- **Chris (RA3)** — steganography eval battery: acrostic, synonym-bit,
  positional, counting schemes; per-char / per-bit accuracy; LLM-as-judge
  and paraphrase-robust detectors.

## Shared project taxonomy (three primitives)
Every method proposal and every experimental result must name which
primitive(s) it touches and report collateral effects on the other two.

- **A. Concept geometry** — concept directions, pairwise-cosine entanglement,
  layer scope, steering fidelity.
- **B. Information-flow circuits** — induction heads, non-induction copying,
  leakage (token-level KL + n-gram overlap), path patching.
- **C. Covert-channel capacity** — steg schemes, per-char / per-bit accuracy,
  counting / positional cliffs, judge robustness under paraphrase.

## Deliverables
- `03_methods/methods_v1.md` and `methods_v2.md` per workstream.
- Reading queue: `04_related_work/reading_queue.md`.
- Meeting notes: `06_decisions/meeting_notes.md` (plus Google Docs copies).
- Paper draft v0.1 in Google Docs, with a local markdown snapshot
  (`paper_draft_v0.1.md`) checked in to `main`-adjacent scratch.
- Each RA maintains a phase intake log in `research-log/` on their branch.

## Working hypotheses
- Template randomization + orthogonalization-in-context (not just post-hoc
  orthogonal projection) is necessary to bring unrelated-concept cosines
  below a useful threshold.
- Post-induction-ablation leakage is concentrated in late-layer MLPs, not in
  non-induction attention heads; patching those MLPs will reduce leakage with
  small perplexity cost.
- Counting / positional steg cliffs are a capability limit, not an encoding-
  scheme limit — they will survive most detection-side interventions.
- Reductions in leakage (workstream B) will partially transfer to reductions in
  covert capacity (workstream C), but not for positional / counting schemes.

## Known risks and fragile assumptions
- Concept directions may not be layer-local; layer-scope has to be tested, not
  assumed (a planned clash between Alex and Brent).
- LLM-as-judge detection is known to collapse under paraphrase; Chris's battery
  must include paraphrase and format-perturbation adversaries.
- "Illustrative" experimental numbers in early phases are not load-bearing —
  only committed pilots with their seeds/configs are citable.
- `xoxp-` tokens live in `system_prompt_cursor/`; treat as sensitive. Do not
  commit those files to any public remote.

## Non-goals (for v0.1 paper)
- Full pretraining-scale interventions.
- Claims about internal cognition unsupported by intervention evidence.
- Productionizing any steering or detection tool.
- Touching domains outside LLM representation / circuit / steg analysis.
