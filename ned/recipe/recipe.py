import random
from utility.json_utility import load_json_into_dict
from utility.style_utility import bold, italics, quoted, indent

HELP = """
`ned recipe help`: show this message
`ned recipe random <course>`: get a random recipe, optionally from <course>
`ned recipe <recipe name>`: gets the first recipe with <recipe name> in the name
`ned recipe list <course>: list all recipes, optionally matching <course>`
"""

RECIPE_PATH = './recipe/recipes.json'

class Recipe:
    def __init__(self, commands):
        self.commands = commands
        self.recipes = load_json_into_dict(RECIPE_PATH)

    def process_command(self):
        if len(self.commands) == 1: # no input
            return self._handle_random()
        base_command = self.commands[1]
        if base_command == 'help':
            return HELP
        elif base_command == 'random':
            return self._handle_random()
        else:
            return self._handle_get_recipe_by_name()

    def _handle_random(self):
        matching = None
        # check for a course specifier
        if len(self.commands) >= 3:
            matching = [recipe for recipe in self.recipes['food'] if self.commands[2] == recipe['type']]
            if len(matching) == 0:
                return "Shucks, I can't find any recipes with the course *" + self.commands[2] + "*"
        else:
            matching = self.recipes['food']
        choice = random.choice(matching)
        return self._format_recipe_for_display(choice)
                
    def _handle_get_recipe_by_name(self):
        target = ' '.join(self.commands[1:]).lower()
        matching = [recipe for recipe in self.recipes['food'] if target in recipe['name'].lower()]
        if len(matching) == 0:
            return "My apologies, I have no recipes containing the phrase *" + target + "*"
        else:
            return self._format_recipe_for_display(matching[0])

    def _format_recipe_for_display(self, recipe):
        s = '=== '+bold(recipe['name'])+' ==='
        s += '\n'+indent(italics('Ingredients'))
        for ingredient in recipe['ingredients']:
            s += '\n'+indent(ingredient['amt'] + ' ' + ingredient['name'], 2)
        s += '\n'+ indent(italics('Directions'))
        for i, direction in enumerate(recipe['directions']):
            s += '\n' + indent(str(i+1) + '. ' + direction, 2)
        s += '\n' + indent(italics('Notes')) + '\n'
        s += quoted(recipe['notes'])
        return s