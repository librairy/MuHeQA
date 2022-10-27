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

	def get_keywords(self,text):
		concepts = [self.unicase(e) for e in self.concept_discovery.get(text)]
		result = { 'entities':[], 'concepts':concepts}
		entities = self.entity_discovery.get(text)
		for e in entities:
			extended_entity = e
			for c in concepts:
				if (e in c):
					extended_entity = c
			if (extended_entity not in result['entities']):
				result['entities'].append(extended_entity)			
		return result