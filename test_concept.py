import test_logger
import application.summary.keywords.concept as cc

concept = cc.Concept()


query = "What is the advantage of the VEE replicon system?"

print(query)
for r in concept.get(query):
	print("Concept:", r)
