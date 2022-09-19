import logging

import application.summary.keywords.concept as cp
import application.summary.keywords.entity as ent
import unidecode

class Discovery:

	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Keyword Discovery class instance...")

		self.entity_discovery = ent.Entity()
		self.concept_discovery = cp.Concept()

	def unicase(self,label):
  		return unidecode.unidecode(label.strip()).lower()

	def get(self,text):
		entities = self.entity_discovery.get(text)
		concepts = [self.unicase(e) for e in self.concept_discovery.get(text)]
		self.logger.debug("getting keywords from the entities:" + str(entities) + " and the concepts:" + str(concepts))
		if (len(entities) == 0):
			self.logger.debug("no entities found")
			return concepts
		keywords = []
		for e in entities:
			keyword = e
			for c in concepts:
				if (e in c):
					keyword = c
			keywords.append(keyword)	
		if (len(keywords)>0):
			return list(set(keywords))
		return entities		
