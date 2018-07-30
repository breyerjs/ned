import re

DEFAULT_RESPONSE = 'A thousand pardons. What you ask is beyond my skill.'
MENTION_REGEX = '^<@(|[WU].+?)>(.*)'
KARMA_REGEX = r'\+\+|\--|\+-|\-\+'
NO_COMMANDS = (None, None, None)

NED_NAME = 'ned'

class Commands:
    def __init__(self, event):
        self.event = event
        self.commands = self._process_commands(event['text'])
        self.ned_command = self._get_ned_commands_or_None(self.commands)
        self.karmatic_entities = self._get_karmatic_entities(self.commands)
        self.work_to_do = self.ned_command or self.karmatic_entities

    def _process_commands(self, commands):
        """
            Takes in a string of the commands.
            Cleans and returns them
        """
        processed = commands.strip().lower().split()
        return processed

    def _get_ned_commands_or_None(self, commands):
        """
            Either returns the processed 'ned' commands or None
                ie. `ned hi` returns ['hi']
                ie. `jackson++ whoah` returns None
        """
        if commands and commands[0] == NED_NAME and len(commands) > 1:
            return commands[1:] # removes the 'ned' at the beginning
        else:
            return None

    def _get_karmatic_entities(self, commands):
        karma_endings = '++ -- +- -+'.split()
        return [word for word in commands if word[-2:] in karma_endings]
