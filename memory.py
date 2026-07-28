class ConversationMemory:

    def __init__(self):

        self.last_career = None

    def set_career(self, career):

        self.last_career = career

    def get_career(self):

        return self.last_career


memory = ConversationMemory()