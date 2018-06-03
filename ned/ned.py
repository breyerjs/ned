import os
import time
import re
import json
from recipe.recipe import Recipe
from slackclient import SlackClient

RTM_READ_DELAY = 0.5 # 0.5 second delay between reading from RTM
MENTION_REGEX = '^<@(|[WU].+?)>(.*)'
DEFAULT_RESPONSE = 'A thousand pardons. What you ask is beyond my skill.'

def load_bot_auth_token():
    with open('secrets.json') as json_data:
        data = json.load(json_data)
        token = data.get('bot_user_oauth_access_token')
        if token is None:
            print('Warning: could not find oauth token')
        return token 

# value is assigned after the bot starts up
ned_id = None
slack_client = SlackClient(load_bot_auth_token())

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == ned_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    response = None
    try:
        commands = process_commands(command)
        base_command = commands[0]
        # This is where you start to implement more commands!
        if base_command in 'hi hello hey'.split():
            response = 'Greetings, my friend! I hope you are well.'
        elif base_command == 'recipe':
            response = Recipe(commands).process_command()

        send_response(channel, response)
    except Exception as e:
        print(e)
        response = 'Great Scott! I seem to have encountered an error :('

def send_response(channel, response):
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or DEFAULT_RESPONSE
    )

def process_commands(commands):
    """
        Takes in a string of the commands.
        Cleans and returns them
    """
    processed = commands.strip().lower().split()
    return processed

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Ned is connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        ned_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Ruh roh! Connection failed. Exception traceback printed above.")
