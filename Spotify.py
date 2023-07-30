from dotenv import load_dotenv
import os
import base64
from requests import post
from requests import get
import json 
import spotipy  
from colorthief import ColorThief
import matplotlib.pyplot as plt
import urllib.request
import os
from spotipy.oauth2 import SpotifyOAuth  

  

load_dotenv()

client_id= os.getenv("CLIENT_ID")
client_secret= os.getenv("CLIENT_SECRET")

scope = "user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,client_secret,redirect_uri='http://example.com',scope=scope))

results = sp.current_user_playing_track()
name_of_song=(results['item']['name'])



def get_token():
    auth_string= client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64= str(base64.b64encode(auth_bytes), "utf-8")

    url="https://accounts.spotify.com/api/token"
    headers= {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result= post(url, headers=headers, data=data)
    json_result= json.loads(result.content)
    token= json_result["access_token"]
    return token
def get_auth_header(token):
    return{"Authorization": "Bearer " + token}


        
    


def search_for_artist(token, artist_name):
    url= "https://api.spotify.com/v1/search"
    headers=get_auth_header(token)
    query = f"?q={artist_name}&type=track,artist&limit=1"
    query_url= url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content) 
    return json_result







    

def dominant_color_from_url(url,tmp_file='tmp.jpg'):
    urllib.request.urlretrieve(url, tmp_file)
    color_thief = ColorThief(tmp_file)
    dominant_color = color_thief.get_color(quality=10)
    os.remove(tmp_file)
    return dominant_color





def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'. format(r, g, b)


token = get_token()
result= search_for_artist(token,name_of_song)


for idx, tracks in enumerate(result["tracks"]["items"]):
    url1=(f"{idx+1}.{tracks['album']['images'][0]['url']}")
colorurl=url1[2:]


print(name_of_song)




a=dominant_color_from_url(colorurl)
plt.imshow([[a]])
plt.show()

print(rgb_to_hex(a[0],a[1],a[2]))
from ifttt_webhook import IftttWebhook

# IFTTT Webhook key, available under "Documentation"
# at  https://ifttt.com/maker_webhooks/.
IFTTT_KEY = 'dizx31FyENIVyuu9P9zwVh'

# Create an instance of the IftttWebhook class,
# passing the IFTTT Webhook key as parameter.
ifttt = IftttWebhook(IFTTT_KEY)

# Trigger the IFTTT event defined by event_name with the content
# defined by the value1, value2 and value3 parameters.
ifttt.trigger('bulb', value1='cool')



