
from flask import Flask
from flask_restx import Api

from config import Config
from setup_db import db

from dao.model.user import User

from views.movie import movies_ns
from views.genre import genres_ns
from views.director import directors_ns
from views.user import user_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


# функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movies_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(user_ns)
    # create_data(app, db)



# def create_data(app, db):
#     with app.app_context():
#         db.create_all()
#
#         u1 = User(username="adnerew", password="my_little_pony", role="user")
#         u2 = User(username="vlad", password="qwerty", role="user")
#         u3 = User(username="admin", password="admin", role="admin")
#
#         with db.session.begin():
#             db.session.add_all([u1,u2,u3])


app = create_app(Config())
app.debug = True
#
if __name__ == '__main__':
    # app.run(host="localhost", port=10001, debug=True)
    app.run(host="localhost", debug=True)
