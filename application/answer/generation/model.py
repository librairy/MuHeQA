import logging

class ModelEN:

    def __init__(self):
        self.logger = logging.getLogger('muheqa')
        self.logger.debug("initializing Answer Model ...")        


    def get_response(self, category, evidence):
        response = {}
        response['confidence'] = evidence['score']
        response['evidence'] = evidence['summary']   
        if (category['category'] == 'resource'):
            response['type'] = 'literal'
            response['answer'] = evidence['value']
        elif (category['category'] == 'boolean'):
            response['type'] = 'boolean'
            response['answer'] = (evidence['score'] > 0.5)
        elif (len(category['type']) > 0) and (category['type'][0] == 'number'):
            response['type'] = 'number'
            if (',' in evidence['value']):
                response['answer'] = len(evidence['value'].split(","))
            else:
                response['answer'] = 1
        return response