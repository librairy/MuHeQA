import test_logger
import application.summary.summarizer as sm
import application.evidence.discoverer as ds

summarizer = sm.Summarizer()
discoverer = ds.discoverer()



query = "What position does Carlos Gomez play?"

print("Query:",query)


sentences = summarizer.get_texts(query,max=5,wikipedia=True,dbpedia=True,d4c=True,by_name=True,by_properties=True,by_description=True)

discoverer.get_evidences(sentences,max=3)
