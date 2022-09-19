import logging
import requests
import application.summary.texts.verbalizer as vb
import application.summary.resources.wikipedia as kg_wikipedia
import application.summary.resources.dbpedia as kg_dbpedia
import application.summary.resources.d4c as db_d4c

class Ranking:
	
	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Ranking ...")

	def get_top_evidences(self,evidences,n=1):
		if (len(evidences)<2):
			return evidences
		evidences.sort(key=lambda x: x.get('score'),reverse=True)
		best_score = evidences[0]['score']
		top_evidences = []
		for index, c in enumerate(evidences):
			if (n < 0) or (index < n) or (c['score'] == best_score):
				top_evidences.append(c)
		return top_evidences
		
