import test_logger
import application.pipe as pp
import coloredlogs, logging
import application.logformatter as lf

logging.getLogger('muheqa').setLevel(logging.INFO)


pipe = pp.Pipe()

counter = 1
out = open("./datasets/ConvQA/test/test.responses", "a")
with open('./datasets/ConvQA/test/test.source') as f:
	for q in f.readlines():
		print(counter,":",q)
		counter += 1
		if (counter < 1801):
			continue
		answers   = pipe.get_responses(q,max_answers=1,wikipedia=False,dbpedia=False,d4c=True)
		if (len(answers)>0):
			answer = str(answers[0]['answer'])
			print("\t",answer)
			out.write(answer)
		out.write("\n")				
out.close()

