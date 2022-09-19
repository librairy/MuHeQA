"""
based on http://ceur-ws.org/Vol-2774/paper-03.pdf

https://github.com/cnikas/isl-smart-task

"""
import logging
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np
import sys
import csv
import json
import tensorflow as tf
import time


class QuestionClassifier:
    
    def __init__(self,resources_dir):
        self.logger = logging.getLogger('muheqa')
        self.logger.debug("initializing Question Classifier ...")
        category_model_dir = resources_dir+'/BERT Fine-Tuning category'
        literal_model_dir = resources_dir+'/BERT Fine-Tuning literal'
        resource_model_dir = resources_dir+'/BERT Fine-Tuning resource'
        mapping_csv = resources_dir+'/mapping.csv'
        hierarchy_json = resources_dir+'/dbpedia_hierarchy.json'
        
        self.id_to_label = {}
        self.label_to_id = {}
        with open(mapping_csv) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                self.id_to_label[row[1]] = row[0]
                self.label_to_id[row[0]] = row[1]
        
        self.logger.debug("loading category model ...")
        self.category_tokenizer = BertTokenizer.from_pretrained(category_model_dir)
        self.category_model = BertForSequenceClassification.from_pretrained(category_model_dir,num_labels=3)
        
        self.logger.debug("loading literal model ...")
        self.literal_tokenizer = BertTokenizer.from_pretrained(literal_model_dir)
        self.literal_model = BertForSequenceClassification.from_pretrained(literal_model_dir,num_labels=3)
        
        self.logger.debug("loading resource model ...")
        self.resource_tokenizer = BertTokenizer.from_pretrained(resource_model_dir)
        self.resource_model = BertForSequenceClassification.from_pretrained(resource_model_dir,num_labels=len(self.id_to_label))
        
        
        self.hierarchy = {}
        with open(hierarchy_json) as json_file:
            self.hierarchy = json.load(json_file)
            
    def get_category(self,question):
        foundCategory = self.classify_category(question)
        if foundCategory == 'boolean':
            foundType = ['boolean']
        elif foundCategory == 'literal':
            foundType = [self.classify_literal(question)]
        else:
            foundType = self.classify_resource(question)[0:10]

        result_dict = {
            'question': question,
            'category': foundCategory,
            'type': foundType
        }       
        return result_dict
            
    def classify_category(self,q):
        input_ids = torch.tensor(self.category_tokenizer.encode(q, add_special_tokens=True)).unsqueeze(0)  # Batch size 1
        labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
        
        with torch.no_grad():
            outputs = self.category_model(input_ids, labels=labels)
        logits = outputs[1]
        result = np.argmax(logits.detach().numpy(),axis=1)[0]
        if result == 0:
            categoryLabel = 'boolean'
        elif result == 1:
            categoryLabel = 'literal'
        else:
            categoryLabel = 'resource'
        return categoryLabel
    
    def classify_literal(self,q):
        input_ids = torch.tensor(self.literal_tokenizer.encode(q, add_special_tokens=True)).unsqueeze(0)  # Batch size 1
        labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
        
        with torch.no_grad():
            outputs = self.literal_model(input_ids, labels=labels)
        logits = outputs[1]
        result = np.argmax(logits.detach().numpy(),axis=1)[0]
        if result == 0:
            categoryLabel = 'date'
        elif result == 1:
            categoryLabel = 'number'
        else:
            categoryLabel = 'string'
        return categoryLabel
    
    def classify_resource(self,q):
        input_ids = torch.tensor(self.resource_tokenizer.encode(q, add_special_tokens=True)).unsqueeze(0)  # Batch size 1
        labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
        
        with torch.no_grad():
            outputs = self.resource_model(input_ids, labels=labels)
        
        logits = outputs[1]
        l_array = logits.detach().numpy()[0]
        #normalize logits so that max is 1
        norm = [float(i)/max(l_array) for i in l_array]
        result_before = np.argsort(norm)[::-1]
        #print(q)
        #print('before')
        #for r in result_before:
            #print(id_to_label[str(r)])
        #reward top class
        initial_top_index = np.argmax(norm)
        initial_top = self.hierarchy[self.id_to_label[str(initial_top_index)]]
        if initial_top != {}:
            norm[initial_top_index] = norm[initial_top_index] + int(initial_top['level'])/6
            #reward sub classes of top class
            initial_top_children = initial_top['children']
            for c in initial_top_children:
                if c in self.label_to_id:
                    norm[int(self.label_to_id[c])] = norm[int(self.label_to_id[c])] + int(self.hierarchy[c]['level'])/6
        #classes in descending order
        result = np.argsort(norm)[::-1]
        #print('after')
        #for r in result:
            #print(id_to_label[str(r)])
        result_mapped = []
        for r in result:
            result_mapped.append(self.id_to_label[str(r)])
        return result_mapped