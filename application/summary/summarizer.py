import logging
import requests
import application.cache as ch
import application.summary.texts.verbalizer as vb
import application.summary.resources.wikipedia as kg_wikipedia
import application.summary.resources.dbpedia as kg_dbpedia
import application.summary.resources.d4c as db_d4c

class Summarizer:
	
	def __init__(self):
		self.cache = ch.Cache("Summarizer")
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Summarizer ...")
		
		self.verbalizer = vb.Verbalizer()		
		self.wikipedia 	= kg_wikipedia.Wikipedia()
		self.dbpedia 	= kg_dbpedia.DBpedia()
		self.d4c 		= db_d4c.D4C()



	def get_texts(self,query,keyword,max=5,wikipedia=True,dbpedia=True,d4c=True,by_name=True,by_properties=True,by_description=True):
		key = query + keyword + str(max)
		if (self.cache.exists(query)):
			return self.cache.get(query)
		sentences = []
		if (wikipedia):
			wiki_sentences = self.verbalizer.kg_to_text(self.wikipedia,query,keyword,max,by_name,by_properties,by_description)
			self.logger.debug("wiki sentences:" + str(wiki_sentences))
			sentences.extend(wiki_sentences)

		if (dbpedia):
			dbpedia_sentences = self.verbalizer.kg_to_text(self.dbpedia,query,keyword,max,by_name,by_properties,by_description)
			self.logger.debug("dbpedia sentences:" + str(dbpedia_sentences))
			sentences.extend(dbpedia_sentences)

		if (d4c):
			rows = max * 5
			d4c_sentences = self.verbalizer.db_to_text(self.d4c, query, keyword,rows)
			self.logger.debug("d4c sentences:" + str(d4c_sentences))
			sentences.extend(d4c_sentences)			

		return sentences