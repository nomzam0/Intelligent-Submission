import random
import notificationService
import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["SmartDB"]
submissions = mydb["submissions"]

class EvaluationManager:
    """
    Manages the evaluation process for research submissions.
    Collects reviewer scores, calculates average score, and applies decision rules.
    
    Attributes:
        reviewers (list): List of reviewer documents assigned to the submission
        submissionID (ObjectId): DB _id of the submission being evaluated
    """
    def __init__(self, reviewers, submissionID):
        self.reviewers = reviewers
        self.submissionID = submissionID

    def startEvaluation(self):
        """
        Initiates the evaluation process: collects scores, calculates average score,
        applies decision rules, and generates notification.
        
        Returns:
            str: Notification message with evaluation outcome
        """
        scores = []
        for rev in self.reviewers:
            score = random.randint(1, 10)
            saveScoreOutput = self.submitScore(self.submissionID, score)
            print(saveScoreOutput)
            scores.append(score)
        average = self.calculateAverage(scores)
        consensus = self.checkConsensus()
        rule = self.applyRules()
        notification = notificationService.NotificationService(rule)
        return notification.sendNotification(rule)

    def submitScore(self, id, score):
        """
        Submits a reviewer score in the database.
        
        Args:
            id (ObjectId): The submission _id
            score (int): The score value (1-10)
        
        Returns:
            str: Database operation confirmation message
        """
        output = saveScore(id, score)
        return output
    
    def calculateAverage(self, scores):
        """
        Calculates the average score from all reviewer scores.
        
        Args:
            scores (list): List of integer scores
        
        Returns:
            float: The average score value
        """
        sum = 0
        counter = 0
        for score in scores:
            sum  += score
            counter += 1          
        average = sum/counter
        return average

    def checkConsensus(self):
        """
        Checks consensus among reviewers (currently random for demonstration).
        
        Returns:
            bool: True if consensus exists, False otherwise
        """
        choice = random.choice([True, False])
        return choice

    def applyRules(self):
        """
        Applies decision rules to determine submission outcome.
        Currently uses random selection for demonstration.
        
        Returns:
            str: Decision outcome (Accept, Reject, or Revise)
        """
        rule = random.choice(["Accept", "Reject", "Revise"])
        return rule

def saveScore(submissionId, score):
        """
        Append a score to the `score` array of the submission with the given id.
        Accepts a string representation of an ObjectId or a raw id value.
        """
        try:
            oid = ObjectId(submissionId)
        except Exception:
            oid = submissionId

        # Try updating by DB _id first (ObjectId). $push will create the array if missing.
        result = submissions.update_one({"_id": oid}, {"$push": {"scores": score}})
        if result.matched_count == 0:
            # Fallback: try matching a non-_id `id` field in the document
            result2 = submissions.update_one({"id": oid}, {"$push": {"scores": score}})
            if result2.matched_count == 0:
                return "No submission found with id: " + str(submissionId)
            return "Score added to submission with id field: " + str(submissionId)

        return "Score added to submission with _id: " + str(submissionId)