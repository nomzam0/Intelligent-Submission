import evaluationManager
import submission
import reviewerManager
import reviewer
import databaseManager
import notificationService


def submit(data):
    """
    Main submission workflow orchestrator: validates, persists, and evaluates submissions.

    Args:
        data (str): The research submission data to process

    Returns:
        str: Notification message with submission status or evaluation outcome
    """
    notification = notificationService.NotificationService(None)
    sub = submission.Submission(data)
    if not sub.validateFormat():
        return notification.sendNotification(notificationService.REJECTED)

    doc = sub.createSubmission()
    dbm = databaseManager.getDatabase()
    submission_id = dbm.saveSubmission(doc)

    available = reviewerManager.getAvailableReviewers(dbm)
    if len(available) == 0:
        return notification.sendNotification(notificationService.MSG_NO_REVIEWERS)

    reviewer.Reviewer(dbm).assignReviews(available)
    evaluation_manager = evaluationManager.EvaluationManager(
        available, submission_id, dbm
    )
    evaluation = evaluation_manager.startEvaluation()
    return notification.sendNotification(evaluation)
