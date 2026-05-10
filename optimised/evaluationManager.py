import random

import notificationService


class EvaluationManager:
    """
    Manages the submission evaluation workflow using collecting reviewer scores
    and applying decision logic to determine submission outcomes.
    
    Attributes:
        reviewers (list): List of assigned reviewer documents
        submissionID (ObjectId): DB _id of the submission being evaluated
        dbm (Database): Database manager for score persistence
    """
    def __init__(self, reviewers, submissionID, dbm):
        self.reviewers = reviewers
        self.submissionID = submissionID
        self.dbm = dbm

    def startEvaluation(self):
        """
        Initiates the evaluation: generates scores, persists them,
        applies rules, and returns decision outcome.
        
        Returns:
            str: Final evaluation decision (Accepted, Rejected, or Needs Revision)
        """
        scores = []
        for _ in self.reviewers:
            score = random.randint(1, 10)
            scores.append(score)
        self.submitScores(self.submissionID, scores)
        rule = self.applyRules()
        return rule

    def submitScores(self, id, scores):
        """
        Persists all reviewer scores for a submission to the database.
        
        Args:
            id (ObjectId): The submission _id
            scores (list): List of integer scores from reviewers
        
        Returns:
            str: Database operation confirmation message
        """
        output = self.dbm.saveScores(id, scores)
        return output

    def applyRules(self):
        """
        Applies decision rules to generate submission outcome.
        Currently uses random selection for demonstration purposes.
        
        Returns:
            str: Decision outcome (Accepted, Rejected, or Needs Revision)
        """
        rule = random.choice(notificationService.ALL_OUTCOMES)
        return rule