import test_logger
import application.evidence.responses.retriever as rt
import application.evidence.documents.splitter as sp

splitter = sp.Splitter()
retriever = rt.Retriever()

question 	= "What medicines treat Covid-19?"
context 	= ['The has cause of COVID-19 pandemic is SARS-CoV-2', 'The number of deaths of COVID-19 pandemic is 5501000','The vaccine for of COVID-19 vaccine is COVID-19','The possible treatment of COVID-19 is immunoglobulin therapy, oxygen therapy, immunotherapy, antiserum, antiviral drug, symptomatic treatment, immunosuppressive drug']



print("Question:",question)


for doc in splitter.get_documents(context,max_lenght=100):
	evidence = retriever.get_evidence(question,doc)
	print("Evidence:", evidence)
