import requests

from model import *
from urllib.parse import quote
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
    url = "https://api.myanimelist.net/v2/anime/ranking?ranking_type=all&limit=500"

    response = requests.request(
        "GET", url, headers=headers, data=payload).json()

    # try:
    #     data = Anime(title, rank)

    return response['data']


def get_anime_by_id(anime_id):
    url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=id,title,rank,popularity,media_type,status,rating,studios,genres,related_anime,recommendations"

    response = requests.request(
        "GET", url, headers=headers, data=payload).json()

    return response


def get_manga_by_name(name):
    url = f"https://kitsu.io/api/edge/manga?filter[text]={quote(name)}&fields[manga]=canonicalTitle"

    response = requests.request(
        "GET", url, headers=headers, data=payload).json()

    return response


def get_theme_by_name(name):
    url = f"https://aruppi-api.herokuapp.com/api/v3/themes/{name}"

    response = requests.request(
        "GET", url, headers=headers, data=payload).json()

    return response


def insert_manga_table(db, anime):
    for data in get_manga_by_name(anime.title)['data']:
        m_id = int(data['id'])
        m_title = data['attributes']['canonicalTitle']
        manga = Manga(m_id, m_title)
        try:
            print(f"Add Manga: {m_title} to db")
            db.session.add(manga)
            db.session.commit()
        except Exception as exception:
            print(exception)
            print(f"Failed to add Manga: {m_title} to db")
            db.session.rollback()


def insert_theme_table(db, anime):
    try:
        for data in get_theme_by_name(anime.title)['themes']['themes']:
            t_title = data['title']
            t_type = data['type']
            theme = Theme(t_title, t_type)
            try:
                print(f"Add Theme: {t_title} to db")
                db.session.add(theme)
                db.session.commit()
            except Exception as e:
                print(f"Failed to add Theme: {t_title} to db")
                db.session.rollback()
    except ValueError:
        print(f"No theme found on Anime: {anime.title}")


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
        for a in db.session.query(Anime).all():
            a_detail = get_anime_by_id(a.mal_id)
            for g in a_detail[key]:
                if x.mal_id == g['id']:
                    add_and_submit_to_db(a, db, key, x)


def link_association_with_node(db, Table, key):
    for x in db.session.query(Table).all():
        for a in db.session.query(Anime).all():
            a_detail = get_anime_by_id(a.mal_id)
            for g in a_detail[key]:
                if x.mal_id == g['node']['id']:
                    add_and_submit_to_db(a, db, key, x)


def link_manga_association(db):
    for a in db.session.query(Anime).all():
        for data in get_manga_by_name(a.title)['data']:
            for x in db.session.query(Manga).all():
                if int(data['id']) == x.kitsu_id:
                    try:
                        print(f"Link Manga: {x.title} and Anime: {a.title}")
                        x.animes.append(a)
                        db.session.commit()
                    except Exception as exception:
                        print(f"Failed to Link Manga: {x.title} and Anime: {a.title}")

def link_theme_association(db):
    for a in db.session.query(Anime).all():
        try:
            for data in get_theme_by_name(a.title)['themes']['themes']:
                for x in db.session.query(Theme).all():
                    if data['title'] == x.title:
                        try:
                            print(f"Link Theme: {x.title} and Anime: {a.title}")
                            x.animes.append(a)
                            db.session.commit()
                        except Exception as exception:
                            print(f"Failed to Link Theme: {x.title} and Anime: {a.title}")
        except ValueError:
            continue


def add_and_submit_to_db(a, db, key, x):
    try:
        print(
            f"Link {key}: {x.mal_id} and Anime: {a.title}")
        x.animes.append(a)
        db.session.commit()
    except Exception as exception:
        print(exception)
        db.session.rollback()
        print(
            f"Failed to link {key}: {x.mal_id} and Anime: {a.title}")


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
            print(f"Failed to add Anime: {anime.title}")
            db.session.rollback()

        insert_sub_table(db, anime_details, Genre, 'genres', 'id', 'name')
        insert_sub_table(db, anime_details, Studio, 'studios', 'id', 'name')
        insert_sub_table_with_node(db, anime_details, RelatedAnime, 'related_anime', 'id', 'title')
        insert_sub_table_with_node(db, anime_details, Recommendation, 'recommendations', 'id', 'title')
        insert_manga_table(db, anime)
        insert_theme_table(db, anime)

    # link_association(db, Genre, 'genres')
    # link_association(db, Studio, 'studios')
    # link_association_with_node(db, RelatedAnime, 'related_anime')
    # link_association_with_node(db, Recommendation, 'recommendations')
    # link_manga_association(db)
    # link_theme_association(db)
