from main import *

intentfp, thesaurusfp, UIName = "intents.json", "thesaurus.json", "Ultron"

JanexPT = JanexPT(intentfp, thesaurusfp, UIName)

JanexPT.trainpt()
inputstr = input("You: ")
Response = JanexPT.SayToAI(inputstr, "Jack")

print(Response)
