from flask import request
from sqlalchemy import desc

from dao.model.movie import Movies
from dao.model.genre import Genres
from dao.model.director import Directors


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Movies.id, Movies.title, Movies.year,
                                       Movies.description, Movies.trailer,
                                       Movies.genre_id,
                                       Genres.name.label('genre_name'),
                                       Movies.rating,
                                       Movies.director_id
                                       , Directors.name.label('director_name')
                                       ).join(Genres, Movies.genre_id == Genres.id) \
            .join(Directors, Movies.director_id == Directors.id).filter(
            (Movies.year == request.args.get('year') if request.args.get('year') is not None else 1 == 1),
            (Genres.id == request.args.get('genre_id') if request.args.get('genre_id') is not None else 1 == 1),
            (Directors.id == request.args.get('director_id') if request.args.get('director_id') is not None else 1 == 1)
        ).order_by(desc(Movies.year), Movies.title).all()

    def get_one(self, mid):
        return self.session.query(Movies.id, Movies.title, Movies.year,
                                       Movies.description, Movies.trailer,
                                       Movies.genre_id,
                                       Genres.name.label('genre_name'),
                                       Movies.rating,
                                       Movies.director_id
                                       , Directors.name.label('director_name')
                                       ).join(Genres, Movies.genre_id == Genres.id).join(Directors,
                                                                                         Movies.director_id == Directors.id).filter(
            Movies.id == mid
        ).order_by(desc(Movies.year), Movies.title).all()

    def create(self,movie_data):
        mov = Movies(**movie_data)
        self.session.add(mov)
        self.session.commit()
        return mov

    def update(self, mid, movie_details):
        movie_to_edit = Movies.query.get(mid)

        movie_to_edit.title = movie_details.get('title')
        movie_to_edit.description = movie_details.get('description')
        movie_to_edit.trailer = movie_details.get('trailer')
        movie_to_edit.year = movie_details.get('year')
        movie_to_edit.rating = movie_details.get('rating')
        movie_to_edit.genre_id = movie_details.get('genre_id')
        movie_to_edit.director_id = movie_details.get('director_id')

        self.session.add(movie_to_edit)
        self.session.commit()
        return "edited", 201

    def delete(self, mid):
        mov = self.session.query(Movies).get(mid)
        self.session.delete(mov)
        self.session.commit()
        return mov