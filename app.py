from model import *
import requests
import json
from decouple import config

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/index')
def index():  # put application's code here
    return json.dumps({'feedback': 'index page'})


def get_all_anime():
    url = "https://api.myanimelist.net/v2/anime/ranking?ranking_type=all&limit=500&fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + config('MAL_ACCESS_TOKEN')
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    # try:
    #     data = Anime(title, rank)

    return response['data']


def get_genres(list):
    result = f""
    for genre in list:
        result += genre['name'] + " "
    return result


if __name__ == '__main__':

    for node in get_all_anime():
        node = node['node']
        anime = Anime(node['title'],
                      int(node['rank']),
                      int(node['popularity']),
                      get_genres(node['genres']),
                      node['media_type'],
                      node['status'],
                      node['rating'],
                      node['studios'])
        print("finished create class")
        try:
            db.session.add(anime)
            db.session.commit()
        except:
            db.session.rollback()

    print(get_all_anime())
    # app.run()
