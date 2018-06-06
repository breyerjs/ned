POINTS = {
    'a': 1,
    'b': 3,
    'c': 3,
    'd': 2,
    'e': 1,
    'f': 4,
    'g': 2,
    'h': 4,
    'i': 1,
    'j': 8,
    'k': 5,
    'l': 1,
    'm': 3,
    'n': 1,
    'o': 1,
    'p': 3,
    'q': 10,
    'r': 1,
    's': 1,
    't': 1,
    'u': 1,
    'v': 4,
    'w': 4,
    'x': 8,
    'y': 4,
    'z': 10
}

class Scrabble:
    def __init__(self, commands):
        # Commands is a list of what followed 'ned' in the slack mention
        # ie. "@ned hi friend" => ['hi', 'friend']
        self.commands = commands

    def process_command(self):
        if len(self.commands) != 2:
            return "Please enter one word so I can calculate its Scrabble score!"
        score = self._calc_score(self.commands[1])
        if score is None:
            return "Hm, some of those letters don't seem to have scrabble values!"
        return "The score for *" + self.commands[1] + "* is: " + str(score)
    
    def _calc_score(self, word):
        total = 0
        for char in word:
            if char not in POINTS:
                return None
            else:
                total += POINTS[char]
        return total