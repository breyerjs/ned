from karma.karma import Karma
from json_utility.json_utility import JsonUtility

commands = "@jackson++".split()

ju = JsonUtility()

print(Karma(commands, ju).process_command())
