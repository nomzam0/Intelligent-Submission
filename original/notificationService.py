

class NotificationService:
    """
    Service class for sending submission evaluation notifications.
    
    Attributes:
        notification (str): The evaluation result (Accept, Reject, or other)
    """
    def __init__(self, notification):
        self.notification = notification

    def sendNotification(self, notification):
        """
        Routes the notification to appropriate handler based on evaluation outcome.
        
        Args:
            notification (str): The evaluation result (Accept, Reject, or else)
        
        Returns:
            str: Formatted notification message
        """
        if notification == "Accept":
            return self.notifyAcceptance() 
        elif notification == "Reject":
            return self.notifyRejection()
        else:
            return self.notifyRevision()


    def notifyAcceptance(self):
        """
        Returns acceptance notification message.
        
        Returns:
            str: Acceptance message
        """
        return 'This submission has been accepted. Congratulations!'

    def notifyRejection(self):
        """
        Returns rejection notification message.
        
        Returns:
            str: Rejection message
        """
        return 'This submission has been rejected.'

    def notifyRevision(self):
        """
        Returns revision request notification message.
        
        Returns:
            str: Revision message
        """
        return 'This submission requires revision.'