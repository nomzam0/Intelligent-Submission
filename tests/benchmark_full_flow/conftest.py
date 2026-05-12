import pytest

from tests._support import (
    ROOT,
    new_patched_mongo_client,
    prep_import_path,
    seed_eligible_reviewers,
    unload_implementation_modules,
)

_SEED_REVIEWERS = 24


@pytest.fixture(scope="module")
def optimised_whole_flow_bench():
    """
    Full optimised submit() stack. Caller resets DB so each benchmark iteration
    runs the happy path (workloads do not accumulate across iterations).
    """
    unload_implementation_modules()
    prep_import_path(ROOT / "optimised")
    new_patched_mongo_client()
    import databaseManager as dm
    import submissionController as sc

    def reset():
        dm.submissions.delete_many({})
        dm.reviewers.delete_many({})
        seed_eligible_reviewers(dm.reviewers, count=_SEED_REVIEWERS)

    reset()
    yield sc.submit, reset
    unload_implementation_modules()


@pytest.fixture(scope="module")
def original_whole_flow_bench():
    unload_implementation_modules()
    prep_import_path(ROOT / "original")
    new_patched_mongo_client()
    import reviewerManger as rm
    import submissionController as sc

    def reset():
        sc.submissions.delete_many({})
        rm.reviewers.delete_many({})
        seed_eligible_reviewers(rm.reviewers, count=_SEED_REVIEWERS)

    reset()
    yield sc.submit, reset
    unload_implementation_modules()
