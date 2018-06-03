from recipe.recipe import Recipe

commands = "recipe random".split()

print(Recipe(commands).process_command())
