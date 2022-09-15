import test_logger
import application.summary.kg.wikipedia as wk

wiki = wk.Wikipedia()

entity = "Q474959"
properties = wiki.get_properties(entity)

print("Entity:", entity)
print("Properties:", properties)

label = "myalgia"
resources = wiki.get_resources(label)

print("Num Resources:", len(resources))
for resource in resources:
	print("Resource:",resource)