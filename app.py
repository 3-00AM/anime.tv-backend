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
    for g in db.session.query(Genre).all():
        genre_list.append(g.get_dict())
    return json.dumps(genre_list)


@app.route('/anime/search', methods=['GET'])
def anime_search():
    title = request.args.get('keyword')
    anime_list = []
    for a in db.session.query(Anime).all():
        if title.lower() in a.title.lower():
            anime_list.append(a.get_dict())
    return json.dumps(anime_list)


@app.route('/genre/search', methods=['GET'])
def genre_search():
    name = request.args.get('keyword')
    genre_list = []
    for g in db.session.query(Genre).all():
        if name.lower() in g.name.lower():
            genre_list.append(g.get_dict())
    return json.dumps(genre_list)


if __name__ == '__main__':
    app.run()
