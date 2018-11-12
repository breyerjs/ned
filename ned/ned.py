import os
import time
import json
from utility.json_utility import load_json_into_dict
from hello.hello import Hello
from flip.flip import Flip
from karma.karma import Karma
from listener.listener import Listener
from listener.listener import send_response
from love.love import Love
from recipe.recipe import Recipe
from scrabble.scrabble import Scrabble
from shades.shades import Shades
from slackclient import SlackClient

DEFAULT_RESPONSE = 'A thousand pardons. What you ask is beyond my skill.'

COMMANDS = """```
Flip
Hello
Love
Recipe
Scrabble
Shades
```
"""

RTM_READ_DELAY = 0.5 # 0.5 second delay between reading from RTM

def load_bot_auth_token():
    secrets = load_json_into_dict('secrets.json')
    token = secrets.get('bot_user_oauth_access_token')
    if token is None:
        print('Warning: could not find oauth token')
    return token 

# value is assigned after the bot starts up
ned_id = None
slack_client = SlackClient(load_bot_auth_token())

def _get_responses(commands):
    """
        Finds the correct response given some set of commands
    """
    responses = []
    try:
        # Direct command to ned
        if commands.ned_command:
            base_command = commands.ned_command[0]
            if base_command in ['hi', 'hello', 'hey', 'kamusta', 'heya', 'howdy']:
                ned_response = Hello(commands.ned_command).process_command()
            elif base_command == 'recipe':
                ned_response = Recipe(commands.ned_command).process_command()
            elif base_command == 'flip':
                ned_response = Flip(commands.ned_command).process_command()
            elif base_command == 'love':
                ned_response = Love(commands.ned_command).process_command()
            elif base_command == 'scrabble':
                ned_response = Scrabble(commands.ned_command).process_command()
            elif base_command == 'shades':
                ned_response = Shades(commands.ned_command).process_command()
            elif base_command in 'commands help'.split():
                ned_response = COMMANDS
            else:
                ned_response = DEFAULT_RESPONSE
            responses.append(ned_response)
        # Any karmatic changes that have happened
        if commands.karmatic_entities:
            karma_response = Karma().process_commands(commands.karmatic_entities)
            responses.append(karma_response)
        return responses
    except Exception as e:
        print(e)
        response = 'Great Scott! I seem to have encountered an error :('
        return [response]

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False, auto_reconnect=True):
        print("Ned is connected and running!")
        slack_listener = Listener(slack_client)
        while True:
            commands = slack_listener.listen(slack_client.rtm_read())
            if commands and commands.work_to_do:
                responses = _get_responses(commands)
                for response in responses:
                    send_response(slack_client, commands.event['channel'], response)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Ruh roh! Connection failed. Exception traceback printed above.")
