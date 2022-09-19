import logging
import requests
import application.cache as ch

from SPARQLWrapper import SPARQLWrapper, JSON


class Wikipedia:

	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Wikipedia retriever...")
		self.sparql = SPARQLWrapper("https://query.wikidata.org/sparql",agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
		self.sparql.setReturnFormat(JSON)
		self.sparql.setTimeout(timeout=60)
		self.cache = ch.Cache("Wikipedia")

	def get_property_value(self,filter):
		if (self.cache.exists(filter)):
			return self.cache.get(filter)
		query = """
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX bd: <http://www.bigdata.com/rdf#>
		PREFIX wd: <http://www.wikidata.org/entity/> 
		PREFIX wdt: <http://www.wikidata.org/prop/direct/>
		PREFIX wikibase: <http://wikiba.se/ontology#>
		SELECT distinct ?obj ?objLabel
		WHERE
		FILTER 
		LIMIT 250
		"""
		query_text = query.replace('FILTER',filter)
		self.sparql.setQuery(query_text)
		result = []
		while (len(result) == 0):
			try:
				ret = self.sparql.queryAndConvert() 
				for r in ret["results"]["bindings"]:
					id = r['obj']['value']
					value = id
					if ('objLabel' in r) and ('value' in r['objLabel']):
						value = r['objLabel']['value']                
					if (' id ' not in value.lower()) and (' link ' not in value.lower()) and ('has abstract' not in value.lower()) and ('wiki' not in value.lower()) and ('instance of' not in value.lower()):
						result.append({'id':id, 'value':value})
			except Exception as e:
				print("Error on wikidata property value query:",e,"->",query_text)
			break
		self.cache.set(filter,result)
		return result	


	def get_forward_property_value(self,entity,property): 
		query_filter = """
			{
				wd:ENTITY wdt:PROPERTY ?obj .
				SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
			}                            
			"""
		return self.get_property_value(query_filter.replace("ENTITY",entity).replace("PROPERTY",property))

	def get_backward_property_value(self,entity,property):
		query_filter = """
			{
				?obj wdt:PROPERTY wd:ENTITY .
				SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
			}                            
			"""
		return self.get_property_value(query_filter.replace("ENTITY",entity).replace("PROPERTY",property))	


	def get_properties(self, entity):
	  if (self.cache.exists(entity)):
	    return self.cache.get(entity)
	  query = """
	      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
	      PREFIX wd: <http://www.wikidata.org/entity/> 
	      SELECT distinct ?prop ?propLabel
	      WHERE
	      {
	        { wd:ENTITY ?a ?b }
	              union
	              { ?s ?a wd:ENTITY } .

	        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 
	        ?prop wikibase:directClaim ?a .
	      } 
	      LIMIT 250
	      """
	  query_text = query.replace('ENTITY',entity)
	  self.sparql.setQuery(query_text)
	  result = []
	  try:
	        ret = self.sparql.queryAndConvert()
	        for r in ret["results"]["bindings"]:
	            if ('propLabel' in r) and ('value' in r['propLabel']):
	                    value = r['propLabel']['value']
	                    id = r['prop']['value'].split("http://www.wikidata.org/entity/")[1]
	                    if ('id' not in value.lower()) and ('link' not in value.lower()) and ('has abstract' not in value.lower()) and ('wiki' not in value.lower()) and ('instance of' not in value.lower()):
	                        result.append({'id':id, 'value':value})
	  except Exception as e:
	        print("Error on wikidata property query:",e,"->",query_text)           
	  self.cache.set(entity,result)
	  return result

	def find_resources(self, label):
		self.logger.debug("getting summary from Wikipedia for resource:" + label)
		if (label==""):
			return candidates
		if (self.cache.exists(label)):
			return self.cache.get(label)
		candidates = []
		headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		query_path = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=QUERY_TEXT&language=en&limit=10&type=item&format=json"
		request = query_path.replace("QUERY_TEXT",label)
		r = requests.get(request,headers = headers)
		if (len(r.json()['search']) == 0):
			lemma = lemmatize(label)	
			self.logger.debug("retry search by lemma:" + str(lemma))
			r = requests.get(query_path.replace("QUERY_TEXT",lemma))
			size = len(label.split(" "))
			index = 1
			while(('search' in r.json()) and (len(r.json()['search']) == 0) and (index<size)):
				query_label = " ".join(label.split(" ")[index:])
				index += 1  
				self.logger.debug("retry search by Partial Label:" + query_label)
				r = requests.get(query_path.replace("QUERY_TEXT",query_label)) 
		for answer in r.json()['search']:
			description = ""
			if ('description' in answer['display']):
				description = answer['display']['description']['value']
				if 'disambiguation' in description:
					continue
			candidate = {
				'label': answer['display']['label']['value'],
				'id':answer['id'],
				'description' : description,
				'properties' : self.get_properties(answer['id'])
				}
			candidates.append(candidate)
		self.cache.set(label,candidates)	    
		return candidates  

