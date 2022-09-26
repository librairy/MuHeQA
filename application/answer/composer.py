import logging
import application.answer.analysis.classifier as cl
import application.answer.generation.model as mo

class Composer:
	
	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Composer ...")
		
		self.model 			= mo.ModelEN()
		self.classifier 	= cl.QuestionClassifier("./resources_dir")


	def get_answers(self, question, evidences, max=3):
		category = self.classifier.get_category(question)
		self.logger.debug("Question Analysis: " + str(category))
		answers = []
		for e in evidences:
			answer = self.model.get_response(category,e)
			answers.append(answer)
		return answers[:max]
