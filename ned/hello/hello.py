import random

GREETINGS = [
    "Ned, speaking in the third person, also says hello",
    "Kamusta, kaibigan",
    "Hello, friend",
    "Salutations.",
    "It's always 'Good Morning' somewhere"
]

class Hello:
    def __init__(self, commands):
        # Commands is a list of what followed 'ned' in the slack mention
        # ie. "@ned hi friend" => ['hi', 'friend']
        self.commands = commands

    def process_command(self):
        return self._randomize_greeting()

    def _randomize_greeting(self):
        return random.choice(GREETINGS)
