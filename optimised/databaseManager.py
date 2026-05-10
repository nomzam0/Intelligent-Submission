import pymongo
from bson.objectid import ObjectId
import config

_client = pymongo.MongoClient(config.MONGO_URI)
_db = _client[config.MONGO_DB_NAME]
submissions = _db[config.SUBMISSIONS_COLLECTION]
reviewers = _db[config.REVIEWERS_COLLECTION]

class Database:
    """
    Centralized database access layer for DB operations.
    """

    def saveSubmission(self, submission_document):
        """
        Saves a new submission document to DB.

        Args:
            submission_document (dict): Document to insert (e.g. data + scores fields)

        Returns:
            ObjectId: The DB _id of the inserted submission document
        """
        insertion = submissions.insert_one(submission_document)
        return insertion.inserted_id

    def fetchAvailableReviewers(self):
        """
        Single source of truth for availability: workload within limit and no
        explicit conflict=True (matches previous client-side rules).
        """
        query = {
            "workload": {"$lte": config.MAX_REVIEWER_WORKLOAD},
            "conflict": {"$ne": True},
        }
        return list(reviewers.find(query))

    def assignReviews(self, reviewerId):
        """
        Assigns a review by incrementing a reviewer's workload counter in the database.

        Args:
            reviewerId (str or ObjectId): The DB _id of the reviewer

        Returns:
            str: Confirmation message or error message if reviewer not found
        """
        try:
            oid = ObjectId(reviewerId)
        except Exception:
            oid = reviewerId

        result = reviewers.update_one({"_id": oid}, {"$inc": {"workload": 1}})
        if result.matched_count == 0:
            return "No reviewer found with id: " + str(reviewerId)
        return "Review assigned to reviewer with id: " + str(reviewerId)

    def saveScores(self, submissionId, scores):
        """
        Appends each score to the submission's scores array (flat list of numbers).

        Args:
            submissionId (str or ObjectId): The DB _id of the submission
            scores (list): Integer scores to append one-by-one

        Returns:
            str: Confirmation message or error message if submission not found
        """
        try:
            oid = ObjectId(submissionId)
        except Exception:
            oid = submissionId

        update = {"$push": {"scores": {"$each": scores}}}
        result = submissions.update_one({"_id": oid}, update)
        if result.matched_count == 0:
            result2 = submissions.update_one({"id": oid}, update)
            if result2.matched_count == 0:
                return "No submission found with id: " + str(submissionId)
            return "Score added to submission with id field: " + str(submissionId)

        return "Score added to submission with _id: " + str(submissionId)


_shared_database = Database()


def getDatabase():
    """Return the process-wide Database instance (reuses the Mongo client)."""
    return _shared_database
