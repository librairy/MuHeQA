import logging
import requests
import application.cache as ch
from transformers import pipeline

class Retriever:
	
	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Retriever ...")
		self.cache = ch.Cache("Retriever")

		self.logger.debug("loading eqa language models ...")
		#qa_language_model = "deepset/roberta-base-squad2-covid" #roberta-covid
		#qa_language_model = "deepset/roberta-base-squad2" #roberta
		#qa_language_model = "shaina/covid_qa_mpnet" #CoQUAD
		qa_language_models = ["deepset/roberta-base-squad2","shaina/covid_qa_mpnet"]
		self.qa_pipes = []	
		for lm in qa_language_models:
			self.qa_pipes.append(pipeline("question-answering", model=lm, tokenizer=lm))
		
		
	def get_evidences(self,question,context):
		evidences = []
		values = []
		for pipe in self.qa_pipes:
			evidence = {}
			try:
				if (len(context) == 0):
					return evidence
				result = pipe(question=question, context=context, min_answer_len=1, max_answer_len=100)
				score = round(result['score'], 1)
				value = result['answer']
				if (value not in values):
					values.append(value)			
					evidence['value']=result['answer']
					evidence['score']=score
					evidence['summary']=context
					evidence['start']=result['start']
					evidence['end']=result['end']			
					evidences.append(evidence)					
			except Exception as e:
				print("Error extracting evidence:",e)
		return evidences
