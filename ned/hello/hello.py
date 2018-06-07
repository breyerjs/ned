class Hello:
    def __init__(self, commands):
        # Commands is a list of what followed 'ned' in the slack mention
        # ie. "@ned hi friend" => ['hi', 'friend']
        self.commands = commands

    def process_command(self):
        return self._randomize_greeting()

    def _randomize_greeting(self):
        """
            TODO:
                - This should choose and return a random greeting
        """
        return "For now, I only say 'hi', but soon I'll say a lot more! If only Rachelle would update me!"
