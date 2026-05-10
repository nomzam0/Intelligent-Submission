
class Reviewer:
    """
    Handles review assignments.
    """

    def __init__(self, dbm):
        self.dbm = dbm

    def assignReviews(self, reviewers):
        """
        Increments workload for each assigned reviewer.

        Args:
            reviewers (list): Reviewer documents from fetchAvailableReviewers

        Returns:
            str: Last assignment status message from the database layer
        """
        output = ""
        for rev in reviewers:
            output = self.dbm.assignReviews(rev.get("_id"))
        return output
