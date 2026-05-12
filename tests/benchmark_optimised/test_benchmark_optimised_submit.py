def test_optimised_full_submit_pipeline(benchmark, optimised_submit):
    """End-to-end submit: validate, persist, assign reviewers, evaluate, notify."""

    def run():
        return optimised_submit("Benchmark submission body for optimised pipeline.")

    benchmark(run)


def test_optimised_eligible_reviewers_query(benchmark, optimised_fetch_eligible):
    """Indexed fetchAvailableReviewers with many documents."""

    benchmark(optimised_fetch_eligible)
