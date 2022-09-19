import test_logger
import application.summary.summarizer as sm

summarizer = sm.Summarizer()


query = "What position does Carlos Gomez play?"
keyword = "Carlos Gomez"




texts = summarizer.get_texts(query,keyword,max=5,wikipedia=True,dbpedia=True,d4c=True,by_name=True,by_properties=True,by_description=True)
print("Texts: ", texts)