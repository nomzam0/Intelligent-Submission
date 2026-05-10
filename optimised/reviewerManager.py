
def getAvailableReviewers(dbm):
    """
    Retrieves reviewers eligible for assignment using server-side filtering.

    Args:
        dbm (Database): Database manager instance for data access

    Returns:
        list: Reviewer documents matching workload and conflict criteria
    """
    return dbm.fetchAvailableReviewers()
