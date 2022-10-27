import logging
import requests
import application.cache as ch
import application.summary.keywords.concept as cp
import application.summary.keywords.discovery as kw
import application.summary.texts.verbalizer as vb
import application.summary.resources.wikipedia as kg_wikipedia
import application.summary.resources.dbpedia as kg_dbpedia
import application.summary.resources.d4c as db_d4c

class Summarizer:
	
	def __init__(self):
		self.cache = ch.Cache("Summarizer")
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Summarizer ...")
	
		self.concept 	= cp.Concept()
		self.discovery 	= kw.Discovery()		
		self.verbalizer = vb.Verbalizer()		
		self.wikipedia 	= kg_wikipedia.Wikipedia()
		self.dbpedia 	= kg_dbpedia.DBpedia()
		self.d4c 		= db_d4c.D4C()



	def get_sentences(self,query,max_resources=5,wikipedia=True,dbpedia=True,d4c=True,by_name=True,by_properties=True,by_description=True):
		key = query + str(max_resources) + str(wikipedia) + str(dbpedia) + str(d4c) + str(by_name) + str(by_properties) + str(by_description)
		if (self.cache.exists(key)):
			return self.cache.get(key)

		# Create Summary
		sentences = []

		## Keywords to search KG Resources
		keywords = self.discovery.get_keywords(query)
		if ((len(keywords['entities']) == 0) and (len(keywords['concepts']) == 0)):
			self.logger.warn("no keywords found in question")
			return sentences

		self.logger.debug("keywords: " + str(keywords))
		keys = keywords['entities']
		if (len(keys) == 0):
			keys =  keywords['concepts']
		for kw in keys:
			if (wikipedia):
				wiki_sentences = self.verbalizer.kg_to_text(self.wikipedia,query,kw,max_resources,by_name,by_properties,by_description)
				self.logger.debug("wiki sentences:" + str(wiki_sentences))
				sentences.extend(wiki_sentences)

			if (dbpedia):
				dbpedia_sentences = self.verbalizer.kg_to_text(self.dbpedia,query,kw,max_resources,by_name,by_properties,by_description)
				self.logger.debug("dbpedia sentences:" + str(dbpedia_sentences))
				sentences.extend(dbpedia_sentences)

		## Concepts to search texts
		if (d4c):

			self.logger.debug("Concepts: " + str(keywords['concepts']))
			
			rows = 3
			if (max_resources > 1):
				rows = max_resources*2
			d4c_sentences = self.verbalizer.db_to_text(self.d4c, query, keywords['entities'], keywords['concepts'], rows)
			self.logger.debug("d4c sentences:" + str(len(d4c_sentences)))
			sentences.extend(d4c_sentences)			

		self.cache.set(key,sentences)	
		return sentences