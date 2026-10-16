#!/usr/bin/env python3
"""Banc d'essai de performance — urban-json.

Mesure le débit de ``JsltTemplate.transform`` sur des scénarios orientés
« import en masse » (grands tableaux via boucle ``$source``, avec opérateurs,
casts, conditions). Le template est analysé une fois puis réappliqué N fois.

Usage :
    python benchmarks/bench_transform.py              # tailles par défaut
    python benchmarks/bench_transform.py --size 50000 --repeats 9

Objectif : établir une ligne de base de l'interpréteur d'AST actuel, et servir
de référence comparative pour le futur chemin *compilé* (``JsltTemplate.build``).
Quand la compilation existera, ce même banc exécutera les deux chemins côte à
côte et vérifiera l'égalité des résultats (voir ``benchmarks/README.md``).
"""
from __future__ import annotations

import argparse
import statistics
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from urban_json import JsltTemplate

# --- scénarios -------------------------------------------------------------

SIMPLE = '[ { "$source": $.items, "id": $.id, "name": $.name } ]'

TYPED = (
    '[ { "$source": $.items,'
    '    "id": $.id #integer,'
    '    "name": $.name,'
    '    "total": $.a + $.b,'
    '    "flag": when($.a > $.b) { "true": "hi", "default": "lo" } } ]'
)

NESTED = (
    '[ { "$source": $.groups,'
    '    "g": $.key,'
    '    "rows": [ { "$source": $.items, "v": $.v, "double": $.v + $.v } ] } ]'
)


def make_items(n: int) -> dict[str, Any]:
    return {"items": [{"id": str(i), "name": f"n{i}", "a": i, "b": n - i}
                      for i in range(n)]}


def make_groups(ng: int, ni: int) -> dict[str, Any]:
    return {"groups": [{"key": f"g{g}", "items": [{"v": g * ni + i} for i in range(ni)]}
                       for g in range(ng)]}


@dataclass
class Scenario:
    label: str
    template: str
    document: Any
    out_count: int  # nombre d'éléments produits (pour le débit)


def build_scenarios(size: int) -> list[Scenario]:
    ng = max(1, size // 100)
    return [
        Scenario(f"simple ({size:,})", SIMPLE, make_items(size), size),
        Scenario(f"typé + when + cast ({size:,})", TYPED, make_items(size), size),
        Scenario(f"imbriqué ({ng}x100)", NESTED, make_groups(ng, 100), ng * 100),
    ]


# --- mesure ----------------------------------------------------------------

@dataclass
class Result:
    label: str
    parse_ms: float
    transform_ms: float  # médiane
    throughput: float     # éléments/s


def time_median(fn: Callable[[], Any], repeats: int) -> float:
    fn()  # warmup
    times = []
    for _ in range(repeats):
        t = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t)
    return statistics.median(times)


def run_scenario(sc: Scenario, repeats: int) -> Result:
    t0 = time.perf_counter()
    tpl = JsltTemplate.parse(sc.template)
    parse_ms = (time.perf_counter() - t0) * 1000
    med = time_median(lambda: tpl.transform(sc.document), repeats)
    thr = sc.out_count / med if med else float("inf")
    return Result(sc.label, parse_ms, med * 1000, thr)


def print_table(results: list[Result]) -> None:
    w = max(len(r.label) for r in results)
    print(f"{'scénario':<{w}}  {'parse':>9}  {'transform(méd)':>15}  {'débit':>18}")
    print("-" * (w + 9 + 15 + 18 + 6))
    for r in results:
        print(f"{r.label:<{w}}  {r.parse_ms:7.2f}ms  {r.transform_ms:13.2f}ms  "
              f"{r.throughput:12,.0f} it/s")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--size", type=int, default=20_000,
                    help="nombre d'éléments par scénario (défaut 20000)")
    ap.add_argument("--repeats", type=int, default=7,
                    help="nombre de mesures (médiane) (défaut 7)")
    args = ap.parse_args()

    print("=== urban-json — banc d'essai transform (interpréteur) ===")
    print(f"taille={args.size:,}  répétitions={args.repeats}\n")
    results = [run_scenario(sc, args.repeats) for sc in build_scenarios(args.size)]
    print_table(results)


if __name__ == "__main__":
    main()
