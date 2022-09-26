from typing import Union
from fastapi import FastAPI
import application.pipe as pp

import coloredlogs, logging
import application.logformatter as lf

log_level = logging.DEBUG

fh = logging.StreamHandler()
fh.setFormatter(lf.CustomFormatter())
fh.setLevel(log_level)

logger = logging.getLogger('muheqa')
logger.addHandler(fh)
logger.setLevel(log_level)


logging.getLogger().setLevel(log_level)


pipe = pp.Pipe()
app = FastAPI()

@app.get("/")
def read_root():
	return { "Hello":"World"}

@app.get("/answers")
def read_item(q: Union[str, None] = None, max: Union[int, None] = None, wiki: Union[bool, None] = True, dbpedia: Union[bool, None] = True, d4c: Union[bool, None] = True):
	question = { 'q':q, 'max':max, 'wiki':wiki, 'dbpedia':dbpedia, 'd4c':d4c}
	logger.info("New question: " + str(question) + "...")
	answers = pipe.get_responses(q,max_answers=max,max_resources=3,wikipedia=wiki,dbpedia=dbpedia,d4c=d4c)
	return answers