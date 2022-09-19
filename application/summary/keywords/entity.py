import logging

# uncased NER model
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

class Entity:

	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Entity class instance...")

		self.logger.debug("loading NER model ...")
		ner_language_model = "dslim/bert-base-NER-uncased"
		ner_tokenizer = AutoTokenizer.from_pretrained(ner_language_model)
		ner_model = AutoModelForTokenClassification.from_pretrained(ner_language_model)
		self.ner_nlp = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer)

	def get(self,text):
		self.logger.debug("getting entities...")
		entities = []
		entity = ""
		index = -1
		offset = -1
		for token in self.ner_nlp(text):
			if (index == -1):
				index = token['index']
				offset = token['start']
			word = token['word']
			if (word[0] == '#'):
				word = token['word'].replace("#","")
			if (token['start']== offset):
				entity += word
			elif (token['index']-index < 2):
				entity += " " + word
			else:
				entities.append(entity)
				entity = word		
			index = token['index']
			offset = token['end']
		if (len(entity) > 0):    
			entities.append(entity)
		return entities



	