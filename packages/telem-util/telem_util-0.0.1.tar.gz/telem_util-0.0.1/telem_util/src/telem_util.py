class TelemUtil:
    def __init__(self):
        self.telem_data = []
        self.stats = []

    def capture_details(self, exception, time, project_label):
        payload = {
            "exception" : exception,
            "time" : time,
            "project_label" : project_label
        }
        self.telem_data.append(payload)

    def user_stats(self, test_session_id):
        self.stats.append(test_session_id)