from __future__ import annotations

from dataclasses import dataclass
from math import log
from typing import Iterable

from mpmath import mp

# Khinchin constant
K0 = mp.mpf("2.6854520010653064453097148354817956938203822939945")

COORD_NAMES = ["S_n", "log_S_n", "S_n_minus_K0", "log_n"]


@dataclass(frozen=True)
class TemplateSpec:
    name: str
    indices: tuple[int, ...]


TEMPLATES: dict[str, TemplateSpec] = {
    "T1_L_LminusK_logn": TemplateSpec("T1_L_LminusK_logn", (0, 2, 3)),
    "T2_L_LminusK_logL": TemplateSpec("T2_L_LminusK_logL", (0, 2, 1)),
    "T3_L_logL_logn": TemplateSpec("T3_L_logL_logn", (0, 1, 3)),
    "T4_LminusK_logL_n": TemplateSpec("T4_LminusK_logL_n", (2, 1, 3)),
    "T5_L_logL_LminusK": TemplateSpec("T5_L_logL_LminusK", (0, 1, 2)),
    "T7_full4": TemplateSpec("T7_full4", (0, 1, 2, 3)),
}


def coordinate_row(n: int, s_n: mp.mpf) -> list[mp.mpf]:
    """Return the four coordinates used in the PSLQ search."""
    return [
        mp.mpf(s_n),
        mp.log(s_n),
        mp.mpf(s_n) - K0,
        mp.log(n),
    ]


def row_to_jsonable(n: int, s_n: mp.mpf) -> dict:
    coords = coordinate_row(n, s_n)
    return {
        "n": int(n),
        "coord_names": COORD_NAMES,
        "coords": [mp.nstr(c, 50) for c in coords],
    }


def template_vector(row: dict, template_id: str) -> list[mp.mpf]:
    spec = TEMPLATES[template_id]
    coords = [mp.mpf(v) for v in row["coords"]]
    return [coords[i] for i in spec.indices]


def iter_template_rows(rows: Iterable[dict]):
    for row in rows:
        for template_id, spec in TEMPLATES.items():
            yield row["n"], template_id, spec.indices, template_vector(row, template_id)
