import os

FILENAME = './karma/karma.json'
INITIAL_STRUCTURE = {}

class Karma:
    """
        This needs to work differently than the other commands. 
        It needs to run passively over all messages. 
    """
    def __init__(self, commands, json_utility):
        self.commands = commands
        self.json_utility = json_utility
 
    def process_command(self):
        karma_changed_entities = [word for word in self.commands if 
            word.endswith('++') 
            or word.endswith('--') 
            or word.endswith('+-') 
            or word.endswith('-+')
        ]
        json = self.json_utility.load_or_create_file(FILENAME, INITIAL_STRUCTURE) 
        for entity in karma_changed_entities:
            self._perform_update(entity, json)        
        # build and return the messaging
        return self._build_response(karma_changed_entities, json)
    
    def _process_name(self, entity):
        entity = entity.strip('@+-') # remove all mentions, plusses and minuses
        return entity

    def _perform_update(self, entity, json):
        if len(entity) < 3:
            return
        modifier = entity[-2:]
        if modifier == '++':
            cleaned_entity = self._process_name(entity)
            self._add_or_update_name(json, cleaned_entity, 1)
        elif modifier == '--':
            cleaned_entity = self._process_name(entity)
            self._add_or_update_name(json, cleaned_entity, -1)
        self.json_utility.write_to_file(FILENAME, json)

    def _add_or_update_name(self, json, entity, amt_to_add):
        if entity not in json:
            json[entity] = 0
        json[entity] += amt_to_add

    def _build_response(self, entities, json):
        response = []
        for entity in entities:
            cleaned_entity = self._process_name(entity)
            response.append(cleaned_entity + "'s karma is now at *" + str(json[cleaned_entity]) + '*')
        return '\n'.join(response)