"""End-to-end submit() tests (mongomock; no real MongoDB required)."""

from tests._support import (
    ROOT,
    new_patched_mongo_client,
    prep_import_path,
    unload_implementation_modules,
)


def test_optimised_full_flow_success(optimised_flow):
    sc, dm, ns = optimised_flow
    body = "Integration test submission body."
    result = sc.submit(body)

    assert "Evaluation of your submission is done with the following outcome:" in result
    assert any(o in result for o in ns.ALL_OUTCOMES)

    docs = list(dm.submissions.find())
    assert len(docs) == 1
    assert docs[0]["data"] == body
    n_reviewers = 3
    assert len(docs[0].get("scores", [])) == n_reviewers


def test_optimised_full_flow_rejects_empty(optimised_flow):
    sc, dm, ns = optimised_flow
    result = sc.submit("")
    assert ns.REJECTED in result
    assert dm.submissions.count_documents({}) == 0


def test_optimised_full_flow_no_reviewers():
    unload_implementation_modules()
    prep_import_path(ROOT / "optimised")
    new_patched_mongo_client()
    try:
        import databaseManager as dm
        import notificationService as ns
        import submissionController as sc

        assert dm.reviewers.count_documents({}) == 0
        result = sc.submit("orphan submission")
        assert ns.MSG_NO_REVIEWERS in result
    finally:
        unload_implementation_modules()


def test_original_full_flow_success(original_flow):
    sc, rm, _ns = original_flow
    body = "Original stack integration test."
    result = sc.submit(body)

    assert result in (
        "This submission has been accepted. Congratulations!",
        "This submission has been rejected.",
        "This submission requires revision.",
    )

    import pymongo

    client = pymongo.MongoClient()
    subs = client["SmartDB"]["submissions"]
    docs = list(subs.find())
    assert len(docs) == 1
    assert docs[0]["data"] == body
    assert len(docs[0].get("scores", [])) == 3


def test_original_full_flow_invalid_data(original_flow):
    sc, _rm, _ns = original_flow
    assert sc.submit("") is False
