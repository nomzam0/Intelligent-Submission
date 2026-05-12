"""Helpers to load each implementation in isolation (no cross-import cache clashes)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import mongomock
import pymongo
from bson import ObjectId

ROOT = Path(__file__).resolve().parent.parent

ALL_IMPL_MODULE_NAMES = (
    "submissionController",
    "evaluationManager",
    "validator",
    "reviewerManger",
    "databaseManager",
    "submission",
    "reviewer",
    "reviewerManager",
    "notificationService",
    "config",
)


def unload_implementation_modules() -> None:
    for name in ALL_IMPL_MODULE_NAMES:
        sys.modules.pop(name, None)


def prep_import_path(impl_dir: Path) -> None:
    opt = str((ROOT / "optimised").resolve())
    orig = str((ROOT / "original").resolve())
    impl = str(impl_dir.resolve())
    sys.path[:] = [p for p in sys.path if p not in (opt, orig)]
    if impl not in sys.path:
        sys.path.insert(0, impl)


def new_patched_mongo_client() -> mongomock.MongoClient:
    client = mongomock.MongoClient()

    def _factory(*_args: Any, **_kwargs: Any) -> mongomock.MongoClient:
        return client

    pymongo.MongoClient = _factory  # type: ignore[assignment]
    return client


def seed_eligible_reviewers(collection: Any, count: int = 24) -> None:
    docs = [
        {"_id": ObjectId(), "workload": 1, "conflict": False} for _ in range(count)
    ]
    collection.insert_many(docs)


def large_reviewer_pool(size: int = 400) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for i in range(size):
        conflict = i % 17 == 0
        workload = 4 if i % 23 == 0 else 1
        out.append({"_id": ObjectId(), "workload": workload, "conflict": conflict})
    return out
