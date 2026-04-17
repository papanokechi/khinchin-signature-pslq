from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from mpmath import mp


CONSTANTS = {
    "pi": lambda: mp.pi,
    "e": lambda: mp.e,
    "ln2": lambda: mp.log(2),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute Khinchin-signature prefix statistics.")
    parser.add_argument("--constant", choices=sorted(CONSTANTS), default="pi")
    parser.add_argument("--n", type=int, default=1000, help="Number of continued-fraction partial quotients to extract.")
    parser.add_argument("--dps", type=int, default=256, help="Working decimal precision for mpmath.")
    parser.add_argument(
        "--outdir",
        default="artifacts",
        help="Output directory for JSON and CSV files.",
    )
    return parser.parse_args()


def partial_quotients_for_fractional_part(x: mp.mpf, n: int) -> list[int]:
    x = mp.frac(x)
    out: list[int] = []
    for _ in range(n):
        if x == 0:
            break
        a = int(mp.floor(1 / x))
        out.append(a)
        x = (1 / x) - a
    return out


def build_rows(terms: list[int]) -> list[dict]:
    rows = []
    log_sum = mp.mpf("0")
    for n, a in enumerate(terms, start=1):
        log_sum += mp.log(a)
        s_n = mp.e ** (log_sum / n)
        rows.append(
            {
                "n": n,
                "a_n": int(a),
                "S_n": mp.nstr(s_n, 50),
                "log_S_n": mp.nstr(mp.log(s_n), 50),
            }
        )
    return rows


def write_outputs(rows: list[dict], constant_name: str, dps: int, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    stem = f"{constant_name}_n{len(rows)}_p{dps}"

    payload = {
        "metadata": {
            "constant": constant_name,
            "n_terms": len(rows),
            "dps": dps,
            "statistic": "S_n = exp((1/n) * sum(log(a_k)))",
        },
        "rows": rows,
    }

    (outdir / f"{stem}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with open(outdir / f"{stem}.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["n", "a_n", "S_n", "log_S_n"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    mp.dps = args.dps
    constant = CONSTANTS[args.constant]()
    terms = partial_quotients_for_fractional_part(constant, args.n)
    rows = build_rows(terms)
    write_outputs(rows, args.constant, args.dps, Path(args.outdir))
    print({"constant": args.constant, "rows": len(rows), "dps": args.dps, "outdir": str(Path(args.outdir))})


if __name__ == "__main__":
    main()
