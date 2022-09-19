import test_logger
import application.summary.resources.graph as kg_graph

graph = kg_graph.Graph()


query 	= "What position does Carlos Gomez play?"
texts 	= [ 'name','birth place','after','awards','before','birth date','caption','finaldate','image size','position','teams', 'title','years', 'br','bats', 'brm', 'debutdate', 'debutleague', 'debutteam', 'debutyear', 'espn', 'fangraphs', 'finalleague', 'finalteam', 'finalyear', 'mlb', 'stat1value']

result = graph.sort_by_similarity(query,texts)
print(result)


resources = [{ 'text':t} for t in texts]
result2 = graph.get_top_similar(query,resources)
print(result2)




