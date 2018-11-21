#set the sever
get_ipython().run_line_magic('env', 'HTTP_PROXY=http://lyrane:58471')
get_ipython().run_line_magic('env', 'HTTPS_PROXY=http://lyrane:58471')
# palain, lyrane, trenco, (klovia)

import pandas as pd
import requests
import time
# If you are using a Jupyter notebook, uncomment the following line.
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO

df = pd.read_csv('df100_medium.csv')
df['gender'] = ''
main_url = "https://scholar.google.co.uk"
# df
my_dict = {}
for i in range(len(df)):
    df.loc[i,'portrait_url'] = main_url + df.loc[i,'portrait_url']
    my_dict[df.loc[i,'portrait_url']] = i

urls = df.portrait_url
urls


#method from  https://docs.microsoft.com/en-us/azure/cognitive-services/Face/Overview
# Replace <Subscription Key> with your valid subscription key.
subscription_key = "ca6b2f7ddcfe42c887a4b4e01641b6f9"
assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the westcentralus region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.
face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

# Set image_url to the URL of an image that you want to analyze.
def gender_compute(link):
    image_url = link 
    #image_url = "https://scontent-lht6-1.xx.fbcdn.net/v/t1.0-9/32602568_1624594444304712_2263634978321465344_o.jpg?_nc_cat=0&oh=c1c5ed6997710ac519f0c6090c52cda3&oe=5C06E8FF"
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
        'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }
    data = {'url': image_url}
    response = requests.post(face_api_url, params=params, headers=headers, json=data)
    faces = response.json()

    # Display the original image and overlay it with the face information.
    image = Image.open(BytesIO(requests.get(image_url).content))
    plt.figure(figsize=(8, 8))
    ax = plt.imshow(image, alpha=0.6)
    for face in faces:
        fr = face["faceRectangle"]
        fa = face["faceAttributes"]
        origin = (fr["left"], fr["top"])
        p = patches.Rectangle(
            origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
        ax.axes.add_patch(p)
        plt.text(origin[0], origin[1], "%s, %d"%(fa["gender"].capitalize(), fa["age"]),
                 fontsize=20, weight="bold", va="bottom")
    _ = plt.axis("off")
    print(faces)
    if len(faces) > 0:
        #return {'url':((faces[0])['faceAttributes'])['gender']}
        return ((faces[0])['faceAttributes'])['gender']
    else:
        return 'no face or blurred'
#gender_compute('https://scholar.google.co.uk/citations?view_op=view_photo&user=qc6CJjYAAAAJ&citpid=2')


#set a running time limitation, because faces API runs only 20 time per minute for free
for i, url in enumerate(urls):
    if (i + 1) % 20 != 0:
        index = my_dict[url]
        df['gender'][index] = gender_compute(url)
        print(index)
    else:
        time.sleep(60)

df_new = df
df_new.to_csv("df_100_with_gender.csv")
df.pop("Unnamed: 1")
df.pop("Unnamed: 0")
df.rename(columns={"Unnamed: 0.1":"domain"}, inplace=True)