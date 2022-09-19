import logging
import application.cache as ch
import application.summary.kg.graph as kg_graph
import application.summary.kg.wikipedia as kg_wikipedia
import application.summary.kg.dbpedia as kg_dbpedia


class Verbalizer:

	def __init__(self):
		self.cache = ch.Cache("Verbalizer")
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Verbalizer ...")

		self.graph 		= kg_graph.Graph()
		self.wikipedia 	= kg_wikipedia.Wikipedia()
		self.dbpedia 	= kg_dbpedia.DBpedia()
		
	def property_to_text(self,s,p,o):
		if (len(o)==0):
			return ""
		property_value = o
		if (len(o)>0):
			property_value = ", ".join(o)		
		tokens = ["The",p,"of",s,"is",property_value]   
		return " ".join(tokens)
	

	def kg_to_text(self,kg,query,keyword,max=5,by_name=True,by_properties=True,by_description=True):
		sentences = []
		kg_resources = kg.find_resources(keyword)
		self.logger.debug("KG Candidates: " + str(len(kg_resources)))
		# get top MAX resources
		top_resources = self.graph.get_top_resources(query,keyword,kg_resources,max,by_name,by_properties,by_description)
		self.logger.debug("Top KG Resources: " + str(len(top_resources)))
		# get top MAX properties for each resource
		for resource in top_resources:
			self.logger.debug(" Resource: " + str(resource['id'] + str(resource['label'])))
			if ('properties' in resource):
				properties = [{ 'id':r['id'] , 'text':r['value']} for r in resource['properties']]
				top_properties = self.graph.get_top_similar(query,properties)
				for p in top_properties:
					fw_values = kg.get_forward_property_value(resource['id'],p['id'])
					if (len(fw_values)>0):
						t = self.property_to_text(resource['label'],p['text'],[o['value'] for o in fw_values])
						sentences.append(t)						

					bw_values = kg.get_backward_property_value(resource['id'],p['id'])	
					if (len(bw_values)>0):
						t = self.property_to_text(resource['label'],p['text'],[o['value'] for o in bw_values])
						sentences.append(t)
		return sentences


	def get_text(self,query,keyword,max=5,wikipedia=True,dbpedia=True,d4c=True,by_name=True,by_properties=True,by_description=True):
		sentences = []
		if (wikipedia):
			wiki_sentences = self.kg_to_text(self.wikipedia,query,keyword,max,by_name,by_properties,by_description)
			self.logger.debug("wiki sentences:" + str(wiki_sentences))
			sentences.extend(wiki_sentences)

		if (dbpedia):
			dbpedia_sentences = self.kg_to_text(self.dbpedia,query,keyword,max,by_name,by_properties,by_description)
			self.logger.debug("dbpedia sentences:" + str(dbpedia_sentences))
			sentences.extend(dbpedia_sentences)

		return sentences
