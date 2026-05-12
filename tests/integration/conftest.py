import pytest

from tests._support import (
    ROOT,
    new_patched_mongo_client,
    prep_import_path,
    seed_eligible_reviewers,
    unload_implementation_modules,
)


@pytest.fixture
def optimised_flow():
    unload_implementation_modules()
    prep_import_path(ROOT / "optimised")
    new_patched_mongo_client()
    import databaseManager as dm
    import notificationService as ns
    import submissionController as sc

    seed_eligible_reviewers(dm.reviewers, count=3)
    yield sc, dm, ns
    unload_implementation_modules()


@pytest.fixture
def original_flow():
    unload_implementation_modules()
    prep_import_path(ROOT / "original")
    new_patched_mongo_client()
    import notificationService as ns
    import reviewerManger as rm
    import submissionController as sc

    seed_eligible_reviewers(rm.reviewers, count=3)
    yield sc, rm, ns
    unload_implementation_modules()
