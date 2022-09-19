import test_logger
import application.evidence.responses.retriever as rt
import application.evidence.documents.splitter as sp

splitter = sp.Splitter()
retriever = rt.Retriever()

question 	= "What position does Carlos Gomez play?"
context 	= ['The position played on team / speciality of Carlos Gómez is defender', 'The member of sports team of Carlos Gómez is Atlético Potosino, Club León, Puebla F.C., Mexico national football team, Club de Fútbol Monterrey', 'The family name of Carlos Gómez is Gómez', 'The given name of Carlos Gómez is Carlos', 'The occupation of Carlos Gómez is association football player', 'The position played on team / speciality of Carlos Gómez is center fielder', 'The league of Carlos Gómez is Major League Baseball', 'The member of sports team of Carlos Gómez is Minnesota Twins, Milwaukee Brewers, Nashville Sounds, Texas Rangers, Houston Astros, Tampa Bay Rays, New York Mets, Wisconsin Timber Rattlers', 'The family name of Carlos Gómez is Gómez', 'The given name of Carlos Gómez is Carlos', 'The position played on team / speciality of Carlos Gómez is midfielder', 'The member of sports team of Carlos Gómez is Cobreloa', 'The family name of Carlos Gómez is Gómez', 'The given name of Carlos Gómez is Carlos', 'The occupation of Carlos Gómez is association football player','The mlb of Carlos Gómez is 460576', 'The position of Carlos Gómez is Center fielder', 'The statleague of Carlos Gómez is MLB', 'The throws of Carlos Gómez is Right', 'The name of Carlos Gómez is Carlos Gomez', 'The name of Juan Carlos Gómez is Juan Carlos Gomez', 'The nickname of Juan Carlos Gómez is , Pantera Negra', 'The style of Juan Carlos Gómez is Southpaw stance, background:#C1D8FF; font-weight: bold;', 'The Total of Juan Carlos Gómez is 60', 'The weight of Juan Carlos Gómez is Cruiserweight (boxing), Heavyweight, ', 'The years of Juan Carlos Gómez is --02-10, --02-21, --03-27, --06-16, --07-06, --08-17, --10-19, Vacated, Won world title, Won world title eliminator', 'The dec-losses of Juan Carlos Gómez is 1', 'The dec-wins of Juan Carlos Gómez is 15', 'The ko-losses of Juan Carlos Gómez is 3', 'The ko-wins of Juan Carlos Gómez is 40', 'The losses of Juan Carlos Gómez is 4', 'The Wins of Juan Carlos Gómez is 55']

print("Question:",question)


for doc in splitter.get_documents(context,max_lenght=100):
	evidence = retriever.get_evidence(question,doc)
	print("Evidence:", evidence)
