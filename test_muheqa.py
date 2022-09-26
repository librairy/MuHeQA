import test_logger
import application.pipe as pp

pipe = pp.Pipe()


question  = "What position does Carlos Gomez play in a football match?"
answers   = pipe.get_responses(question,max_answers=3)

print("#### ANSWERS: ")
for a in answers:
	print("Answer:",a)
