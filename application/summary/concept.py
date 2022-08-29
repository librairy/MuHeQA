import logging

# PoS tagger
from flair.data import Sentence
from flair.models import SequenceTagger

class Concept:

	def __init__(self):
		logging.getLogger("flair").setLevel(level=logging.WARNING)
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Concept class instance...")

		pos_language_model = "flair/pos-english"
		self.ner_tagger = SequenceTagger.load(pos_language_model)
		
	def get(self,text):
		self.logger.debug("getting concepts ...")
		main_categories=['CD','NN','NNS','NNP','NNPS']
		additional_categories=['JJ','NNS','CC']
		drop_categories=['IN']

		# make sentence
		sentence = Sentence(text)

		# predict NER tags
		self.ner_tagger.predict(sentence)

		# iterate over tokens
		concepts = []
		current_concept = ""
		partial_concept = ""
		for t in sentence.tokens:
			for label in t.annotation_layers.keys():
				token = t.text
				category = t.get_labels(label)[0].value
				self.logger.debug("Token:"+ token + " [ " + category + "] ")
				if (category in main_categories):
					if (len(partial_concept) > 0 ):
						current_concept = partial_concept + " " + token
						partial_concept = ""
					elif (current_concept == ""):
						current_concept += token
					else:
						current_concept += " " + token
				elif (category in additional_categories):
					if (len(current_concept)>0):
						current_concept += " " + token
					elif (len(partial_concept)>0):
						partial_concept += " " + token
					else:
						partial_concept += token
				elif(category in drop_categories):
					current_concept = ""
					partial_concept = ""
				elif len(current_concept) > 0:
					concepts.append(current_concept)
					current_concept = ""
					partial_concept = ""
		if (len(current_concept) > 0):
			concepts.append(current_concept)
		return concepts




	
