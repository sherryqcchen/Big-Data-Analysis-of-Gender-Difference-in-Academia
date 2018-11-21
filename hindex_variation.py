#modified maka package from https://github.com/gfhuertac/maka
import os
import sys
import json

from os.path import join, dirname
from random import randint
from queue import Queue
from threading import Thread
from time import sleep
from dotenv import load_dotenv
from optparse import IndentedHelpFormatter, OptionGroup, OptionParser

load_dotenv('.env')

try:
    import maka.classes as classes
    import maka.inquirer as inquirer
except ImportError:
    import inspect
    CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    PARENT_DIR = os.path.dirname(CURRENT_DIR)
    os.sys.path.insert(0, PARENT_DIR)
    import classes
    import inquirer

DELAY = 1
NUM_QUERIER_THREADS = 2
ROOT = {'author': None, 'aliases': [], 'articles': []}
THE_QUEUE = Queue()
QUITTHREAD = False

def find_article(article, parent=None):
    if parent is not None:
        for p in ROOT['articles']:
            if p['id'] == parent and p['cites']:
                 for art in p['cites']:
                     if art['id'] == article:
                         return art
    else:
        for art in ROOT['articles']:
            if art['id'] == article:
                return art
    return None

def querier_enclosure(i, q):
    """
    Wrapper for the query procedure in order to be used in a Worker
    """
    while not QUITTHREAD:
        print('Worker {}: Looking for the next query'.format(i))
        args = q.get()
        query = inquirer.AcademicQuerier(args['query_type'], args['payload'])
        if query is not None:
            results = query.post()
            if results:
                if args['query_type'] == inquirer.AcademicQueryType.INTERPRET:
                    expr = 'OR({})'.format(','.join([interpretation['rules'][0]['value']
                                                     for interpretation in results]))
                    THE_QUEUE.put({
                        'query_type': inquirer.AcademicQueryType.EVALUATE,
                        'payload':    {
                            'expr':       expr,
                            'attributes': '*'
                        },
                        'parent': None
                    })
                elif args['query_type'] == inquirer.AcademicQueryType.EVALUATE:
                    parent = args.get('parent', None)
                    branch = ROOT['articles'] if parent is None else (find_article(parent))['cites']
                    for result in results:
                        article = find_article(result['id'], parent)
                        if article is None:
                            branch.append(result)
                            if parent is None:
                                expr = 'RId={}'.format(result['id'])
                                THE_QUEUE.put({
                                    'query_type': inquirer.AcademicQueryType.EVALUATE,
                                    'payload':    {
                                        'expr':       expr,
                                        'attributes': '*'
                                    },
                                    'parent': result['id']
                                })
                    total = len(branch)
                    if total%50 == 0:
                        new_payload = args['payload'].copy()
                        new_payload['offset'] = total
                        THE_QUEUE.put({
                            'query_type': args['query_type'],
                            'payload': new_payload,
                            'parent': args['parent']
                        })
        q.task_done()
        sleep(DELAY)

def authors(author):
    global ROOT
    ROOT = {'author': None, 'aliases': [], 'articles': []}
    workers = []

    for i in range(NUM_QUERIER_THREADS):
        worker = Thread(target=querier_enclosure, args=(i, THE_QUEUE,))
        workers.append(worker)
        worker.setDaemon(True)
        worker.start()

    ROOT['author'] = author
    THE_QUEUE.put({
        'query_type': inquirer.AcademicQueryType.INTERPRET,
        'payload': {
           'query': 'papers by {}'.format(author)
        }
    })

    THE_QUEUE.join()
    print('Done')
    QUITTHREAD = True
    return ROOT
    #json.dump(ROOT, outfile, cls=classes.AcademicEncoder, indent=4)


import pandas as pd
import numpy as np
from maka.classes import AcademicPaper, AcademicAuthor
import pickle
import pprint
import matplotlib.pylab as plt

#dump ROOT here because running the codes above many times costs time and might reach the Microsoft Academiic API access limitation
pkl_file = open('xiaolicheng.pkl', 'rb')
ROOT= pickle.load(pkl_file)
pprint.pprint(ROOT)

#gain parent article's id and citations's id
#ROOT['articles'][3]['references'][0]['id']
dict_id={}
for article in ROOT['articles']:
    if article['id'] not in dict_id:
        dict_id[article['id']]=[]
    for cite in article['cites']:
        dict_id[article['id']].append(cite['id'])
dict_id

# gain the object of citing articles
list1 = []
for key, value in dict_id.items():
    list2 = []
    for id in value:
        art = find_article(id, parent=key)
        list2.append(art)
    list1.append(list2)
list1[0]

def count_year(y, list):
    count = 0
    for ob in list:
        year = ob['year']
        if year <=  y:
            count += 1
#             print(count)
    return count
# count_year(2002,list1[0])

def find_start_year(list):
    start = 2018
    for ob in list:
        year = ob['year']
        if year < start:
            start = year
    return start
# find_start_year(list1[0])

#produce a dictionary, the keys are years,values are citation list
dict_h = {}
for list in list1:
    start = find_start_year(list)
    years = np.arange(start,2019)
    for i in years:
        if i not in dict_h:
            dict_h[i] = []
            dict_h[i].append(count_year(i,list))
        else:
            dict_h[i].append(count_year(i,list))
#     print(i, [count_year(i,list)])
dict_h

#take citation list from dict_h to calculate h-index, :type citations: List[int]
#method from: https://github.com/kamyu104/LeetCode/blob/master/Python/h-index.py
def cal_hindex(citations):
    citations.sort(reverse=True)
    h=0
    for x in citations:
        if  x>= h + 1:
            h += 1
        else:
            break
    return h

dict_hindex={}
for key in dict_h.keys():
    cit = dict_h[key]
    if key not in dict_hindex:
        dict_hindex[key]=cal_hindex(cit)
dict_hindex

#plot h-index variation in years
#method from https://stackoverflow.com/questions/37266341/plotting-a-python-dict-in-order-of-key-values/37266356
h_list=sorted(dict_hindex.items())
x, y = zip(*h_list)
plt.plot(x, y, marker='.', markersize=12)

plt.title("H-index variation")
plt.xlabel("Year")
plt.ylabel("H-index")
plt.show()

h_list
