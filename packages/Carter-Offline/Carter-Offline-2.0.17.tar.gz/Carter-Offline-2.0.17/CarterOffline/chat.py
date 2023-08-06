from Janex import *

intents_file_path = "./intents.json"
thesaurusfp = "thesaurus.json"

matcher = IntentMatcher(intents_file_path, thesaurusfp)

user_input = input("You: ")

intent_class = matcher.pattern_compare(user_input)
response, sim = matcher.response_compare(user_input, intent_class)
print(response)
