class Submission:
    """
    Handles submission validation and document shaping for DB.

    Attributes:
        data (str): The submission content being processed
    """

    def __init__(self, data):
        self.data = data
        self.scores = []

    def validateFormat(self):
        """
        Validates that the input data is not empty.

        Returns:
            bool: True if data length > 0, False otherwise
        """
        return len(self.data) > 0

    def createSubmission(self):
        """
        Creates a submission document when validation passes.

        Returns:
            dict | None: Submission document, or None if invalid
        """
        if not self.validateFormat():
            return None
        return {"data": self.data, "scores": self.scores}
