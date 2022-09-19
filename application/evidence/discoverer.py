import logging
import requests
import application.evidence.documents.splitter as sp
import application.evidence.responses.retriever as rt
import application.evidence.candidates.ranking as rk

class Discoverer:
	
	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Discoverer ...")
		
		self.splitter 	= sp.Splitter()
		self.retriever 	= rt.Retriever()
		self.ranking 	= rk.Ranking()


	def get_evidences(self, question, summary, max=3):
		max_tokens = 25
		docs = self.splitter.get_documents(summary,max_tokens)
		evidences = []
		for d in docs:
			evidence = self.retriever.get_evidence(question, d)
			evidences.append(evidence)
		top_evidences = self.ranking.get_top_evidences(evidences,max)
		return top_evidences
