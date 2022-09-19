import test_logger
import application.summary.concept as cc

concept = cc.Concept()


query = "What position does Carlos Gomez play?"
keyword = "Carlos Gomez"


for r in concept.get(query):
	print("Concept:", r)
