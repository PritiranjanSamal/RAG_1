from collections import deque


class ChatHistory:

    def __init__(self, max_messages=10):

        self.history = deque(maxlen=max_messages)

    def add_user(self, message):

        self.history.append(
            ("User", message)
        )

    def add_assistant(self, message):

        self.history.append(
            ("Assistant", message)
        )

    def get_history(self):

        history = ""

        for role, msg in self.history:

            history += f"{role}: {msg}\n"

        return history