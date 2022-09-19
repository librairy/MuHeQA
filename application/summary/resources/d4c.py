import logging
from urllib.request import urlopen
import urllib.parse
import json
import unidecode
import application.cache as ch
import application.summary.keywords.concept as cc


class D4C:

	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing D4C retriever...")
		self.url = "http://librairy.linkeddata.es/solr/cord19-paragraphs"
		self.cache = ch.Cache("D4C")
		self.concept_discovery = cc.Concept()


	def find_texts(self,query,keyword,max=5):
		if (self.cache.exists(query)):
			return self.cache.get(query)
		terms = self.concept_discovery.get(query)
		if (keyword not in terms):
			terms.append(keyword)
		q = " or ".join([ "text_t:"+t for t in terms])		
		connection = urlopen(self.url + '/select?fl=text_t&q='+urllib.parse.quote(q)+'&rows='+str(max)+'&wt=json')
		response = json.load(connection)
		self.logger.debug(str(response['response']['numFound']) + " documents found.")
		sentences = []
		for document in response['response']['docs']:
			sentences.append(document['text_t'])
		self.cache.set(query,sentences)	
		return sentences

