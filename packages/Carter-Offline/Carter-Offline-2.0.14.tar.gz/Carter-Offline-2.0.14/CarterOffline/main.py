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

        tag = intent_class.get("tag")

        for intent_class in intents['intents']:
            if intent_class.get("tag") == tag:
                target_class = intent_class
                print(intent_class.get("tag"))

                ResponseOutput = ResponseOutput.replace(User, "")
                print(ResponseOutput)

                if target_class:
                        target_class.setdefault("patterns", []).append(original)
                        target_class.setdefault("responses", []).append(ResponseOutput)
                else:
                        new_class = {
                                "tag": User,
                                "patterns": [sentence],
                                "responses": [ResponseOutput]
                                }
                        intents['intents'].append(new_class)

                with open("intents.json", 'w') as json_file:
                    json.dump(intents, json_file, indent=4, separators=(',', ': '))

        return response.output_text
