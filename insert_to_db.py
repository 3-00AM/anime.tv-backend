import requests

from model import *

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
    for node in get_all_anime():
        node = node['node']
        anime_id = node['id']
        anime_details = get_anime_by_id(anime_id)
        anime = Anime(anime_details['id'], anime_details['title'], int(anime_details['rank']), int(
            anime_details['popularity']), anime_details['media_type'], anime_details['status'], anime_details['rating'])
        print("finished create class")
        try:
            db.session.add(anime)
            db.session.commit()
            print("Finished commit table")
        except Exception as e:
            print(e)
            db.session.rollback()

    print(get_all_anime())