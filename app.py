from model import *
from flask import request
import json

@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return json.dumps({'feedback': 'End of the world!!! ~~ sono chi no kioku ~~'})


@app.route('/index', methods=['GET'])
def index():
    return hello_world()

@app.route('/anime', methods=['GET'])
def anime():
    anime_list = []
    for anime in db.session.query(Anime).all():
        anime_list.append(anime.get_dict())
    return json.dumps(anime_list)

@app.route('/genre', methods=['GET'])
def genre():
    genre_list = []
    for genre in db.session.query(Genre).all():
        genre_list.append(genre.get_dict())
    return json.dumps(genre_list)

@app.route('/anime/search', methods=['GET'])
def anime_search():
    title = request.args.get('title')
    anime_list = []
    for anime in db.session.query(Anime).all():
        if title.lower() in anime.title.lower():
            anime_list.append(anime.get_dict())
    return json.dumps(anime_list)


if __name__ == '__main__':
    app.run()
