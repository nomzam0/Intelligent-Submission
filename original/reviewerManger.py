import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["SmartDB"]
reviewers = mydb["reviewers"]

def getAvailableReviewers():
    """
    Retrieves a list of reviewers filtered by conflicts and workload constraints.
    
    Returns:
        list: List of reviewer documents that have no conflicts and workload <= 2
    """
    reviewers = fetchReviewers()
    availableReviewer = filterConflict(reviewers)
    newAvailableReviewer = checkWorkload(availableReviewer)
    return newAvailableReviewer


def filterConflict(reviewers):
    """
    Filters reviewers who do not have conflicts of interest.
    
    Args:
        reviewers (list): List of reviewer documents
    
    Returns:
        list: Reviewers without conflicts (conflict field is False/None)
    """
    filteredReviewers = []
    for reviewer in reviewers:
        if not reviewer.get('conflict'):
            filteredReviewers.append(reviewer)
    return filteredReviewers

def checkWorkload(filteredReviewers):
    """
    Filters reviewers based on workload capacity (max 2 concurrent reviews).
    
    Args:
        filteredReviewers (list): Pre-filtered list of reviewer documents
    
    Returns:
        list: Reviewers with workload <= 2 (available for assignment)
    """
    newFilteredList = []
    for reviewer in filteredReviewers:
        if reviewer.get('workload') <= 2:
            newFilteredList.append(reviewer)
    return newFilteredList

def fetchReviewers():
    """
    Retrieves all reviewers from the DB reviewers collection.
    
    Returns:
        list: All reviewer documents from the database
    """
    foundReviewers = reviewers.find()
    return list(foundReviewers)