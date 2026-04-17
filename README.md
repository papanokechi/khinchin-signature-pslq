# Khinchin-Signature PSLQ: A Precision-Controlled Null Result

This repository contains the reproducible computational experiments, PSLQ searches, stability masking, and diagnostic analyses supporting the paper *A Precision-Controlled Null Result for a Khinchin-Signature PSLQ Family*. All numerical results, figures, and audit artifacts are generated from the code and data in this repository.

## Repository Contents

- **paper/** — Manuscript (TeX + PDF), figures, and references  
- **code/** — Reproducible Python scripts for prefix stabilization, PSLQ sweeps, and diagnostics  
- **artifacts/** — Stable prefix, masks, residual logs, status-block JSON files, and wide-cap diagnostics  
- **aeal/** — Epistemic accountability layer: methodology, verification log, and provenance manifest  

## Reproducibility

To reproduce the main results:

1. Install dependencies from [code/environment.yml](code/environment.yml)
2. Regenerate the stabilized prefix:

   ```
   python code/compute_ln.py <paths-to-saved-runs> --out artifacts/stable_prefix.json
   ```

3. Run the PSLQ sweep:

   ```
   python code/run_pslq_sweep.py --input artifacts/stable_prefix.json --output artifacts/status_blocks/pslq_attempts_reproduced.json
   ```

4. Regenerate figures using the scripts in [code/diagnostics](code/diagnostics)

All results in the paper were reproduced from this repository.

## AEAL Disclosure

This repository includes a complete epistemic audit trail:
- [aeal/methodology.md](aeal/methodology.md) — Description of the multi-agent workflow  
- [aeal/verification_log.md](aeal/verification_log.md) — Verification steps and outcomes  
- [aeal/provenance_manifest.json](aeal/provenance_manifest.json) — Code → artifact → claim mapping  

## Paper and Citation

The manuscript is located in [paper](paper).  
A citation block will be added once the DOI is minted.

## Public Repository

The latest version of this project is available at:  
**<INSERT_PUBLIC_GITHUB_URL_HERE>**
