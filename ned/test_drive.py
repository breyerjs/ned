from recipe.recipe import Recipe

commands = "recipe lamb".split()

print(Recipe(commands).process_command())