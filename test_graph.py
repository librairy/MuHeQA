import test_logger
import application.summary.kg.graph as kg_graph


graph = kg_graph.Graph()


context 	= "Which medicine treats myalgia?"
label 		= "myalgia"
labels 		= [ "delayed onset muscle soreness", "myalgia", "MYALGIA", "Myalgia cruris epidemica", "Myalgias or non-specific muscle pain in Arab or Indo-Pakistani patients may indicate vitamin D deficiency." ]


#print("Reference Context :",context)
#print("Reference Text :",label)
#print("Lemma:", graph.lemmatize(label))


result = graph.sort_by_similarity(label,labels)
#print("Sorted texts:", result)

nodes = [ {'id':i, 'text':c } for i,c in enumerate(labels)]
#print("Top Similar Nodes:", graph.get_top_similar(label,nodes,3))
#print("Top1 Similar Nodes:", graph.get_top_similar(label,nodes,1))


res_1 = {'label': 'myalgia', 'id': 'Q474959', 'description': 'muscle pain', 'properties': [{'id': 'P780', 'value': 'symptoms and signs'}, {'id': 'P2176', 'value': 'drug or therapy used for treatment'}, {'id': 'P279', 'value': 'subclass of'}, {'id': 'P921', 'value': 'main subject'}, {'id': 'P494', 'value': 'ICD-10'}, {'id': 'P557', 'value': 'DiseasesDB'}, {'id': 'P373', 'value': 'Commons category'}, {'id': 'P18', 'value': 'image'}, {'id': 'P493', 'value': 'ICD-9'}, {'id': 'P1995', 'value': 'health specialty'}, {'id': 'P672', 'value': 'MeSH tree code'}, {'id': 'P2888', 'value': 'exact match'}, {'id': 'P1343', 'value': 'described by source'}, {'id': 'P2892', 'value': 'UMLS CUI'}, {'id': 'P5137', 'value': 'item for this sense'}, {'id': 'P7807', 'value': 'ICD-11 (foundation)'}]}
res_2 = {'label': 'delayed onset muscle soreness', 'id': 'Q574415', 'description': 'pain in muscles after exercise', 'properties': [{'id': 'P921', 'value': 'main subject'}, {'id': 'P1995', 'value': 'health specialty'}, {'id': 'P279', 'value': 'subclass of'}, {'id': 'P2175', 'value': 'medical condition treated'}, {'id': 'P5137', 'value': 'item for this sense'}]}
res_3 = {'label': 'MYALGIA', 'id': 'Q84884151', 'description': 'scientific article published on 01 June 1908', 'properties': [{'id': 'P478', 'value': 'volume'}, {'id': 'P1476', 'value': 'title'}, {'id': 'P407', 'value': 'language of work or name'}, {'id': 'P433', 'value': 'issue'}, {'id': 'P356', 'value': 'DOI'}, {'id': 'P1433', 'value': 'published in'}, {'id': 'P2093', 'value': 'author name string'}, {'id': 'P577', 'value': 'publication date'}, {'id': 'P304', 'value': 'page(s)'}]}
res_4 = {'label': 'Myalgia cruris epidemica', 'id': 'Q74437509', 'description': 'scientific article published on 01 January 1957', 'properties': [{'id': 'P478', 'value': 'volume'}, {'id': 'P1476', 'value': 'title'}, {'id': 'P433', 'value': 'issue'}, {'id': 'P356', 'value': 'DOI'}, {'id': 'P1433', 'value': 'published in'}, {'id': 'P2860', 'value': 'cites work'}, {'id': 'P2093', 'value': 'author name string'}, {'id': 'P577', 'value': 'publication date'}, {'id': 'P304', 'value': 'page(s)'}, {'id': 'P921', 'value': 'main subject'}]}
res_5 = {'label': 'Myalgias or non-specific muscle pain in Arab or Indo-Pakistani patients may indicate vitamin D deficiency.', 'id': 'Q51651206', 'description': 'scientific article published on 10 March 2009', 'properties': [{'id': 'P478', 'value': 'volume'}, {'id': 'P1476', 'value': 'title'}, {'id': 'P433', 'value': 'issue'}, {'id': 'P356', 'value': 'DOI'}, {'id': 'P1433', 'value': 'published in'}, {'id': 'P2860', 'value': 'cites work'}, {'id': 'P2093', 'value': 'author name string'}, {'id': 'P577', 'value': 'publication date'}, {'id': 'P304', 'value': 'page(s)'}, {'id': 'P921', 'value': 'main subject'}]}
res_6 = {'label': 'Myalgia and biochemical changes following intermittent suxamethonium administration. Effects of alcuronium, lignocaine, midazolam and suxamethonium pretreatments on serum myoglobin, creatinine kinase and myalgia.', 'id': 'Q51790923', 'description': 'scientific article published in May 1987', 'properties': [{'id': 'P478', 'value': 'volume'}, {'id': 'P1476', 'value': 'title'}, {'id': 'P407', 'value': 'language of work or name'}, {'id': 'P433', 'value': 'issue'}, {'id': 'P356', 'value': 'DOI'}, {'id': 'P1433', 'value': 'published in'}, {'id': 'P2860', 'value': 'cites work'}, {'id': 'P2093', 'value': 'author name string'}, {'id': 'P577', 'value': 'publication date'}, {'id': 'P304', 'value': 'page(s)'}, {'id': 'P921', 'value': 'main subject'}]}
res_7 = {'label': 'Myalgias and arthralgias associated with paclitaxel.', 'id': 'Q35084059', 'description': 'scientific article', 'properties': [{'id': 'P478', 'value': 'volume'}, {'id': 'P1476', 'value': 'title'}, {'id': 'P433', 'value': 'issue'}, {'id': 'P1433', 'value': 'published in'}, {'id': 'P2860', 'value': 'cites work'}, {'id': 'P2093', 'value': 'author name string'}, {'id': 'P577', 'value': 'publication date'}, {'id': 'P304', 'value': 'page(s)'}]}
res_8 = {'label': "Myalgias and muscle contractures as the presenting signs of Addison's disease", 'id': 'Q36722355', 'description': 'scientific article published on March 1988', 'properties': [{'id': 'P478', 'value': 'volume'}, {'id': 'P1476', 'value': 'title'}, {'id': 'P407', 'value': 'language of work or name'}, {'id': 'P433', 'value': 'issue'}, {'id': 'P356', 'value': 'DOI'}, {'id': 'P1433', 'value': 'published in'}, {'id': 'P2860', 'value': 'cites work'}, {'id': 'P2093', 'value': 'author name string'}, {'id': 'P577', 'value': 'publication date'}, {'id': 'P304', 'value': 'page(s)'}]}
res_9 = {'label': 'Myalgia and biochemical changes following suxamethonium after induction of anaesthesia with thiopentone or propofol.', 'id': 'Q42288134', 'description': 'scientific article published on July 1993', 'properties': [{'id': 'P478', 'value': 'volume'}, {'id': 'P1476', 'value': 'title'}, {'id': 'P407', 'value': 'language of work or name'}, {'id': 'P433', 'value': 'issue'}, {'id': 'P356', 'value': 'DOI'}, {'id': 'P1433', 'value': 'published in'}, {'id': 'P2860', 'value': 'cites work'}, {'id': 'P2093', 'value': 'author name string'}, {'id': 'P577', 'value': 'publication date'}, {'id': 'P304', 'value': 'page(s)'}, {'id': 'P921', 'value': 'main subject'}]}
res_10 = {'label': 'Myalgia cruris epidemica (benign acute childhood myositis) associated with a Mycoplasma pneumonia infection', 'id': 'Q68981037', 'description': 'scientific article published on 01 May 1987', 'properties': [{'id': 'P478', 'value': 'volume'}, {'id': 'P1476', 'value': 'title'}, {'id': 'P433', 'value': 'issue'}, {'id': 'P356', 'value': 'DOI'}, {'id': 'P1433', 'value': 'published in'}, {'id': 'P2860', 'value': 'cites work'}, {'id': 'P2093', 'value': 'author name string'}, {'id': 'P577', 'value': 'publication date'}, {'id': 'P304', 'value': 'page(s)'}, {'id': 'P921', 'value': 'main subject'}]}

resources = [res_1, res_2, res_3, res_4, res_5, res_6, res_7, res_8, res_9, res_10]


def test_resources(criteria,top,by_name,by_properties,by_description):
	print("####   Top Resources by",criteria,"->")
	for t in graph.get_top_resources(context,label,resources,top,by_name,by_properties,by_description):
		print("\t Resource:",t)	


test_resources("by name",3,True,False,False)
test_resources("by properties",3,False,True,False)
test_resources("by description",3,False,False,True)
test_resources("by all",3,True,True,True)
