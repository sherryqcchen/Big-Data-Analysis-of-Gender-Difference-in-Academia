#Set server
# available severs: palain, lyrane, trenco, (klovia)
get_ipython().run_line_magic('env', 'HTTP_PROXY=http://lyrane:58471')
get_ipython().run_line_magic('env', 'HTTPS_PROXY=http://lyrane:58471')

#Modify scholarly package and save it as more_scholarly.py, import more scholarly here
import more_scholarly as scholarly
import pandas as pd

def get_hindex(name):
    search_query = scholarly.search_author(name)
    content = next(search_query).fill(hindexonly=True)
    h_index = content.hindex
    return h_index

df =  pd.read_csv('df_100_with_gender.csv')
df['co_author'] = ''

#get h index for all the 2000 researchers in dataframe
names = df['name']
#names = ['quanfa zhang', 'kerong zhang']
h={}
for name in names[0:2000]:
    print(name)
    if name not in h:
        h[name] = []
        h[name] = get_hindex(name)
    else:
        h[name] = h[name].extend(get_hindex(name))
h_1999 = h
#len(h_1999)

#set researcher's name as index to drop the duplicate researchers that could occur many times in different domain classifications
s_hindex = pd.Series(h_1999,name='h_index')
s_hindex.index.name = 'name'
df_hindex = s_hindex.reset_index()
df_hindex = df_hindex.set_index('name')
type(df_hindex)

#encode h-index back to dataframe by using name as index
# df = df.set_index('name')
# frames = [df, df_hindex]
df['h-index'] = ''
l_miss = []
for i in range(len(df)):
    try:
        df.loc[i,'h-index'] = h_1999[df.iloc[i]['name']]
#         print(i, h_1999[df.iloc[i]['name']])
    except:
        l_miss.append(df.iloc[i]['name'])
l_miss

#there are names failed to be passed into dataframe. redo the procedure above
h_miss={}
for name in l_miss:
    print(name)
    if name not in h_miss:
        h_miss[name] = []
        h_miss[name] = get_hindex(name)
    else:
        h_miss[name] = h_miss[name].extend(get_hindex(name))
#h_miss
h_all = {**h_1999,**h_miss}
len(h_all)

for i in range(len(df)):
    try:
        df.loc[i,'h-index'] = h_all[df.iloc[i]['name']]

    except:
       print(df.iloc[i]['name'])

#save dataframe in a .csv file
#df
df.to_csv('gender_difference_df.csv', encoding='utf-8')
