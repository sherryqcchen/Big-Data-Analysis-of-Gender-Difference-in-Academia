#use different servers in computer science school to unblock Google Scholar's limitation
# servers' name: palain, lyrane, trenco, (klovia)
get_ipython().run_line_magic('env', 'HTTP_PROXY=http://lyrane:58471')
get_ipython().run_line_magic('env', 'HTTPS_PROXY=http://lyrane:58471')

#import scholarly
import more_scholarly as scholarly
import pandas as pd
from IPython.display import display

#delete all the researchers without portrait
def check_avatar(search_query, results):
    try:
        x = next(search_query)
    except:
        return
    if '/citations/images/avatar_scholar_56.png' in x.url_picture:
        check_avatar(search_query, results)
    else:
        results.append(vars(x))

#construct data frame from the result
def get_data(label):
    search_query = scholarly.search_keyword(label)
    results = []
    for i in range(100):
        check_avatar(search_query, results)
    df_origin = pd.DataFrame(results).drop(columns=['_filled', 'email']) #delete two rows
    col = df_origin.columns.tolist()
    col = col[-2:] + col[:-2]
    df = df_origin[col].rename(index=str, columns={'url_picture':'portrait_url','citedby':'citations','interests':'label'})
    #display(df)
    return df

#get the data for each diciplines in social science
def get_df_ss():
    law_data = get_data('law')
    anthropology_data = get_data('anthropology')
    economics_data = get_data('economics')
    human_geography_data = get_data('human')
    political_science_data = get_data('political')
    psychology_data = get_data('psychology')
    sociology_data = get_data('sociology')

    df_sc = pd.concat([anthropology_data, economics_data,human_geography_data, political_science_data, psychology_data, sociology_data, law_data],keys=['anthropology','economics','human', 'political', 'psychology', 'sociology','law'])
    df_sc1 = df_sc.drop_duplicates(subset="id", keep="first")
    df_social_science = df_sc1.sort_values(['citations'],ascending=0).reset_index(drop=True)
    return df_social_science

#get the data for each diciplines in humanities
def get_df_h():
    arts_data = get_data('arts')
    history_data = get_data('history')
    literature_data = get_data('literature')
    philosophy_data = get_data('philosophy')
    theology_data = get_data('theology')

    df_h = pd.concat([arts_data, history_data,literature_data, philosophy_data, theology_data],keys=['arts','history','literature', 'philosophy', 'theology'])
    df_h1 = df_h.drop_duplicates(subset="id", keep="first")
    df_humanity = df_h1.sort_values(['citations'],ascending=0).reset_index(drop=True)
    return df_humanity

#get the data for each diciplines in natural science
def get_df_ns():
    biology_data = get_data('biology')
    chemistry_data = get_data('chemistry')
    earth_science_data = get_data('earth')
    space_science_data = get_data('space')
    physics_data = get_data('physics')

    df_ns = pd.concat([biology_data, chemistry_data,earth_science_data, space_science_data, physics_data],keys=['biology','chemistry','earth', 'space', 'physics'])
    df_ns1 = df_ns.drop_duplicates(subset="id", keep="first")
    df_natural_science = df_ns1.sort_values(['citations'],ascending=0).reset_index(drop=True)
    return df_natural_science

#get the data for each diciplines in formal science
def get_df_fs():
    computer_science_data = get_data('computer')
    mathematics_data = get_data('mathematics')
    statistics_data = get_data('statistics')

    df_fs = pd.concat([computer_science_data, mathematics_data,statistics_data],keys=['computer','mathematics','statistics'])
    df_fs1 = df_fs.drop_duplicates(subset="id", keep="first")
    df_formal_science = df_fs1.sort_values(['citations'],ascending=0).reset_index(drop=True)
    return df_formal_science

#get the data for each diciplines in applied science
def get_df_as():
    engineering_data = get_data('engineering')
    medicine_data = get_data('medicine')
    health_data = get_data('health')

    df_as = pd.concat([engineering_data, medicine_data,health_data],keys=['engineering','medicine','health'])
    df_as1 = df_as.drop_duplicates(subset="id", keep="first")
    df_applied_science = df_as1.sort_values(['citations'],ascending=0).reset_index(drop=True)
    return df_applied_science
def get_df():
    df1 = get_df_ss()
    df2 = get_df_h()
    df3 = get_df_ns()
    df4 = get_df_fs()
    df5 = get_df_as()
    df = pd.concat([df1,df2,df3,df4,df5], keys=["social science", "humanity", "natural science", "fomal science", "applied science"])
    return df

get_df().to_csv("df100.csv")

# method from https://blog.csdn.net/wwaiym/article/details/5829471
#import urllib
df = get_df()
#law_data.shape
def portrait_download(d):
    urls = d["portrait_url"]
    names = d["id"]
    img_folder = "portraits/"
    gs_url = "https://scholar.google.co.uk/"
    response = urllib.request.urlopen(gs_url)
    html = response.read()
    #print(html)

    for i in range(d.shape[0]):
        url = gs_url + urls[i]
        name = names[i] + ".jpeg"
        urllib.request.urlretrieve(url,img_folder + name)
    print("successfully downloaded")

portrait_download(df)
