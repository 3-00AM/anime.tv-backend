import sys

import requests

from model import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.mysql import insert

payload = {}
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + config('MAL_ACCESS_TOKEN')
}


# def get_all_genres():
#     url = "https://api.myanimelist.net/v2/anime/ranking?ranking_type=all&limit=10&fields=genres"

#     response = requests.request(
#         "GET", url, headers=headers, data=payload).json()

#     return response['data']


def get_all_anime():
    url = "https://api.myanimelist.net/v2/anime/ranking?ranking_type=all&limit=10"

    response = requests.request(
        "GET", url, headers=headers, data=payload).json()

    # try:
    #     data = Anime(title, rank)

    return response['data']


def get_anime_by_id(anime_id):
    url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=id,title,rank,popularity,media_type,status,rating,studios,genres,related_anime,related_manga,recommendations"

    response = requests.request(
        "GET", url, headers=headers, data=payload).json()

    return response


def insert_sub_table(db, anime_details, Table, key, arg1, arg2):
    for g in anime_details[key]:
        try:
            print(f"Add {key}: {g[arg2]} to db")
            data = Table(g[arg1], g[arg2])
            db.session.add(data)
            db.session.commit()
        except IntegrityError:
            print(f"Failed to add {key}: {g[arg2]} to db")
            db.session.rollback()


def insert_sub_table_with_node(db, anime_details, Table, key, arg1, arg2):
    for n in anime_details[key]:
        try:
            print(f"Add {key}: {n['node'][arg2]} to db")
            data = Table(n['node'][arg1], n['node'][arg2])
            db.session.add(data)
            db.session.commit()
        except IntegrityError:
            print(f"Failed to add {key}: {n['node'][arg2]} to db")
            db.session.rollback()


def link_association(db, Table, key):
    for x in db.session.query(Table).all():
        for anime in db.session.query(Anime).all():
            anime_details = get_anime_by_id(anime.mal_id)
            for g in anime_details[key]:
                if x.mal_id == g['id']:
                    try:
                        print(
                            f"Link {key}: {x.mal_id} and Anime: {anime.title}")
                        x.animes.append(anime)
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        db.session.rollback()
                        print(
                            f"Failed to link {key}: {x.mal_id} and Anime: {anime.title}")


def link_association_with_node(db, Table, key):
    for x in db.session.query(Table).all():
        for anime in db.session.query(Anime).all():
            anime_details = get_anime_by_id(anime.mal_id)
            for g in anime_details[key]:
                if x.mal_id == g['node']['id']:
                    try:
                        print(
                            f"Link {key}: {x.mal_id} and Anime: {anime.title}")
                        x.animes.append(anime)
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        db.session.rollback()
                        print(
                            f"Failed to link {key}: {x.mal_id} and Anime: {anime.title}")


""" Use Case
anime7 = Anime(id=7, 'Arifureta', ... ,... ,...)
genre9 = Genre(id=9, 'Isekai')

genre9.animes.append(anime_object)
db.session.commit()
"""
# The relation 'genres' table might be like this // genres comes from line 31 of code
""" association_genres
    anime_id    |    genre_id    |    title       |    genre    |
    7           |    4           |    Arifureta   |    Isekai   |
"""

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    # Insert all data into database.
    for node in get_all_anime():
        node = node['node']
        anime_id = node['id']
        anime_details = get_anime_by_id(anime_id)
        anime = Anime(
            anime_details['id'],
            anime_details['title'],
            int(anime_details['rank']),
            int(anime_details['popularity']),
            anime_details['media_type'],
            anime_details['status'],
            anime_details['rating']
        )
        try:
            # insert anime
            db.session.add(anime)
            db.session.commit()
            print(f"Finished add Anime: {anime.title}")
        except Exception as e:
            print(e)
            db.session.rollback()

        insert_sub_table(db, anime_details, Genre, 'genres', 'id', 'name')
        insert_sub_table(db, anime_details, Studio, 'studios', 'id', 'name')
        insert_sub_table_with_node(db, anime_details, RelatedAnime, 'related_anime', 'id', 'title')
        insert_sub_table_with_node(db, anime_details, Recommendation, 'recommendations', 'id', 'title')
        print("Finished insert anime.\n")

    link_association(db, Genre, 'genres')
    link_association(db, Studio, 'studios')
    link_association_with_node(db, RelatedAnime, 'related_anime')
    link_association_with_node(db, Recommendation, 'recommendations')
