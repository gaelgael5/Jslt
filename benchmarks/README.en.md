# Benchmarks (performance)

Scripts measuring the engine's throughput. **Outside the test suite** (`pytest`
does not collect them): they do not run in CI, you launch them by hand.

```bash
pip install -e "packages/urban-json[dev]"
python benchmarks/bench_transform.py                 # default sizes
python benchmarks/bench_transform.py --size 50000 --repeats 9
```

## `bench_transform.py`

Compares, on “bulk import” scenarios (large arrays through a `$source` loop,
with operators, casts and `when`), the **AST interpreter** against the
**compiled path** (`JsltTemplate.build()`). The template is parsed once, then
applied N times; the benchmark reports the median of each path, the speed-up
factor, and the throughput (items/s) of the compiled path. Before measuring, it
checks that **both paths produce an identical result** (compilation is proven
equivalent, not merely faster).

The figures are **machine-relative**: they are there to compare the two paths
with each other, not to give an absolute value. Observed order of magnitude:
**×3 to ×5** depending on the template (the gain peaks on `$.x` field accesses,
which dominate imports).
