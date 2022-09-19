import test_logger
import application.answer.composer as cp


question = "What position does Carlos Gomez play?"
evidences = [
	{'value': 'defender', 'score': 0.9, 'summary': 'The position played on team / speciality of Carlos Gómez is defender', 'start': 60, 'end': 68},
	{'value': 'Center fielder', 'score': 0.9, 'summary': 'The mlb of Carlos Gómez is 460576 . The position of Carlos Gómez is Center fielder . The statleague of Carlos Gómez is MLB', 'start': 68, 'end': 82},
	 {'value': 'midfielder', 'score': 0.5, 'summary': 'The position played on team / speciality of Carlos Gómez is midfielder . The member of sports team of Carlos Gómez is Cobreloa', 'start': 60, 'end': 70}
	]


composer = cp.Composer()
answers = composer.get_answer(question, evidences)
for a in answers:
	print(a)

