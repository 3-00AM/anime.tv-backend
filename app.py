from model import *
import requests
import json
from decouple import config

app = Flask(__name__)  # keep it?


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/index')
def index():  # put application's code here
    return json.dumps({'feedback': 'index page'})


def get_all_anime(query):
    url = f"https://api.myanimelist.net/v2/anime?q={query}&fields=id,title,main_picture,alternative_titles," \
          f"start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at," \
          f"updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source," \
          f"average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios," \
          f"statistics "

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + config('MAL_ACCESS_TOKEN')
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    # try:
    #     data = Anime(title, rank)

    return json.dumps(response['data'][0]['node']['title'])


if __name__ == '__main__':
    print(get_all_anime(""))
    # app.run()
