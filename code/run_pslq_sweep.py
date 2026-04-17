from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from mpmath import mp, pslq

from pslq_templates import TEMPLATES, template_vector


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a PSLQ sweep on the certified stable prefix.")
    parser.add_argument("--input", default="artifacts/stable_prefix.json")
    parser.add_argument("--precision", type=int, default=300)
    parser.add_argument("--maxcoeff", type=int, default=1000)
    parser.add_argument("--maxsteps", type=int, default=10000)
    parser.add_argument("--residual-threshold", type=float, default=1e-20)
    parser.add_argument("--output", default="artifacts/status_blocks/pslq_attempts.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mp.dps = args.precision
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rows = payload.get("stable_rows", [])

    attempts = []
    status_counts: dict[str, int] = {}
    for row in rows:
        for template_id in TEMPLATES:
            vec = template_vector(row, template_id)
            start = time.perf_counter()
            try:
                rel = pslq(vec, maxcoeff=args.maxcoeff, maxsteps=args.maxsteps)
            except Exception as exc:
                rel = None
                error = str(exc)
            else:
                error = None

            residual = None
            status = "unsupported"
            coeffs = None
            if rel:
                coeffs = [int(c) for c in rel]
                residual = abs(sum(mp.mpf(c) * v for c, v in zip(coeffs, vec)))
                if residual <= args.residual_threshold:
                    status = "verified"

            status_counts[status] = status_counts.get(status, 0) + 1
            attempts.append(
                {
                    "n": int(row["n"]),
                    "template_id": template_id,
                    "coord_indices": list(TEMPLATES[template_id].indices),
                    "coords": row["coords"],
                    "coeffs": coeffs,
                    "residual": None if residual is None else mp.nstr(residual, 30),
                    "status": status,
                    "elapsed_seconds": round(time.perf_counter() - start, 6),
                    "error": error,
                }
            )

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_payload = {
        "metadata": {
            "precision": args.precision,
            "maxcoeff": args.maxcoeff,
            "maxsteps": args.maxsteps,
            "residual_threshold": args.residual_threshold,
            "stable_count": len(rows),
            "template_count": len(TEMPLATES),
        },
        "status_counts": status_counts,
        "attempts": attempts,
    }
    out_path.write_text(json.dumps(out_payload, indent=2), encoding="utf-8")
    print({"output": str(out_path), "status_counts": status_counts, "attempts": len(attempts)})


if __name__ == "__main__":
    main()
