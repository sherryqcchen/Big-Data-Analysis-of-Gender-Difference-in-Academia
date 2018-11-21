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
# xxx = find_article('SAS')
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
import json
import numpy as np
from maka.classes import AcademicPaper, AcademicAuthor

def get_coauthor_maka(name_):
#     ROOT = {'author': None, 'aliases': [], 'articles': []}
#     print(name_)
    dict_train = authors(name_)
#     print(dict_train)
    article_list = dict_train['articles']
    coauthors = []
    for article in article_list:
        coauthor_list = article['authors']
        for coauthor in coauthor_list:
            if coauthor['name'] not in coauthors:
                #print(coauthor['name'])
                coauthors.append(coauthor['name'])
    return coauthors

#get_coauthor_maka('qiuyang chen')
#get_coauthor_maka('xxxxxxxxxxxxx')

df =  pd.read_csv('/cs/home/qc22/qc22code/df_100_with_gender.csv')
names = df['name']
names
# df = df.set_index('name')
# for i in range(len(df)):
#     print(df.iloc[i]['name'])
 
# df =  pd.read_csv('/cs/home/qc22/qc22code/df_100_with_gender.csv')
names = df['name']
#print(names)
a = {}
#Run really slowly!!! only use 10 researchers as an example
for name in names[1907:1922]:
    print(name)
#     ROOT = {'author': None, 'aliases': [], 'articles': []}
    if name not in a:
        a[name] = []
        a[name] = get_coauthor_maka(name)
    else:
        a[name] = a[name].extend(get_coauthor_maka(name))


s_coauthor = pd.Series(a, name='co_author')
s_coauthor.index.name = 'name'
df_coauthor=s_coauthor.reset_index()
df_coauthor=df_coauthor.set_index('name')
df_coauthor

df = df.set_index('name')
frames = [df, df_coauthor]
df_new = pd.concat(frames,axis=1)
df_new.to_csv("df_100_with_coauthor.csv")

