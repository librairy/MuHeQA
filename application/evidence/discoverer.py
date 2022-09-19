import logging
import requests
import application.evidence.documents.splitter as sp

class Discoverer:
	
	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Discoverer ...")
		self.splitter = sp.splitter()


	def get_evidences(self, sentences, max=3):
		docs = self.splitter.get_documents(sentences,417)
		for d in docs:
			print("Document:", d)
