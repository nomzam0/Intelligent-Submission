import pytest

from tests._support import (
    ROOT,
    new_patched_mongo_client,
    prep_import_path,
    seed_eligible_reviewers,
    unload_implementation_modules,
)


@pytest.fixture(scope="module")
def original_submit():
    unload_implementation_modules()
    prep_import_path(ROOT / "original")
    new_patched_mongo_client()
    import reviewerManger as rm
    import submissionController as sc

    seed_eligible_reviewers(rm.reviewers)
    yield sc.submit
    unload_implementation_modules()


@pytest.fixture(scope="module")
def original_reviewer_filter():
    unload_implementation_modules()
    prep_import_path(ROOT / "original")
    new_patched_mongo_client()
    import reviewerManger as rm

    yield rm
    unload_implementation_modules()
