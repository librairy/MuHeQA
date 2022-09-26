import test_logger
import application.summary.resources.d4c as db_d4c

d4c = db_d4c.D4C()


query = "What is the treatment of Hydroxychloroquine?"
keywords = ["Hydroxychloroquine"]

resources = d4c.find_texts(query,keywords,5)
for r in resources:
	print("Resource:",r)
