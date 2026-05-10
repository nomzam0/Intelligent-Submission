"""Evaluation outcomes and user-facing notification messages."""

ACCEPTED = "Accepted"
REJECTED = "Rejected"
NEEDS_REVISION = "Needs Revision"

ALL_OUTCOMES = (ACCEPTED, REJECTED, NEEDS_REVISION)

MSG_NO_REVIEWERS = (
    "No available reviewers at the moment. Please try again later."
)


class NotificationService:
    """
    Service for sending submission evaluation notifications to users.

    Attributes:
        notification (str): The evaluation result to be communicated
    """

    def __init__(self, notification):
        self.notification = notification

    def sendNotification(self, notification):
        """
        Formats and sends evaluation notification to the user.

        Args:
            notification (str): The evaluation outcome

        Returns:
            str: Formatted notification message with evaluation outcome
        """
        return "Evaluation of your submission is done with the following outcome: " + notification
