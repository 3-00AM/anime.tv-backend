from turtle import title

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from decouple import config
import logging

app = Flask(__name__)
CORS(app)

app.debug = config("DEBUG")
app.config['SQLALCHEMY_DATABASE_URI'] = config("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s: %(message)s')

file_handler = logging.FileHandler('government.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

"""Association table for Anime and Genre"""
association_genres_table = db.Table('association_genres',
                                    db.Column('anime_id', db.Integer,
                                              db.ForeignKey('anime.id')),
                                    db.Column('genre_id', db.Integer,
                                              db.ForeignKey('genre.id')),
                                    )

"""Association table for Anime and Studio"""
association_studios_table = db.Table('association_studios',
                                     db.Column('anime_id', db.Integer,
                                               db.ForeignKey('anime.id')),
                                     db.Column('studio_id', db.Integer,
                                               db.ForeignKey('studio.id')),
                                     )

"""Association table for Anime an RelatedAnime"""
association_related_animes_table = db.Table('association_related_animes',
                                            db.Column(
                                                'anime_id', db.Integer, db.ForeignKey('anime.id')),
                                            db.Column('related_anime_id', db.Integer,
                                                      db.ForeignKey('related_anime.id')),
                                            )

"""Association table for Anime an Manga"""
association_mangas_table = db.Table('association_mangas',
                                    db.Column('anime_id', db.Integer,
                                              db.ForeignKey('anime.id')),
                                    db.Column('manga_id', db.Integer,
                                              db.ForeignKey('manga.id')),
                                    )

"""Association table for Anime an Recommendation"""
association_recommendations_table = db.Table('association_recommendations',
                                             db.Column(
                                                 'anime_id', db.Integer, db.ForeignKey('anime.id')),
                                             db.Column('manga_id', db.Integer, db.ForeignKey(
                                                 'recommendation.id')),
                                             )


class Anime(db.Model):
    """
    A class to represent a citizen.
    Attributes:
        id                      (int):  anime ID
        mal_id                  (int):  My Anime List id
        title               (varchar):  anime title
        rank                    (int):  rank of the anime
        popularity              (int):      
        genres              (varchar):  genre of the anime
        media_type          (varchar):  type of media of the anime
        status              (varchar):  status of the anime
        rating              (varchar):  rating of the anime
        studios             (varchar):  array of studios
        related_anime       (varchar):  array of related anime
        related_manga       (varchar):  array of manga
        recommendations     (varchar):  array of recommendation
    """
    __tablename__ = 'anime'
    id = db.Column(db.Integer, primary_key=True)  # primary key
    mal_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(200))
    rank = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    genres = db.relationship('Genre',
                             secondary=association_genres_table, backref=db.backref('animes', lazy='dynamic'))
    media_type = db.Column(db.String(50))
    status = db.Column(db.String(50))
    rating = db.Column(db.String(50))
    studios = db.relationship('Studio',
                              secondary=association_studios_table, backref=db.backref('animes', lazy='dynamic'))
    related_anime = db.relationship('RelatedAnime',
                                    secondary=association_related_animes_table,
                                    backref=db.backref('animes', lazy='dynamic'))
    related_manga = db.relationship('Manga',
                                    secondary=association_mangas_table, backref=db.backref('animes', lazy='dynamic'))
    recommendations = db.relationship('Recommendation',
                                     secondary=association_recommendations_table,
                                     backref=db.backref('animes', lazy='dynamic'))

    # db.Column(db.Date)
    # db.Column(db.Text())
    # db.Column(db.Boolean)
    # db.Column(db.PickleType())

    def __init__(self, mal_id, title, rank, popularity, media_type, status, rating):
        self.mal_id = mal_id
        self.title = title
        self.rank = rank
        self.popularity = popularity
        self.media_type = media_type
        self.status = status
        self.rating = rating

    def get_dict(self):
        genre_list = []
        studio_list = []
        recommendation_list = []
        for genre in self.genres:
            genre_list.append(genre.name)
        for studio in self.studios:
            studio_list.append(studio.name)
        for recommendation in self.recommendations:
            recommendation_list.append(recommendation.title)
        return {
            '_id': self.id,
            'mal_id': self.mal_id,
            'title': self.title,
            'rank': self.rank,
            'popularity': self.popularity,
            'genres': genre_list,
            'media_type': self.media_type,
            'status': self.status,
            'studios': studio_list,
            'recommendation': recommendation_list
        }


class Genre(db.Model):
    """
    A class to represent a genre.
    Attributes:
        id          (int):  genre ID
        mal_id      (int):  My Anime List id
        name    (varchar):  genre name
    """
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)  # primary key
    mal_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100))  # unique

    def __init__(self, mal_id, name):
        self.mal_id = mal_id
        self.name = name

    def get_dict(self):
        return {
            '_id': self.id,
            'mal_id': self.mal_id,
            'name': self.name,
        }


class Studio(db.Model):
    """
    A class to represent a genre.
    Attributes:
        id          (int):  studio ID
        mal_id      (int):  My Anime List id
        name    (varchar):  studio name
    """
    __tablename__ = 'studio'
    id = db.Column(db.Integer, primary_key=True)  # primary key
    mal_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100))  # unique

    def __init__(self, mal_id, name):
        self.mal_id = mal_id
        self.name = name

    def get_dict(self):
        return {
            '_id': self.id,
            'mal_id': self.mal_id,
            'name': self.name,
        }


class RelatedAnime(db.Model):
    """
    A class to represent a genre.
    Attributes:
        id           (int):  related anime ID
        mal_id       (int):  My Anime List id
        title    (varchar):  related anime title
    """
    __tablename__ = 'related_anime'
    id = db.Column(db.Integer, primary_key=True)  # primary key
    mal_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(200))

    def __init__(self, mal_id, title):
        self.mal_id = mal_id
        self.title = title

    def get_dict(self):
        return {
            '_id': self.id,
            'mal_id': self.mal_id,
            'title': self.title,
        }


class Manga(db.Model):
    """
    A class to represent a genre.
    Attributes:
        id           (int):  manga ID
        kitsu_id       (int):  My Anime List id
        title    (varchar):  manga title
    """
    __tablename__ = 'manga'
    id = db.Column(db.Integer, primary_key=True)  # primary key
    kitsu_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(200))

    def __init__(self, mal_id, title):
        self.mal_id = mal_id
        self.title = title

    def get_dict(self):
        return {
            '_id': self.id,
            'mal_id': self.mal_id,
            'title': self.title,
        }


class Recommendation(db.Model):
    """
    A class to represent a genre.
    Attributes:
        id           (int):  recommendation ID
        mal_id       (int):  My Anime List id
        title    (varchar):  anime title
    """
    __tablename__ = 'recommendation'
    id = db.Column(db.Integer, primary_key=True)  # primary key
    mal_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(200))

    def __init__(self, mal_id, title):
        self.mal_id = mal_id
        self.title = title

    def get_dict(self):
        return {
            'id': self.id,
            'mal_id': self.mal_id,
            'title': self.title,
        }


class Theme(db.Model):
    """
    A Class to represent a Theme table.
    Attributes:
        id              (int): theme ID.
        arrupi_ID       (int): arrupi id.
        title       (varchar): title of theme.
        type        (varchar): type of that songs eg. opening, ending.
    """
