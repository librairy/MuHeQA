#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thuesday June 1 12:45:05 2021

@author: cbadenes
"""
import pysolr
import html
import time
import sys
import os
import csv
from datetime import datetime

if __name__ == '__main__':

    # Create a client instance. The timeout and authentication options are not required.
    server          = 'http://localhost:8983/solr'
    solr_index      = pysolr.Solr(server+'/documents', always_commit=True, timeout=120)
    t               = time.time()

    print("[",datetime.now(),"] loading files ")

    with open('conv_dump_spllited.csv') as csv_file:
        csv_reader  = csv.reader(csv_file, delimiter='\t')
        line_count  = 0
        window      = 100
        docs        = []
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #print(f'\t{row[0]} - {row[1]}')
                doc = { 'name_s':row[0], 'text_t':row[0] + row[1]}
                docs.append(doc)
                line_count += 1
            if (line_count % window == 0):
                print("[",datetime.now(),"] indexing docs: ", line_count)
                solr_index.add(docs)
                docs = []
        print(f'Processed {line_count} lines.')

    # Load articles
    print("[",datetime.now(),"] indexing docs: ", line_count)
    solr_index.add(docs)
    print('Time to parse articles: {} mins'.format(round((time.time() - t) / 60, 2)))
    print("Total Documents:",line_count)