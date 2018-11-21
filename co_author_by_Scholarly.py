get_ipython().run_line_magic('env', 'HTTP_PROXY=http://trenco:58471')
get_ipython().run_line_magic('env', 'HTTPS_PROXY=http://trenco:58471')
# palain, lyrane, trenco, (klovia)

#import more_scholarly as scholarly
import scholarly
import pandas as pd

def get_researcher():
    df = pd.read_csv('df100.csv')
    return [name for name in df.name]
researchers = get_researcher()
print(researchers)

#Get all co-authors from extract  of a researcher
def get_coauthor(name):
    search_query1 = scholarly.search_author(name)
    author_info = next(search_query1).fill()
    #print(author_info)
    titles = [pub.bib['title'] for pub in author_info.publications]
    
    coauthors = []
    for index in range(2):
    #for index in range(len(author_info.publications)):
        search_query = scholarly.search_pubs_query(titles[index])
        pubs = next(search_query).fill()
        #print(pubs)
        author = pubs.bib['author'].split("and")
        #print(author)
        coauthors.extend(author)
    print(coauthors)
    coauthor_list = list(set(coauthors))
    return coauthor_list

#Build a dictionary to store the coauthors of each researcher

df100 = pd.read_csv('df100.csv', index_col='name')
coauthor = {}
for name in researchers:
    if name not in coauthor:
        coauthor[name] = {}
        coauthor[name] = get_coauthor(name)
df_author = pd.DataFrame(coauthor).set_index('name')
df = pd.concat([df0, df_author],axis=1)
df.to_csv('df100_with_coauthor.csv')

search_query1 = scholarly.search_author('Quanfa Zhang')
author_info = next(search_query1).fill()
#print(author_info)
titles = [pub.bib['title'] for pub in author_info.publications]
    
coauthors = []
for index in range(2):
#for index in range(len(author_info.publications)):
    search_query = scholarly.search_pubs_query(titles[index])
    pubs = next(search_query).fill()
    #print(pubs)
    author = pubs.bib['author'].split("and")
    #print(author)
    coauthors.extend(author)
print(coauthors)
coauthor_list = list(set(coauthors))

search_query1 = scholarly.search_author('Wenjun Huang')
author_info = next(search_query1).fill()
#print(author_info)
titles = [pub.bib['title'] for pub in author_info.publications]
    
coauthors = []
for index in range(3):
#for index in range(len(author_info.publications)):
    search_query = scholarly.search_pubs_query(titles[index])
    pubs = next(search_query).fill()
    #print(pubs)
    author = pubs.bib['author'].split("and")
    #print(author)
    coauthors.extend(author)
print(coauthors)
coauthor_list = list(set(coauthors))

