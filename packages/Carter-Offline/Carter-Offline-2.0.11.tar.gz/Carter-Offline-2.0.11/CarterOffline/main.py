from Janex import *
from carterpy import Carter

class CarterOffline:
    def __init__(self, intents_file_path, CarterAPI):
        self.intents_file_path = intents_file_path
        self.CarterAPI = CarterAPI

    def SendToCarter(self, input_string, User):
        carter = Carter(self.CarterAPI)
        response = carter.say(input_string, User)
        thesaurus_file_path = "thesaurus.json"
        matcher = IntentMatcher(self.intents_file_path, thesaurus_file_path)
        intent_class, sim = matcher.pattern_compare(input_string)
        intents = matcher.train()
        response = matcher.SendToCarter(input_string, text)

        if intent_class:
                target_class = intent_class
                target_class.setdefault("patterns", []).append(input_string)
                target_class.setdefault("responses", []).append(response.output_text)
        else:
                new_class = {
                        "tag": User,
                        "patterns": [input_string],
                        "responses": [response.output_text]
                        }
                intents['intents'].append(new_class)

        with open(f"{self.intents_file_path}", 'w') as json_file:
            json.dump(intents, json_file, indent=4, separators=(',', ': '))

        return response.output_text
