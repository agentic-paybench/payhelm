"""MockBench CLI.

    python -m paybench.mockbench.cli generate   # gen fixtures + write provenance hashes
    python -m paybench.mockbench.cli run         # run the finality benchmark
    python -m paybench.mockbench.cli verify       # re-verify fixture hashes vs provenance
    python -m paybench.mockbench.cli all          # generate then run

Every subcommand takes ``--dimension {finality,auth-latency}`` (default
``finality``). The default reproduces the original, frozen settlement-finality
behaviour exactly (5 rails → 10 pairs → 5,000 trials, run_hash unchanged); the
``auth-latency`` dimension exercises the 6-rail (AP2 debuts) → 15-pair benchmark
over PLACEHOLDER calibration (§8 Resolution B; §11 Day-30).
"""

from __future__ import annotations

import argparse
import re
import sys

from .bench import run_benchmark, write_report
from .dimensions import DIMENSIONS, FINALITY, Dimension, get_dimension
from .fixtures import generate_fixture, load_fixture


def cmd_generate(ns: argparse.Namespace) -> int:
    dim: Dimension = get_dimension(ns.dimension)
    print(f"Generating calibrated log-normal {dim.name} fixtures (seeded)...\n")
    for rail in dim.rails:
        gf = generate_fixture(rail, dim)
        flag = "updated" if gf.provenance_updated else "unchanged"
        print(
            f"  {rail:<4} median={gf.median_s:<6} sigma_log={gf.sigma_log:<6} "
            f"n={gf.n_samples}  {gf.hash}  (provenance {flag})"
        )
    print("\nDone. Provenance fixture_content_hash fields written.")
    return 0


def cmd_verify(ns: argparse.Namespace) -> int:
    dim: Dimension = get_dimension(ns.dimension)
    ok = True
    hash_re = re.compile(r'fixture_content_hash:\s*"(.*?)"')
    for rail in dim.rails:
        try:
            obj = load_fixture(rail, dim)  # raises on hash mismatch
        except (FileNotFoundError, ValueError) as exc:
            print(f"  {rail:<4} FAIL  {exc}")
            ok = False
            continue
        prov_text = dim.provenance_path(rail).read_text(encoding="utf-8")
        m = hash_re.search(prov_text)
        prov_hash = m.group(1) if m else ""
        match = prov_hash == obj["content_hash"]
        ok = ok and match
        status = "OK  " if match else "FAIL"
        print(f"  {rail:<4} {status} fixture={obj['content_hash']}  provenance={'match' if match else prov_hash or '(empty)'}")
    print("\nAll fixtures verified." if ok else "\nVERIFICATION FAILED.")
    return 0 if ok else 1


def cmd_run(ns: argparse.Namespace) -> int:
    dim: Dimension = get_dimension(ns.dimension)
    report = run_benchmark(dim)
    path = write_report(report, dim)
    cfg = report["config"]
    bt = report["bradley_terry"]
    k_grid = cfg["k_grid_seconds"]

    print(f"PayBench — {dim.name} benchmark")
    print(
        f"  {cfg['n_pairs']} pairs x {cfg['trials_per_pair']} trials "
        f"= {cfg['total_trials']} trials   seed={cfg['master_seed']}"
    )
    print(f"  run_hash {report['run_hash']}\n")

    print(f"Bradley-Terry strength (lowest-{dim.unit} first):")
    for rank, rail in enumerate(bt["ranking"], 1):
        name = cfg["rail_names"][rail]
        print(f"  {rank}. {rail:<4} {bt['strengths'][rail]:.4f}  {name}")
    print(f"  (converged={bt['converged']} in {bt['iterations']} iters)\n")

    print(f"pass@k = P({dim.name} <= k {dim.unit})  [Wilson 95% lower bound in brackets]")
    header = "  rail  " + "  ".join(f"k={k:<4g}" for k in k_grid)
    print(header)
    for rail in cfg["rails"]:
        cells = []
        for row in report["pass_at_k"][rail]:
            cells.append(f"{row['phat']:.2f}[{row['wilson_lb']:.2f}]")
        print(f"  {rail:<4}  " + "  ".join(cells))
    print(f"\nReport written: {path}")
    return 0


def cmd_all(ns: argparse.Namespace) -> int:
    rc = cmd_generate(ns)
    if rc != 0:
        return rc
    print()
    return cmd_run(ns)


def _add_dimension_arg(p: argparse.ArgumentParser) -> None:
    # Keep the parsed value a plain string (choices-checked) and resolve it to a
    # Dimension at use; combining choices= with a type= that returns an object
    # breaks argparse's post-conversion choices comparison.
    p.add_argument(
        "--dimension",
        "-d",
        choices=sorted(DIMENSIONS),
        default=FINALITY.key,
        help="benchmark dimension (default: finality)",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="paybench-mockbench", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    specs = [
        ("generate", "generate fixtures + write provenance hashes", cmd_generate),
        ("verify", "re-verify fixture hashes vs provenance", cmd_verify),
        ("run", "run the benchmark", cmd_run),
        ("all", "generate then run", cmd_all),
    ]
    for cmd_name, help_text, func in specs:
        sp = sub.add_parser(cmd_name, help=help_text)
        _add_dimension_arg(sp)
        sp.set_defaults(func=func)
    ns = parser.parse_args(argv)
    return ns.func(ns)


if __name__ == "__main__":
    sys.exit(main())
