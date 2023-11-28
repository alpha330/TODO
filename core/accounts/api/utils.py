import threading


# create function for parallel processing in specific request
class EmailThread(threading.Thread):
    """
    This class is used to create a thread for sending emails in parallel.
    """

    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()
