import re
from enum import Enum 
from karma.karma import Karma
from utility.commands import Commands

MENTION_REGEX = '^<@(|[WU].+?)>(.*)'
NED_REGEX = '^([Nn]ed )(.*)'
KARMA_REGEX = r'\+\+|\--|\+-|\-\+'

class Listener:
    def __init__(self, slack_client):
        self.slack_client = slack_client
        # Read bot's user ID by calling Web API method `auth.test`
        self.ned_id = slack_client.api_call("auth.test")["user_id"]      
        self.karma_client = Karma()  

    def listen(self, slack_events):
        """
            Takes in a feed of slack messages and returns either
                1) a Commands object if there's work to do
                2) None if there's not
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