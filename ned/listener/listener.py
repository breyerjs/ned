import re
from enum import Enum 
from karma.karma import Karma
from utility.commands import Commands

MENTION_REGEX = '^<@(|[WU].+?)>(.*)'
NED_REGEX = '^([Nn]ed )(.*)'
KARMA_REGEX = r'\+\+|\--|\+-|\-\+'

class CommandTypes(Enum):
    NED = 'ned'

class Listener:
    def __init__(self, slack_client):
        self.slack_client = slack_client
        # Read bot's user ID by calling Web API method `auth.test`
        self.ned_id = slack_client.api_call("auth.test")["user_id"]      
        self.karma_client = Karma()  

    def listen(self, slack_events):
        """
            Takes in a feed of slack messages and either returns 
                1) the processed command & channel, if they're applicable
        """
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                return Commands(event)
        return None


def send_response(slack_client, channel, response):
    """
        Sends the response back to the channel
    """
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response
    )

    # def _get_direct_mention_and_userId(self, message_text):
    #     """
    #         NO LONGER USED
    #         Finds a direct mention (a mention that is at the beginning) in message text
    #         and returns the user ID which was mentioned. If there is no direct mention, returns None
    #     """
    #     matches = re.search(MENTION_REGEX, message_text)
    #     # the first group contains the username, the second group contains the remaining message
    #     return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    # def _parse_direct_mention_bot_commands(self, slack_events):
    #     """
    #         NO LONGER USED
    #         Parses a list of events coming from the Slack RTM API to find bot commands.
    #         If a bot command is found, this function returns a tuple of command and channel.
    #         If its not found, then this function returns None, None.
    #     """
    #     for event in slack_events:
    #         if event["type"] == "message" and not "subtype" in event:
    #             user_id, message = self._get_direct_mention_and_userId(event["text"])
    #             if user_id == self.ned_id:
    #                 return message, event["channel"]
    #     return None, None
