import test_logger
import application.summary.summarizer as sm


query = "What drugs is used to treat schizophrenia?"


summarizer = sm.Summarizer()
texts = summarizer.get_sentences(query,max_resources=5,wikipedia=False,dbpedia=True,d4c=False,by_name=True,by_properties=True,by_description=True)
#print("Summary sentences: ", texts)