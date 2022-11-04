
dataset = "CovidQA"
#dataset = "NewsQA"
#dataset = "ConvQA"
with open('./datasets/'+dataset+'/test/test.target') as f_t:
	with open('./datasets/'+dataset+'/test/test.responses') as f_r:
		ref_responses = f_t.readlines()
		inf_responses = f_r.readlines()
		i = 0
		p_list= []
		r_list = []
		f1_list = []
		tp_list = []
		fp_list = []
		fn_list = []
		em_list = []
		while ( i < len(inf_responses)):
			ref_response = ref_responses[i].replace("\n","").lower().strip()
			inf_response = inf_responses[i].replace("\n","").lower().strip()
			print("reference: ", ref_response)
			print("inference: ", inf_response)
			em = 0
			if (inf_response == ref_response):
				em = 1
			em_list.append(em)

			ref_tokens = ref_response.lower().replace(",","").replace(".","").split(" ")
			inf_tokens = inf_response.lower().replace(",","").replace(".","").split(" ")

			tp = tn = fp = fn = 0
			for t in ref_tokens:
				if (t not in inf_tokens):
					fn += 1				
			for t in inf_tokens:
				if (t not in ref_tokens):
					fp += 1
				else:
					tp += 1
			print("tp:",tp,"fn:",fn,"fp:",fp)
			tp_list.append(tp)
			fp_list.append(fp)
			fn_list.append(fn)
			precision = tp / (tp + fp)
			recall = tp / (tp + fn)
			fmeasure = 0.0
			if ((precision+recall)>0):
				fmeasure = 2 * ((precision*recall)/(precision+recall))
			print("p:",precision,"r:",recall,"f1:",fmeasure)
			p_list.append(precision)
			r_list.append(recall)
			f1_list.append(fmeasure)
			i+=1		
		avg_p = sum(p_list)/len(p_list)
		avg_r = sum(r_list)/len(r_list)
		avg_f1 = sum(f1_list)/len(f1_list)		
		print("macro_p:",avg_p,"macro_r:",avg_r,"macro_f1:",avg_f1)

		micro_p = sum(tp_list)/ (sum(tp_list)+sum(fp_list))
		micro_r = sum(tp_list)/ (sum(tp_list)+sum(fn_list))
		micro_f = 2 * ((micro_p*micro_r)/(micro_p+micro_r))
		print("micro_p:",micro_p,"micro_r:",micro_r,"micro_f1:",micro_f)

		em_avg = sum(em_list) / len(em_list)
		print("em:",em_avg)
		print("questions:",i)

