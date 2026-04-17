# AEAL methodology

This repository follows an Agent Epistemic Accountability Layer workflow.

## Core principle

Every manuscript-level statement must be backed by auditable artifacts generated from deterministic code paths or independently re-runnable computations.

## Relay-chain summary

1. Numerical generation of continued-fraction partial quotients for the target constant
2. Multi-precision stability check at 256, 512, and 1024 bits
3. Construction of a certified stable prefix and coordinate vectors
4. Conservative PSLQ sweep with small coefficient cap
5. Wide-cap diagnostic comparison for artefact analysis
6. Status-block generation linking counts, figures, and manuscript claims

## Evidence chain

- code/ contains the executable workflow
- artifacts/ stores JSON outputs and diagnostic logs
- paper/ contains the note and figures derived from those outputs
- aeal/provenance_manifest.json maps claims back to source artifacts

## Accountability rule

No claim of success, failure, or discovery is included in the manuscript unless it is supported by a fresh build or saved artifact with matching counts.
