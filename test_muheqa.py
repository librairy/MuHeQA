import test_logger
import application.pipe as pp

pipe = pp.Pipe()


question  = "What is the advantage of the VEE replicon system?"
answers   = pipe.get_responses(question,max_answers=5,wikipedia=False,dbpedia=False,d4c=True)

print("#### ANSWERS: ")
for a in answers:
	print("Answer:",a)
