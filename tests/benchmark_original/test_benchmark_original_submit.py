def test_original_full_submit_pipeline(benchmark, original_submit):
    """End-to-end submit: validate, persist, assign reviewers, evaluate, notify."""

    def run():
        return original_submit("Benchmark submission body for original pipeline.")

    benchmark(run)


def test_original_reviewer_filter_large_pool(benchmark, original_reviewer_filter):
    from tests._support import large_reviewer_pool

    pool = large_reviewer_pool(400)
    rm = original_reviewer_filter

    def run():
        step = rm.filterConflict(pool)
        return rm.checkWorkload(step)

    benchmark(run)
