from flask_restx.fields import List

from dao.movie import MovieDAO
from dao.model.movie import Movies


class MovieService:

    def __init__(self, dao: MovieDAO):
        self.movie_dao = dao

    def get_all_movies(self):# -> List["Movies"]:
        return self.movie_dao.get_all()

    def get_one_movie(self,mid):
        return self.movie_dao.get_one(mid)

    def create_movie(self,movie_data):
        return self.movie_dao.create(movie_data)

    def update_movie(self,mid, movie_data):
        return self.movie_dao.update(mid,movie_data)

    def delete_movie(self,mid):
        return self.movie_dao.delete(mid)
