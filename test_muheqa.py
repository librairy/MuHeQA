import test_logger
import application.pipe as pp

pipe = pp.Pipe()


question  = "Why can't Belva use u'10.0.0.0' to make a single code work with both Python 2 and Python 3?"
answers   = pipe.get_responses(question,max_answers=5,wikipedia=False,dbpedia=False,d4c=True)

print("#### ANSWERS: ")
for a in answers:
	print("Answer:",a)
