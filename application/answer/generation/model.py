import logging

class ModelEN:

    def __init__(self):
        self.logger = logging.getLogger('muheqa')
        self.logger.debug("initializing Answer Model ...")        

    def contains_number(self,text):
        return any(char.isdigit() for char in text)    

    def get_response(self, category, evidence):
        response = {}
        if (category['category'] == 'resource'):
            response['type'] = 'literal'
            response['answer'] = evidence['value']
        elif (category['category'] == 'boolean'):
            response['type'] = 'boolean'
            response['answer'] = (evidence['score'] > 0.5)
        elif (len(category['type']) > 0) and (category['type'][0] == 'number'):
            response['type'] = 'number'
            if (self.contains_number(evidence['value'])):
                response['answer'] = evidence['value']
            elif (',' in evidence['value']):
                response['answer'] = len(evidence['value'].split(","))
            else:
                response['answer'] = 1
        else:
           response['answer'] = evidence['value'] 
        response['confidence'] = evidence['score']
        response['evidence'] = evidence['summary']
        response['start'] = evidence['start']
        response['end'] = evidence['end']
        return response