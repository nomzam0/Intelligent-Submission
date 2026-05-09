import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["SmartDB"]
reviewers = mydb["reviewers"]

def assignReviews(reviewerId):
    """
    Assigns a review to a reviewer by incrementing their workload counter.
    
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