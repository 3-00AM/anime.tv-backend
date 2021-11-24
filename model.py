from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import logging

app = Flask(__name__)
CORS(app)

app.debug = os.getenv("DEBUG")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
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


class Anime(db.Model):
    """
    A class to represent a citizen.
    Attributes:
        id              (int):       anime ID
        title           (varchar):  anime name
        rank            (int):      rank of that anime
        popularity      (int):      
        genres          (varchar):  array of genre
        media_type      (varchar):  type of media of the anime
        status          (varchar):  status of that anime
        rating          (varchar):  rating of that anime
        studios         (varchar):  array of studios
        related_anime   (varchar):  array of related anime
        related_manga   (varchar):  array of manga
        recommendations (varchar):  array of recommendation
    """
    __tablename__ = 'anime'
    id = db.Column(db.Integer, primary_key=True) # primary key
    title = db.Column(db.String(200))
    rank = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    genres = db.Column(db.ARRAY(db.String(50)))
    media_type = db.Column(db.String(50))
    status = db.Column(db.String(50))
    rating = db.Column(db.String(50))
    studios = db.Column(db.ARRAY(db.String(200)))
    related_anime = db.Column(db.ARRAY(db.String(200)))
    related_manga = db.Column(db.ARRAY(db.String(200)))
    recommendations = db.Column(db.ARRAY(db.String(200)))

    # db.Column(db.Date)
    # db.Column(db.Text())
    # db.Column(db.Boolean)
    # db.Column(db.PickleType())

    def __init__(self, title, rank, popularity, genres, media_type, status, rating, studios, related_anime, related_manga, recommendations):
        self.title = title
        self.rank = rank
        self.popularity = popularity
        self.genres = genres
        self.media_type = media_type
        self.status = status
        self.studios = studios
        self.related_anime = related_anime
        self.related_manga = related_manga
        self.recommendations = recommendations

        logger.info(f'created Anime: title: {self.title} rank: {self.rank} popularity: {self.popularity} \
            genres: {self.genres} media_type: {self.media} status: {self.status} studios: {self.studios} \
            related_anime: {self.related_anime} related_manga: {self.related_manga} recommendations: {self.recommendations}')

    def get_dict(self):
        return {
            'title': self.title,
            'rank': self.rank,
            'popularity': self.popularity,
            'genres': self.genres,
            'media_type': self.media_type,
            'status': self.status,
            'studios': self.studios,
            'related_anime': self.related_anime,
            'related_manga': self.related_manga,
            'recommendations': self.recommendations,
        }