import logging
import requests
import application.summary.texts.verbalizer as vb
import application.summary.resources.wikipedia as kg_wikipedia
import application.summary.resources.dbpedia as kg_dbpedia
import application.summary.resources.d4c as db_d4c

class Splitter:
	
	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Splitter ...")
		
	def get_documents(self,sentences,max_lenght=427):
		counter = 0
		doc_sentences = []
		documents = []
		for s in sentences:
			num_tokens = len(s.split(" "))	
			if ((counter + num_tokens) > max_lenght):
				document = " . ".join(doc_sentences)
				documents.append(document)
				doc_sentences = []
				counter = 0
			doc_sentences.append(s)
			counter += num_tokens
		if (len(doc_sentences)>0):
			document = " . ".join(doc_sentences)
			documents.append(document)
		return documents