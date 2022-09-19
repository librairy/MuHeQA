import logging
import requests
import unidecode
import application.cache as ch

from SPARQLWrapper import SPARQLWrapper, JSON


class DBpedia:

    def __init__(self):
        self.logger = logging.getLogger('muheqa')
        self.logger.debug("initializing DBpedia retriever...")
        self.sparql = SPARQLWrapper(
            "https://dbpedia.org/sparql/", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
        self.sparql.setReturnFormat(JSON)
        self.sparql.setTimeout(timeout=60)
        self.cache = ch.Cache("DBpedia")

    def get_property_value(self, filter):
        if (self.cache.exists(filter)):
            return self.cache.get(filter)
        query = """
			PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
			PREFIX dbr: <http://dbpedia.org/resource/> 
			select distinct ?object ?label {
			{ FILTER }
			optional { 
			?object rdfs:label ?label .
			filter langMatches(lang(?label), 'en')
			}
			}
			LIMIT 250
		"""
        query_text = query.replace('FILTER', filter)
        self.sparql.setQuery(query_text)
        result = []
        while (len(result) == 0):
            try:
                ret = self.sparql.queryAndConvert()
                for r in ret["results"]["bindings"]:
                    id = r['object']['value']
                    value = id
                    if ('label' in r) and ('value' in r['label']):
                        value = r['label']['value']
                    if (' id ' not in value.lower()) and (' link ' not in value.lower()) and ('has abstract' not in value.lower()) and ('wiki' not in value.lower()) and ('instance of' not in value.lower()):
                        result.append(
                            {'id': id, 'value': unidecode.unidecode(value).replace("\n*","")})
            except Exception as e:
                print("Error on wikidata property value query:",
                      e, "->", query_text)
            break
        self.cache.set(filter, result)
        return result

    def get_forward_property_value(self, entity, property):
        query_filter = "<http://dbpedia.org/resource/ENTITY> <PROPERTY> ?object"
        return self.get_property_value(query_filter.replace("ENTITY", entity).replace("PROPERTY", property))

    def get_backward_property_value(self, entity, property):
        query_filter = "?object <PROPERTY> <http://dbpedia.org/resource/ENTITY>"
        return self.get_property_value(query_filter.replace("ENTITY", entity).replace("PROPERTY", property))

    def get_properties(self, entity):
        if (self.cache.exists(entity)):
            return self.cache.get(entity)
        query = """
	  		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
	  		PREFIX dbr: <http://dbpedia.org/resource/> 
	  		select distinct ?property ?label {
	  			{ <http://dbpedia.org/resource/ENTITY> ?property ?o }
	  			union
	  			{ ?s ?property <http://dbpedia.org/resource/ENTITY> }
	  			optional { 
	  			?property rdfs:label ?label .
	  			filter langMatches(lang(?label), 'en')
	  		}
	  		filter(regex(?property, "property", "i" )) 
  			}
  			LIMIT 250
  			"""
        query_text = query.replace('ENTITY', entity)
        self.sparql.setQuery(query_text)
        result = []
        try:
            ret = self.sparql.queryAndConvert()
            for r in ret["results"]["bindings"]:
                if ('label' in r) and ('value' in r['label']):
                    value = r['label']['value']
                    id = r['property']['value']
                    if ('id' not in value.lower()) and ('link' not in value.lower()) and ('has abstract' not in value.lower()) and ('wiki' not in value.lower()) and ('instance of' not in value.lower()):
                        result.append({'id': id, 'value': value})
        except Exception as e:
            print("Error on dbpedia property query:", e, "->", query_text)
        self.cache.set(entity, result)
        return result

    def find_resources(self, label):
        self.logger.debug("getting summary from DBpedia for resource:" + label)
        if (label == ""):
            return candidates
        if (self.cache.exists(label)):
            return self.cache.get(label)
        candidates = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        query_path = "https://lookup.dbpedia.org/api/search?format=JSON&query=QUERY_TEXT&maxResults=10"
        request = query_path.replace("QUERY_TEXT", label)
        r = requests.get(request, headers=headers)
        if (len(r.json()['docs']) == 0):
            r = requests.get(query_path.replace(
                "QUERY_TEXT", lemmatize(label)))
            size = len(label.split(" "))
            index = 1
            while(('search' in r.json()) and (len(r.json()['search']) == 0) and (index < size)):
                query_label = " ".join(label.split(" ")[index:])
                index += 1
                r = requests.get(query_path.replace("QUERY_TEXT", query_label))
        for answer in r.json()['docs']:
            description, label, id = "", "", ""
            properties = []
            if ('comment' in answer) and (len(answer['comment']) > 0):
                description = answer['comment'][0].replace(
                    "<B>", "").replace("</B>", "")
            if ('resource' in answer) and (len(answer['resource']) > 0):
                id = answer['resource'][0].split(
                    "http://dbpedia.org/resource/")[1]
                properties = self.get_properties(id)
            if ('label' in answer) and (len(answer['label']) > 0):
                label = answer['label'][0].replace(
                    "<B>", "").replace("</B>", "")
            else:
                label = id
            candidate = {
                'label': label,
                'id': id,
                'description': description,
                'properties': properties
            }
        candidates.append(candidate)
        self.cache.set(label, candidates)
        return candidates
