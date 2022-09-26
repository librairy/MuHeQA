import test_logger
import application.pipe as pp

pipe = pp.Pipe()


question  = "What substance contains Hydroxychloroquine?"
answers   = pipe.get_responses(question,max_answers=3,wikipedia=False,dbpedia=False,d4c=True)

print("#### ANSWERS: ")
for a in answers:
	print("Answer:",a)
