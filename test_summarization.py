import test_logger
import application.summary.summarizer as sm


query = "What drugs is used to treat schizophrenia?"


summarizer = sm.Summarizer()
texts = summarizer.get_sentences(query,max_resources=3,wikipedia=True,dbpedia=True,d4c=True,by_name=True,by_properties=True,by_description=True)
print("Summary sentences: ", texts)