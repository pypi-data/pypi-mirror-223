from Janex import *
from carterpy import Carter

class CarterOffline:
    def __init__(self, intents_file_path, CarterAPI):
        self.intents_file_path = intents_file_path
        self.CarterAPI = CarterAPI

    def SendToCarter(self, input_string, User):
        original = input_string
        sentence = input_string

        carter = Carter(self.CarterAPI)
        ResponseOutput = carter.say(sentence, User)

        ResponseOutput = ResponseOutput.output_text

        ResponseOutput = str(ResponseOutput)

        User = str(User)

        intents_file_path, thesaurus_file_path = f"{self.intents_file_path}", "thesaurus.json"

        matcher = IntentMatcher(intents_file_path, thesaurus_file_path)

        tag, similarity_percentage = matcher.pattern_compare(sentence)

        tag = tag.get("tag")

        intents = matcher.train()

        target_class = None
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

        ResponseOutput = matcher.ResponseGenerator(ResponseOutput)

        return ResponseOutput
