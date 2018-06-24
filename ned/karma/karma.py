import os

from utility.json_utility import load_json_into_dict
from utility.json_utility import write_to_file
from utility.json_utility import load_or_create_file

FILENAME = './karma/karma.json'
INITIAL_STRUCTURE = {}

class Karma:
    """
        This needs to work differently than the other commands. 
        It needs to run passively over all messages. 
    """ 
    def process_commands(self, commands):
        karma_changed_entities = [word for word in commands if 
            word.endswith('++') 
            or word.endswith('--') 
            or word.endswith('+-') 
            or word.endswith('-+')
        ]
        data_file = load_or_create_file(FILENAME, INITIAL_STRUCTURE) 
        for entity in karma_changed_entities:
            self._perform_update(entity, data_file)        
        # build and return the messaging
        response = self._build_response(karma_changed_entities, data_file)
        return response if response != '' else None
    
    def _process_name(self, entity):
        entity = entity.strip('@+-') # remove all mentions, plusses and minuses
        entity = entity.lower()
        return entity

    def _perform_update(self, entity, data_file):
        cleaned_entity = self._process_name(entity)
        if cleaned_entity == '':
            return
        modifier = entity[-2:]
        if modifier == '++':
            self._add_or_update_name(data_file, cleaned_entity, 1)
        elif modifier == '--':
            self._add_or_update_name(data_file, cleaned_entity, -1)
        write_to_file(FILENAME, data_file)

    def _add_or_update_name(self, data_file, entity, amt_to_add):
        if entity not in data_file:
            data_file[entity] = 0
        data_file[entity] += amt_to_add

    def _build_response(self, entities, data_file):
        response = []
        for entity in entities:
            cleaned_entity = self._process_name(entity)
            if cleaned_entity == '':
                continue
            response.append(cleaned_entity + "'s karma is now at *" + str(data_file[cleaned_entity]) + '*')
        # this will be '' if there were no entities besides, eg, ' ++ '
        return '\n'.join(response)