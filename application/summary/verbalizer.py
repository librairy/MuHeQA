import logging
import application.cache as ch
import application.summary.kg.graph as kg_graph
import application.summary.kg.wikipedia as kg_wikipedia


class Verbalizer:

	def __init__(self):
		self.cache = ch.Cache("Verbalizer")
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Verbalizer ...")

		self.graph = kg_graph.Graph()
		self.wikipedia = kg_wikipedia.Wikipedia()
		
	def property_to_text(self,s,p,o):
		if (len(o)==0):
			return ""
		print(s,p,o)
		property_value = o
		if (len(o)>0):
			property_value = ", ".join(o)		
		tokens = ["The",p,"of",s,"is",property_value]   
		print(property_value)
		return " ".join(tokens)
		

	def get_text(self,query,keyword,max=5,wikipedia=True,dbpedia=True,d4c=True,by_name=True,by_properties=True,by_description=True):
		sentences = []
		if (wikipedia):
			wiki_resources = self.wikipedia.find_resources(keyword)
			self.logger.debug("Wikipedia Candidates: " + str(wiki_resources))
			# get top MAX resources
			top_wiki_resources = self.graph.get_top_resources(query,keyword,wiki_resources,max,by_name,by_properties,by_description)
			self.logger.debug("Top Wikipedia Resources: " + str(top_wiki_resources))
			# get top MAX properties for each resource
			for resource in top_wiki_resources:
				self.logger.debug("Wikipedia Resource: " + str(resource['id'] + str(resource['label'])))
				if ('properties' in resource):
					properties = [{ 'id':r['id'] , 'text':r['value']} for r in resource['properties']]
					top_properties = self.graph.get_top_similar(query,properties)
					for p in top_properties:
						fw_values = self.wikipedia.get_forward_property_value(resource['id'],p['id'])
						if (len(fw_values)>0):
							print(p)
							print("fw_values:",fw_values)
							print("list of fw_value:", [o['value'] for o in fw_values])
							t = self.property_to_text(resource['label'],p['text'],[o['value'] for o in fw_values])
							sentences.append(t)						

						bw_values = self.wikipedia.get_backward_property_value(resource['id'],p['id'])	
						if (len(bw_values)>0):
							t = self.property_to_text(resource['label'],p['text'],[o['value'] for o in bw_values])
							sentences.append(t)
						#self.logger.debug("backward property values: ")
						#for o in bw_values:
						#	self.logger.debug(str(o))
						#	t = self.property_to_text(resource['label'],p['text'],o['value'])
						#	sentences.append(t)	
		return sentences
