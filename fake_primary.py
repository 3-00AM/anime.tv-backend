import random
from model import *


if __name__ == '__main__':
    Review.__table__.create(db.session.bind)
    db.session.commit()
    for anime in db.session.query(Anime).all():
        review = Review(anime.title, round(random.uniform(0, 10), 2))
        db.session.add(review)
        db.session.commit()
