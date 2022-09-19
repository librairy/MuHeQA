import test_logger
import application.summary.summarizer as sm
import application.evidence.discoverer as ds

summarizer = sm.Summarizer()
discoverer = ds.Discoverer()

question = "What position does Carlos Gomez play?"

print("Question:",question)


sentences = summarizer.get_sentences(question,max_resources=3,wikipedia=True,dbpedia=True,d4c=True,by_name=True,by_properties=True,by_description=True)

evidences = discoverer.get_evidences(question,sentences,max=3)


print("#### EVIDENCES: ")
for e in evidences:
	print("Evidence: ", e)
