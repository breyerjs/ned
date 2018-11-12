import random
PERSON = '(>^.^)> '
EMOTION = ':hearts: '

class Love:
    def __init__(self, commands):
        self.commands = commands

    def process_command(self):
        return PERSON + EMOTION + self.get_suffix()

    def get_suffix(self):
        if len(self.commands) == 1:
            return self.get_random_word()
        else:
            return ' '.join(self.commands[1:])
    
    def get_random_word(self):
        return random.choice(['desk', 'chair', 'lamp'])