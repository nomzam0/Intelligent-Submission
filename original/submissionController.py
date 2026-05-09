import evaluationManager
import validator
import reviewerManger
import reviewer

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["SmartDB"]
submissions = mydb["submissions"]

def submit(data):
    """
    Handles the main submission workflow: validates data, saves submission,
    assigns reviewers, and initiates evaluation.
    
    Args:
        data (str): The research submission data to process
    
    Returns:
        str: Notification message indicating submission status or rejection reason
    """
    valid = validator.validateFormat(data)
    if valid:
        submissionID = saveSubmission(data)
        print("Submission saved with ID:", submissionID)
        filteredReviewers = reviewerManger.getAvailableReviewers()
        if len(filteredReviewers) == 0:
            return "Data submitted successfully! \n No available reviewers at the moment. Please try again later."
        for rev in filteredReviewers:
            reviewer.assignReviews(rev['_id'])
        eval = evaluationManager.EvaluationManager(filteredReviewers, submissionID)
        notification = eval.startEvaluation()
        return notification
    
    return valid

def saveSubmission(data):
    """
    Saves a new submission to the DB submissions collection.
    
    Args:
        data (str): The submission content/data
    
    Returns:
        ObjectId: The DB _id of the inserted submission document
    """
    insertion = {
        "data": data,
        "scores": []
        }
    insertion = submissions.insert_one(insertion)
    return insertion.inserted_id
