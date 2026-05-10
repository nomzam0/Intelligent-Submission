"""Runtime configuration from environment with safe defaults."""

import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "SmartDB")
SUBMISSIONS_COLLECTION = os.environ.get("MONGO_SUBMISSIONS_COLLECTION", "submissions")
REVIEWERS_COLLECTION = os.environ.get("MONGO_REVIEWERS_COLLECTION", "reviewers")

# Original workload rule: reviewers with workload <= 2 are available
MAX_REVIEWER_WORKLOAD = int(os.environ.get("MAX_REVIEWER_WORKLOAD", "2"))
