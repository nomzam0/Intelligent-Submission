"""Benchmark end-to-end submit(): validate → persist → reviewers → assign → evaluate → notify."""

_PAYLOAD = "Benchmark whole-flow submission payload."


def test_benchmark_optimised_whole_submit_flow(benchmark, optimised_whole_flow_bench):
    submit, reset = optimised_whole_flow_bench

    def run():
        reset()
        return submit(_PAYLOAD)

    benchmark(run)


def test_benchmark_original_whole_submit_flow(benchmark, original_whole_flow_bench):
    submit, reset = original_whole_flow_bench

    def run():
        reset()
        return submit(_PAYLOAD)

    benchmark(run)
