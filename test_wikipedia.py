import test_logger
import application.summary.kg.wikipedia as wk

wiki = wk.Wikipedia()


query = "What position does Carlos Gomez play?"
keyword = "Carlos Gomez"

resources = wiki.find_resources(keyword)

for r in resources:
	print("Resource:",r)
	entity = r['id']
	properties = wiki.get_properties(entity)
	#print("\t Properties:",properties)
