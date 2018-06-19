import os
import time
import re
import json
from json_utility.json_utility import JsonUtility
from recipe.recipe import Recipe
from hello.hello import Hello
from flip.flip import Flip
from scrabble.scrabble import Scrabble
from listener.listener import Listener
from slackclient import SlackClient

RTM_READ_DELAY = 0.5 # 0.5 second delay between reading from RTM
DEFAULT_RESPONSE = 'A thousand pardons. What you ask is beyond my skill.'

def load_bot_auth_token():
    secrets = JsonUtility().load_json_into_dict('secrets.json')
    token = secrets.get('bot_user_oauth_access_token')
    if token is None:
        print('Warning: could not find oauth token')
    return token 

# value is assigned after the bot starts up
ned_id = None
slack_client = SlackClient(load_bot_auth_token())

def _send_response(channel, response):
    """
        Sends the response back to the channel
    """
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or DEFAULT_RESPONSE
    )

def _get_response(commands, command_type):
    """
        Finds the correct response given some ned command
    """
    response = None
    try:
        base_command = commands[0]
        # This is where you start to implement more commands!
        if base_command in 'hi hello hey'.split():
            response = Hello(commands).process_command()
        elif base_command == 'recipe':
            response = Recipe(commands).process_command()
        elif base_command == 'flip':
            response = Flip(commands).process_command()
        elif base_command == 'scrabble':
            response = Scrabble(commands).process_command()
        return response
    except Exception as e:
        print(e)
        response = 'Great Scott! I seem to have encountered an error :('
        return response

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False, auto_reconnect=True):
        print("Ned is connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        ned_id = slack_client.api_call("auth.test")["user_id"]
        slack_listener = Listener(slack_client, ned_id)
        while True:
            commands, channel, command_type = slack_listener.listen(slack_client.rtm_read())
            if commands:
                print(commands)
                _send_response(channel, _get_response(commands, command_type))
            time.sleep(RTM_READ_DELAY)
    else:
        print("Ruh roh! Connection failed. Exception traceback printed above.")
