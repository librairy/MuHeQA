import coloredlogs, logging
import application.logformatter as lf
import application.summary.keyword as kw
import application.summary.entity as ent

if __name__ == '__main__':
	
	log_level = logging.DEBUG
	
	fh = logging.StreamHandler()
	#fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
	#fh.setFormatter(fh_formatter)
	fh.setFormatter(lf.CustomFormatter())
	fh.setLevel(log_level)

	logger = logging.getLogger('muheqa')
	logger.addHandler(fh)
	logger.setLevel(log_level)
	

	logger.info("Executing evaluation on Keyword Discovery ....")

	keyword_discovery = kw.Keyword()
	entity_discovery = ent.Entity()


	query = "what male actor was born in  warsaw"
	logger.info("Query: '" + query + "'")
	logger.info("Entities:"+ str(entity_discovery.get(query)))
	logger.info("Keywords:"+ str(keyword_discovery.get(query)))
