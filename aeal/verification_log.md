# Verification log

## Fresh checks performed in this workspace

### 1. Stable-prefix regeneration
Command:

```powershell
python code/compute_ln.py results/khinchin_signature/pi_n10000_p256.json results/khinchin_signature/pi_n10000_p512.json results/khinchin_signature/pi_n10000_p1024.json --out artifacts/stable_prefix.json
```

Observed result:

- stable count: 91
- stable prefix end: 91

### 2. Reproduction smoke run for raw statistic generation
Command:

```powershell
python code/compute_sn.py --constant pi --n 64 --dps 128 --outdir artifacts/reference_runs
```

Observed result:

- 64 rows written successfully

### 3. Fresh conservative PSLQ sweep log
Command:

```powershell
python code/run_pslq_sweep.py --input artifacts/stable_prefix.json --output artifacts/status_blocks/pslq_attempts_reproduced.json --maxcoeff 1000 --precision 80
```

Observed result:

- attempts: 546
- status counts: unsupported = 546

### 4. Paper build verification
Command:

```powershell
cd paper
pdflatex -interaction=nonstopmode khinchin_signature_expmath_note.tex
pdflatex -interaction=nonstopmode khinchin_signature_expmath_note.tex
```

Observed result:

- PDF built successfully from the repository-local sources and figures

## Interpretation

These checks reproduce the repository's central null-result claims inside the local workspace and verify that the paper and artifact layout are self-contained.
