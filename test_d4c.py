import test_logger
import application.summary.resources.d4c as db_d4c

d4c = db_d4c.D4C()


query = "How many children were infected by HIV-1 in 2008-2009, worldwide?"
keywords = ["HIV-1","many children", "2008-2009"]
response = "more than 400,000 children were infected worldwide, mostly through MTCT and 90% of them lived in sub-Saharan Africa."

resources = d4c.find_texts(query,keywords,100)
for r in resources:
	print("Resource:",r)
