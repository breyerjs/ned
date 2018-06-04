class Hello:
    def __init__(self, commands):
        # Commands is a list of what followed 'ned' in the slack mention
        # ie. "@ned hi friend" => ['hi', 'friend']
        self.commands = commands

    def process_command(self):
        return "For now, I only say 'hi', but soon I'll say a lot more!"

    def _randomize_greeting(self):
        """
            TODO:
                - This should choose and return a random greeting
                - Call this function in process_command
        """
        pass