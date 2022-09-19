import logging
import requests
import application.cache as ch
from transformers import pipeline

class Retriever:
	
	def __init__(self):
		self.logger = logging.getLogger('muheqa')
		self.logger.debug("initializing Retriever ...")
		self.cache = ch.Cache("Retriever")

		self.logger.debug("loading eqa language model ...")
		#qa_language_model = "deepset/roberta-base-squad2-covid" #roberta-covid
		qa_language_model = "deepset/roberta-base-squad2" #roberta
		self.question_answerer = pipeline("question-answering", model=qa_language_model, tokenizer=qa_language_model)
		
	def get_evidence(self,question,context):
		evidence = {}
		try:
			if (len(context) == 0):
				return evidence
			result = self.question_answerer(question=question, context=context, min_answer_len=1, max_answer_len=100)
			score = round(result['score'], 1)			
			evidence['value']=result['answer'].replace(","," ")
			evidence['score']=score
			evidence['summary']=context
			evidence['start']=result['start']
			evidence['end']=result['end']			
		except Exception as e:
			print("Error extracting evidence:",e)
		return evidence
