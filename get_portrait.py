get_ipython().run_line_magic('env', 'HTTP_PROXY=http://palain:58471')
get_ipython().run_line_magic('env', 'HTTPS_PROXY=http://palain:58471')
# palain, lyrane, trenco, (klovia)

import pandas as pd
import urllib
from data_frame import get_df

df =  pd.read_csv('df100.csv')
df["portrait_url"] = df.portrait_url.str.replace('small','medium')
#df.portrait_url
df.to_csv("df100_medium.csv")

# method from https://blog.csdn.net/wwaiym/article/details/5829471
#import urllib

#law_data.shape
def portrait_download(d):
    urls = d["portrait_url"]
    names = d["id"]
    img_folder = "portraits/"
    gs_url = "https://scholar.google.co.uk/"
    response = urllib.request.urlopen(gs_url)
    html = response.read()
    print(html)
    
    for i in range(d.shape[0]): 
        url = gs_url + urls[i]
        name = names[i] + ".jpeg" 
        urllib.request.urlretrieve(url,img_folder + name)
    print("successfully downloaded")

portrait_download(df)


