import pytest

from tests._support import (
    ROOT,
    large_reviewer_pool,
    new_patched_mongo_client,
    prep_import_path,
    seed_eligible_reviewers,
    unload_implementation_modules,
)


@pytest.fixture(scope="module")
def optimised_submit():
    unload_implementation_modules()
    prep_import_path(ROOT / "optimised")
    new_patched_mongo_client()
    import databaseManager as dm

    seed_eligible_reviewers(dm.reviewers)
    import submissionController as sc

    yield sc.submit
    unload_implementation_modules()


@pytest.fixture(scope="module")
def optimised_fetch_eligible():
    """Large reviewer set; benchmarks indexed eligibility query (server-side filter)."""
    unload_implementation_modules()
    prep_import_path(ROOT / "optimised")
    new_patched_mongo_client()
    import databaseManager as dm

    dm.reviewers.insert_many(large_reviewer_pool(400))
    db = dm.getDatabase()
    yield db.fetchAvailableReviewers
    unload_implementation_modules()
