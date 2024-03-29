import test_logger
import application.pipe as pp
import coloredlogs, logging
import application.logformatter as lf

logging.getLogger('muheqa').setLevel(logging.INFO)


pipe = pp.Pipe()

counter = 1
out = open("./datasets/CovidQA/test/test.responses", "w")
with open('./datasets/CovidQA/test/test.source') as f:
	for q in f.readlines():
		print(counter,":",q)
		answers   = pipe.get_responses(q,max_answers=1,wikipedia=False,dbpedia=False,d4c=True)
		if (len(answers)>0):
			out.write(str(answers[0]['answer']))
		out.write("\n")
		counter += 1
out.close()

