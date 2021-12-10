from model import *
from flask import request, jsonify
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
@swag_from("swagger/anime_get.yml")
def anime():
    anime_list = []
    for anime in db.session.query(Anime).all():
        anime_list.append(anime.get_dict())
    return jsonify(anime_list)


@app.route('/anime/search', methods=['GET'])
@swag_from("swagger/anime_search_get.yml")
def anime_search():
    keyword = request.args.get('keyword')
    anime_list = []
    for anime in db.session.query(Anime).all():
        anime_dict = anime.get_dict()
        if keyword.lower() in anime_dict['title'].lower():
            anime_list.append(anime_dict)
            continue
        key_check_list = {
            'genres': 'name',
            'studios': 'name',
            'related_anime': 'title',
            'related_manga': 'title',
            'recommendations': 'title',
            'related_theme': 'title',
        }
        for key, checkee in key_check_list.items():
            for keyee in anime_dict[key]:
                if keyword in keyee[checkee].lower():
                    anime_list.append(anime_dict)
                    continue

    return jsonify(anime_list)


@app.route('/genre', methods=['GET'])
@swag_from("swagger/genre_get.yml")
def genre():
    genre_list = []
    for g in db.session.query(Genre).all():
        genre_list.append(g.get_dict())
    return jsonify(genre_list)


@app.route('/genre/search', methods=['GET'])
@swag_from("swagger/genre_search_get.yml")
def genre_search():
    keyword = request.args.get('keyword')
    genre_list = []
    for g in db.session.query(Genre).all():
        if keyword.lower() in g.name.lower():
            genre_list.append(g.get_dict())
    return jsonify(genre_list)


@app.route('/studio', methods=['GET'])
@swag_from("swagger/studio_get.yml")
def studio():
    studio_list = []
    for studio in db.session.query(Studio).all():
        studio_list.append(studio.get_dict())
    return jsonify(studio_list)


@app.route('/studio/search', methods=['GET'])
@swag_from("swagger/studio_search_get.yml")
def studio_search():
    keyword = request.args.get('keyword')
    studio_list = []
    for studio in db.session.query(Studio).all():
        if keyword.lower() in studio.name.lower():
            studio_list.append(studio.get_dict())
    return jsonify(studio_list)


@app.route('/manga', methods=['GET'])
@swag_from("swagger/manga_get.yml")
def manga():
    manga_list = []
    for manga in db.session.query(Manga).all():
        manga_list.append(manga.get_dict())
    return jsonify(manga_list)


@app.route('/manga/search', methods=['GET'])
@swag_from("swagger/manga_search_get.yml")
def manga_search():
    keyword = request.args.get('keyword')
    manga_list = []
    for manga in db.session.query(Manga).all():
        if keyword.lower() in manga.title.lower():
            manga_list.append(manga.get_dict())
    return jsonify(manga_list)


@app.route('/theme', methods=['GET'])
@swag_from("swagger/theme_get.yml")
def theme():
    theme_list = []
    for theme in db.session.query(Theme).all():
        theme_list.append(theme.get_dict())
    return jsonify(theme_list)


@app.route('/theme/search', methods=['GET'])
@swag_from("swagger/theme_search_get.yml")
def theme_search():
    keyword = request.args.get('keyword')
    theme_list = []
    for theme in db.session.query(Theme).all():
        if keyword.lower() in theme.title.lower():
            theme_list.append(theme.get_dict())
    return jsonify(theme_list)


@app.route('/review', methods=['GET'])
@swag_from("swagger/review_get.yml")
def review():
    review_list = []
    for review in db.session.query(Review).all():
        review_list.append(review.get_dict())
    return jsonify(review_list)


@app.route('/review/search', methods=['GET'])
@swag_from("swagger/review_search_get.yml")
def review_search():
    keyword = request.args.get('keyword')
    review_list = []
    for review in db.session.query(Review).all():
        if keyword.lower() in review.title.lower() or keyword.lower() in str(review.score):
            review_list.append(review.get_dict())
    return jsonify(review_list)


if __name__ == '__main__':
    app.run()
