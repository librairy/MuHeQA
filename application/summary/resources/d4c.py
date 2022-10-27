import logging
from urllib.request import urlopen
import urllib.parse
import json
import unidecode
import application.cache as ch
import application.summary.keywords.concept as cc
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class D4C:

	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing D4C retriever...")
		self.url = "http://librairy.linkeddata.es/solr/cord19-paragraphs"
		#self.url = "http://localhost:8983/solr/documents"
		self.cache = ch.Cache("D4C")
		self.concept_discovery = cc.Concept()
		
		model_name = "castorini/monot5-base-msmarco-10k" 
		self.tokenizer = AutoTokenizer.from_pretrained(model_name)
		self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)




	def find_texts(self,query,entities, concepts, max=5):
		#if (self.cache.exists(query)):
		#	return self.cache.get(query)
		q = ""
		if (len(entities)>0):
			q += "(" + " OR ".join([ "text_t:\""+t + "\"" for t in entities]) + ")"
		
		if (len(concepts)>0):
			if (len(q)>0):
				q += " AND "
			q += "(" + " OR ".join([ "text_t:\""+t + "\"" for t in concepts]) +")"

		self.logger.debug("query => " + q)		
		connection = urlopen(self.url + '/select?fl=text_t,id&q='+urllib.parse.quote(q)+'&rows=50'+'&wt=json')
		response = json.load(connection)
		self.logger.debug( str(len(response['response']['docs'])) + "/" + str(response['response']['numFound']) + " documents found.")
		if (response['response']['numFound'] == 0) and (len(concepts)>0):
			q = "(" + " OR ".join([ "text_t:\""+t + "\"" for t in concepts]) +")"
			connection = urlopen(self.url + '/select?fl=text_t,id&q='+urllib.parse.quote(q)+'&rows=50'+'&wt=json')
			response = json.load(connection)
		sentences = []
		for document in response['response']['docs']:
			
			doc_text = document['text_t']
			
			#validate based on T5 instead of BM25 or TFIDF according to paper "Document Ranking with a Pretrained Sequence-to-Sequence Model" https://aclanthology.org/2020.findings-emnlp.63.pdf
			# castorini/monot5-base-msmarco-10k
			# castorini/monot5-3b-msmarco-10k
			input_ids = self.tokenizer(query + " " + doc_text, return_tensors="pt").input_ids  # Batch size 1
			outputs = self.model.generate(input_ids,max_new_tokens=1)
			is_valid = self.tokenizer.decode(outputs[0], skip_special_tokens=True) == "true"
			#self.logger.debug(str(is_valid))
			if (is_valid):			
				sentences.append(doc_text)
		#self.cache.set(query,sentences)	
		return sentences

