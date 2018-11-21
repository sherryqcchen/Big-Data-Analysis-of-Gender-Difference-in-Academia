import pandas as pd
import matplotlib as plt
import seaborn as sns

# using this code in Atom to modify csv file,removing those characters that fail to be encoded [^a-zA-z ,0-9"'-/=&;:?#]

df = pd.read_csv("scholar_dataframe_1.csv", encoding='utf-8')
df_clean = df
print(len(df))
for i, item in enumerate(list(df['gender'])):
#     print(i, item)
    if item == 'no face or blurred':
#         print(i, item)
        df_clean = df_clean.drop([i])
df_clean

g = df_clean.groupby(['domain', 'gender'])
g['citations'].agg(['min', 'max','mean', 'count'])
g['h-index'].agg(['min','max', 'mean', 'count'])

def plot_gender_count(df):
    return sns.countplot(y='domain',
                        hue='gender',
                        data=df)
#method from: http://www.alexsalo.xyz/pretty-boxplots-python-matplotlib-pandas-seaborn/

def plot_gender_hindex(df):
    return sns.factorplot(kind='box',        # Boxplot
                   y='h-index',       # Y-axis - values for boxplot
                   x='domain',        # X-axis - first factor
                   hue='gender',         # Second factor denoted by color
                   data=df,        # Dataframe 
                   size=8,            # Figure size (x100px)      
                   aspect=1.5,        # Width = size * aspect 
                   legend_out=False)  # Mak
def plot_gender_citation(df):
    return sns.factorplot(kind='box',
                       y='citations',
                       x='domain',
                       hue='gender',
                       data=df,
                       aspect=1.5,  
                       size=8,
                       legend_out=False)  # Mak

plot_gender_hindex(df_clean)
plot_gender_count(df_clean)
plot_gender_citation(df_clean)