# файл для создания DAO и сервисов чтобы импортировать их везде

# book_dao = BookDAO(db.session)
# book_service = BookService(dao=book_dao)
#
# review_dao = ReviewDAO(db.session)
# review_service = ReviewService(dao=review_dao)
from dao.user import UserDAO
from service.movie import MovieService
from service.genre import GenreService
from service.director import DirectorService
from service.user import UserService

from setup_db import db
from dao.movie import MovieDAO
from dao.director import DirectorDAO
from dao.genre import GenreDAO

movie_dao = MovieDAO(db.session)
movie_service = MovieService(dao=movie_dao)

director_dao = DirectorDAO(db.session)
director_service = DirectorService(dao=director_dao)

genre_dao = GenreDAO(db.session)
genre_service = GenreService(dao=genre_dao)

user_dao = UserDAO(db.session)
user_service = UserService(dao=user_dao)