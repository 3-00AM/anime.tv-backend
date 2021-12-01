from model import *
from flask import request
from flasgger.utils import swag_from
from flasgger import Swagger
import json

app.config["SWAGGER"] = {"title": "ANIME-TV-API", "universion": 1}

swagger_config = {
    "headers": [],
    "specs": [{
        "title": "anime-tv-api",
        "description":
        "This is api documentation for anime.tv module",
        "version": "1.5.2",
        "externalDocs": {
            "description": "See our github",
            "url": "https://github.com/3-00AM/anime.tv-backend",
        },
        "servers": {
            "url": "https://anime-tv-api.herokuapp.com/"
        },
        "endpoint": "api-doc",
        "route": "/api",
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True,
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api-doc/",
}
swagger = Swagger(app, config=swagger_config)

@app.route('/', methods=['GET'])
def hello_world():
    return json.dumps({'feedback': 'End of the world!!! ~~ sono chi no kioku ~~'})

@app.route('/index', methods=['GET'])
def index():
    return hello_world()

@app.route('/anime', methods=['GET'])
@swag_from("swagger/animeget.yml")
def anime():
    anime_list = []
    for anime in db.session.query(Anime).all():
        anime_list.append(anime.get_dict())
    return json.dumps(anime_list)

@app.route('/genre', methods=['GET'])
@swag_from("swagger/genreget.yml")
def genre():
    genre_list = []
    for genre in db.session.query(Genre).all():
        genre_list.append(genre.get_dict())
    return json.dumps(genre_list)

@app.route('/anime/search', methods=['GET'])
def anime_search():
    title = request.args.get('keyword')
    anime_list = []
    for anime in db.session.query(Anime).all():
        if title.lower() in anime.title.lower():
            anime_list.append(anime.get_dict())
    return json.dumps(anime_list)

@app.route('/genre/search', methods=['GET'])
def genre_search():
    name = request.args.get('keyword')
    genre_list = []
    for genre in db.session.query(Genre).all():
        if name.lower() in genre.name.lower():
            genre_list.append(genre.get_dict())
    return json.dumps(genre_list)


if __name__ == '__main__':
    app.run()
