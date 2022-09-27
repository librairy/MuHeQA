import logging
import application.cache as ch
import application.summary.resources.graph as kg_graph
import application.summary.resources.wikipedia as kg_wikipedia
import application.summary.resources.dbpedia as kg_dbpedia
import application.summary.resources.d4c as db_d4c



class Verbalizer:

	def __init__(self):
		self.cache 		= ch.Cache("Verbalizer")
		self.logger 	= logging.getLogger('muheqa')
		self.logger.debug("initializing Verbalizer ...")
		self.graph 		= kg_graph.Graph()
		
	def property_to_text(self,s,p,o):
		if (len(o)==0):
			return ""
		property_value = o
		if (len(o)>0):
			property_value = ", ".join(o)		
		tokens = ["The",p,"of",s,"is",property_value]   
		return " ".join(tokens)
	

	def kg_to_text(self,kg,query,keyword,max_resources=5,by_name=True,by_properties=True,by_description=True):
		sentences = []
		
		# find related resources
		kg_resources = kg.find_resources(keyword)	

		# sort resources by name, properties and description
		top_resources = self.graph.get_top_resources(query,keyword,kg_resources,max_resources,by_name,by_properties,by_description)
		
		# get top properties for each resource
		for resource in top_resources:
			self.logger.debug("Top Resource: '" + str(resource['id'])+ "'")
			if ('properties' in resource):
				properties = [{ 'id':r['id'] , 'text':r['value']} for r in resource['properties']]
				top_properties = self.graph.get_top_similar(query.replace(keyword,""),properties, 5)
				self.logger.debug("top properties" + str(top_properties) + " from resource: " + str(resource['id']))
				for p in top_properties:
					self.logger.debug("verbalizing property" + str(p))
					fw_values = kg.get_forward_property_value(resource['id'],p['id'])
					if (len(fw_values)>0):
						t = self.property_to_text(resource['label'],p['text'],[o['value'] for o in fw_values])
						sentences.append(t)						

					#bw_values = kg.get_backward_property_value(resource['id'],p['id'])	
					#if (len(bw_values)>0):
					#	t = self.property_to_text(resource['label'],p['text'],[o['value'] for o in bw_values])
					#	sentences.append(t)
		return sentences

	def db_to_text(self, db, query, keywords,max_texts=5):
		db_texts = db.find_texts(query,keywords,max_texts)
		self.logger.debug("DB Texts: " + str(len(db_texts)))
		return db_texts

