import logging
import requests
import application.cache as ch
import nltk
nltk.download('omw-1.4')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import unidecode


class Graph:

	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Graph Explorer...")
		self.cache = ch.Cache("Graph")
		self.logger.debug("loading sentence-transformer...")
		self.sentence_model = SentenceTransformer("sentence-transformers/all-distilroberta-v1")
		self.logger.debug("loading wordnet lemmatizer...")
		self.lemmatizer = WordNetLemmatizer()

	def lemmatize(self, text):
	    result = []
	    for token in text.split(" "):
	    	result.append(self.lemmatizer.lemmatize(token))
	    return " ".join(result)

	def sort_by_similarity(self,ref_text,texts):
		cache_key = "sort_by_similarity"+ref_text + ",".join(texts)
		if (self.cache.exists(cache_key)):
			return self.cache.get(cache_key)
		sentences = [unidecode.unidecode(ref_text.strip())]
		sentences.extend([unidecode.unidecode(t.strip()) for t in texts])
		embeddings = self.sentence_model.encode(sentences)
		sim_list = []
		index=0
		for e in embeddings[1:]:
			ref = embeddings[0]
			score = cosine_similarity([ref], [e])
			score_val = round(score[0][0], 1)
			sim_list.append({'id':index, 'text':texts[index], 'score':score_val})  
			index+=1
		sim_list.sort(key=lambda x: x.get('score'),reverse=True)
		self.cache.set(cache_key,sim_list)
		return sim_list

	def get_top_similar(self,ref_text,resources,max=-1):
		top_resources = []
		if (len(resources) == 0):
			return top_resources
		cache_key = "get_top_similar"+ref_text + str(max) + ",".join([c['text'] for c in resources])
		if (self.cache.exists(cache_key)):
			return self.cache.get(cache_key)	
		sorted_resources = self.sort_by_similarity(ref_text,[c['text'] for c in resources])  
		best_score = sorted_resources[0]['score']
		for index, c in enumerate(sorted_resources):
			if (max < 0) or (index < max) or (c['score'] == best_score):
				candidate = resources[c['id']]
				candidate['score'] = c['score']
				top_resources.append(candidate)
		self.cache.set(cache_key,top_resources)
		return top_resources

	def get_top_resources(self,context,label,candidates,max=-1,by_name=True,by_properties=True,by_description=True):
		if (len(candidates) == 0):
			return []
		
		# initialize score		
		sorted_candidates = []	
		for c in candidates:
			candidate = c
			candidate['score'] = 1.0
			sorted_candidates.append(candidate)


		# filter by similar resource name and label
		if (by_name):
			names = [ {'id':i, 'text':c['label'] } for i,c in enumerate(candidates)]
			top_candidates_by_name = self.get_top_similar(label,names,max)
			sorted_candidates = []
			for t in top_candidates_by_name:
				candidate = candidates[t['id']]
				# normalize score
				candidate['score'] = t['score']
				sorted_candidates.append(candidate)
  		
		# filter by similar resource propery and context
		if(by_properties):
			properties = []
			for i,c in enumerate(sorted_candidates):
				for p in c['properties']:
					properties.append({'id':i, 'text':p['value'] })
			top_candidates_by_prop = self.get_top_similar(context.replace(label,""),properties,-1) 
			new_sorted_candidates = []
			for t in top_candidates_by_prop:
				candidate = sorted_candidates[t['id']]
				# only the best property is considered
				if (candidate not in new_sorted_candidates):
					# normalize score
					candidate['score'] = (2*candidate['score'] + 4*t['score']) / 6.0
					new_sorted_candidates.append(candidate)
			sorted_candidates = new_sorted_candidates[:max]

		# filter by similar resource description and context
		if(by_description):
			descriptions = [ {'id':i, 'text':c['description'] } for i,c in enumerate(sorted_candidates)]
			top_candidates_by_desc = self.get_top_similar(context.replace(label,""),descriptions,max)
			new_sorted_candidates = []    
			for t in top_candidates_by_desc:
				candidate = sorted_candidates[t['id']]
				# only the best description is considered
				if (candidate not in new_sorted_candidates):
					# normalize score
					candidate['score'] = (2*candidate['score'] + 1*t['score']) / 3.0
					new_sorted_candidates.append(candidate)
			sorted_candidates = new_sorted_candidates
		return sorted_candidates
	
		