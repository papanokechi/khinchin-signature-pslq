# Agent G residual analysis

## Status block

### Conservative masked run

- T1_L_LminusK_logn: unsupported = 91
- T2_L_LminusK_logL: unsupported = 91
- T3_L_logL_logn: unsupported = 91
- T4_LminusK_logL_n: unsupported = 91
- T5_L_logL_LminusK: unsupported = 91
- T7_full4: unsupported = 91

### Wide-cap non-unsupported counts

- T1_L_LminusK_logn: 0
- T2_L_LminusK_logL: 0
- T3_L_logL_logn: 1
- T4_LminusK_logL_n: 0
- T5_L_logL_LminusK: 0
- T7_full4: 90

## 1) Current numeric status

- Conservative file total attempts: 546
- Overall conservative status counts: unsupported = 546
- The baseline null is uniform across all six templates.
- In the conservative file, no attempt produced a retained residual payload; nonnull residual count is zero and estimated digit strength stays at 0.0 throughout. Structurally, this means the small-coefficient search did not even enter a credible near-miss regime on the stability-certified prefix.

From the mask:
- input precisions: 256, 512, 1024
- shared indices: 10000
- stable_count: 91
- stable_prefix_end: 91
- accepted range: n = 1 to 91

## 2) High-cap artefact characterization

### T3_L_logL_logn

- non-unsupported attempts: 1
- minimum max coefficient: 968826
- median max coefficient: 968826
- example: n = 33, coeffs = [424269, 968826, -743242], residual = 0.0

### T7_full4

- non-unsupported attempts: 90
- minimum max coefficient: 43197
- median max coefficient: 173198.5
- smallest-coefficient examples:
  - n = 41, coeffs = [43197, 7010, -40887, -33583], residual = 0.0
  - n = 55, coeffs = [44044, -27912, -499, -24449], residual = 0.0
  - n = 19, coeffs = [2018, 38062, 52051, -12855], residual = 0.0

Interpretation: apparent hits emerge only once the coefficient ceiling is loosened dramatically; they disappear completely when the cap is reduced to 1000. This strongly supports treating them as exploratory numerical fits rather than meaningful arithmetic structure.

## 3) Recommended figures

1. Conservative status-by-template bar chart
   - source: conservative file only
   - x = template_id, y = count, stack = status
   - purpose: show the clean null baseline

2. Conservative vs wide-cap comparison bars
   - source: conservative and wide-cap files
   - x = template_id, y = count(status != unsupported), grouped by run type
   - purpose: show that hits appear only under relaxed caps

3. n vs max coefficient scatter for wide-cap artefacts
   - source: wide-cap file only
   - x = n, y = max(abs(coeffs)), color = template_id
   - purpose: show the large-coefficient nature of all artefacts

4. Stability-mask profile
   - source: mask file only
   - x = n, y = diff_L_256_512 and diff_L_512_1024
   - purpose: justify the cutoff to the stable prefix n <= 91

## 4) Experimental-results note

Using the 256-, 512-, and 1024-precision pi runs, we restricted the PSLQ study to the contiguous stability-certified prefix n <= 91, where both L_n and S_n agree across precisions at the 1e-20 tolerance level. On this stabilized dataset we executed six 3D and 4D coordinate templates at 300-digit working precision with 600-digit confirmation. Under the conservative coefficient cap maxcoeff = 1000, all 546 attempts were unsupported, giving a clean null result for the tested template family. A wider exploratory pass with maxcoeff = 1e6 did produce nominal hits, but only at very large integer coefficients; these vanished completely when the cap was tightened back to the conservative setting. Accordingly, we treat the wide-cap outputs as diagnostic artefacts rather than genuine relations. The next clear step is to preserve this as a high-quality null result and then extend the masked workflow to different constants or enriched coordinate families.
