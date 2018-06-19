import re
from enum import Enum

MENTION_REGEX = '^<@(|[WU].+?)>(.*)'
NED_REGEX = '^([Nn]ed )(.*)'
NED_COMMAND_TYPE = 'ned'
NO_COMMANDS = (None, None, None)

class CommandTypes(Enum):
    NED = 'ned'
    KARMA = 'karma'

class Listener:
    def __init__(self, slack_client, ned_id):
        self.ned_id = ned_id
        self.slack_client = slack_client

    def listen(self, slack_events):
        """
            Takes in a feed of slack messages and either returns 
                1) the processed command & channel, if they're applicable
        """
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                commands = self._get_ned_commands_or_None(event['text'])
                if commands is not None:
                    command_type = CommandTypes.NED
                    return (commands, event["channel"], command_type)
                # TODO Karma goes here
        return NO_COMMANDS

    def _get_ned_commands_or_None(self, message_text):
        """
            Either returns the processed 'ned' commands or None
                ie. `ned hi` returns ['hi']
                ie. `jackson++ whoah` returns None
        """
        matches = re.search(NED_REGEX, message_text)
        if matches is not None and len(matches.groups()) >= 2:
            return self.process_commands(matches.group(2))
        return None


    def process_commands(self, commands):
        """
            Takes in a string of the commands.
            Cleans and returns them
        """
        processed = commands.strip().lower().split()
        return processed

    def _get_direct_mention_and_userId(self, message_text):
        """
            NO LONGER USED
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def _parse_direct_mention_bot_commands(self, slack_events):
        """
            NO LONGER USED
            Parses a list of events coming from the Slack RTM API to find bot commands.
            If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                user_id, message = self._get_direct_mention_and_userId(event["text"])
                if user_id == self.ned_id:
                    return message, event["channel"]
        return None, None