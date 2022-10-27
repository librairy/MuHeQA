import logging
import application.summary.summarizer as sm
import application.evidence.discoverer as ds
import application.answer.composer as cp


class Pipe:

	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Pipe ...")
		
		self.summarizer = sm.Summarizer()
		self.discoverer = ds.Discoverer()
		self.composer   = cp.Composer()

	def get_responses(self,question,max_answers=3,max_resources=3,wikipedia=True,dbpedia=True,d4c=True,by_name=True,by_properties=True,by_description=True):
		self.logger.debug("Question: " + question)
		sentences = self.summarizer.get_sentences(question,max_resources,wikipedia,dbpedia,d4c,by_name,by_properties,by_description)
		if (len(sentences) == 0):
			self.logger.warn("no summary created")
			return sentences
		evidences = self.discoverer.get_evidences(question,sentences,max_answers)
		self.logger.debug("Evidences: " + str(evidences))
		answers   = self.composer.get_answers(question,evidences,max_answers)
		self.logger.debug("Answers: " + str(answers))
		return answers

