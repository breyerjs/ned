import os

FILENAME = './karma/karma.json'
INITIAL_STRUCTURE = {}

class Karma:
    """
        This needs to work differently than the other commands. 
        It needs to run passively over all messages. 
    """
    def __init__(self, json_utility):
        self.json_utility = json_utility
 
    def process_commands(self, commands):
        karma_changed_entities = [word for word in commands if 
            word.endswith('++') 
            or word.endswith('--') 
            or word.endswith('+-') 
            or word.endswith('-+')
        ]
        data_file = self.json_utility.load_or_create_file(FILENAME, INITIAL_STRUCTURE) 
        for entity in karma_changed_entities:
            self._perform_update(entity, data_file)        
        # build and return the messaging
        return self._build_response(karma_changed_entities, data_file)
    
    def _process_name(self, entity):
        entity = entity.strip('@+-') # remove all mentions, plusses and minuses
        return entity

    def _perform_update(self, entity, data_file):
        """
        TODO: This should be more robust than it is
        TODO: Also add comments
        """
        if len(entity) < 3:
            return
        modifier = entity[-2:]
        if modifier == '++':
            cleaned_entity = self._process_name(entity)
            self._add_or_update_name(data_file, cleaned_entity, 1)
        elif modifier == '--':
            cleaned_entity = self._process_name(entity)
            self._add_or_update_name(data_file, cleaned_entity, -1)
        self.json_utility.write_to_file(FILENAME, data_file)

    def _add_or_update_name(self, data_file, entity, amt_to_add):
        if entity not in data_file:
            data_file[entity] = 0
        data_file[entity] += amt_to_add

    def _build_response(self, entities, data_file):
        response = []
        for entity in entities:
            cleaned_entity = self._process_name(entity)
            response.append(cleaned_entity + "'s karma is now at *" + str(data_file[cleaned_entity]) + '*')
        return '\n'.join(response)