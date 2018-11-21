import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

#run the command-line to get a researcher's publication json file
# reading the JSON data using json.load() https://stackoverflow.com/questions/21104592/json-to-pandas-dataframe
file = 'xiaolicheng.json'
with open(file) as train_file:
    dict_train = json.load(train_file)

# converting json dataset from dictionary to dataframe
df = pd.DataFrame.from_dict(dict_train, orient='index')
df.reset_index(level=0, inplace=True)
df_pub = pd.DataFrame(df.iloc[2,1])
#df_pub

#Prooduce co-author list of a researcher
list_coauthors = []
for pub in df_pub.authors:
    #print((pub[0])['name'])
    for author in pub:
        coauthor = author['name']
        list_coauthors.append(coauthor)

coauthors = list(set(list_coauthors))
#coauthors

def single_pub_plot():
    pubs_count = df_pub['year'].value_counts() #type: series
    pubs_count.sort_index().plot(kind="bar",color="#66B2FF")
    plt.xlabel('Year')
    plt.ylabel('Publications')

single_pub_plot()

def single_cit_plot():
    years = df_pub["year"]
    cits = df_pub["num_citations"]

    df_citations = pd.concat([years,cits],axis=1)
    df_citations
    citations_count = df_citations.groupby(by=['year'])['num_citations'].sum()
    citations_count.plot(kind="bar",color="#FF9999")
    plt.xlabel('Year')
    plt.ylabel('Citations')
    #return plt
single_cit_plot()
