import json
import random

HELP = """
`ned recipe help`: show this message
`ned recipe random <course>`: get a random recipe, optionally from <course>
`ned recipe <recipe name>`: gets the first recipe with <recipe name> in the name
`ned recipe list <course>: list all recipes, optionally matching <course>`
"""

class Recipe:
    def __init__(self, commands):
        self.commands = commands
        self.recipes = self._load_recipes()
    
    def _load_recipes(self):
        # path is relative to ned.py, not this file
        with open('./recipe/recipes.json') as json_data:
            return json.load(json_data)

    def process_command(self):
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
            matching = [recipe for recipe in self.recipes['food']]
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
        s = '=== *'+recipe['name']+'* ==='
        s += '\n\t_Ingredients_'
        for ingredient in recipe['ingredients']:
            s += '\n\t\t'+ingredient['amt'] + ' ' + ingredient['name']
        s += '\n\t_Directions_'
        for i, direction in enumerate(recipe['directions']):
            s += '\n\t\t' + str(i+1) + '. ' + direction
        s += '\n\t_Notes_\n'
        s += '>' + recipe['notes']
        return s