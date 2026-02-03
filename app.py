import os
import requests  # WICHTIG: Oben importieren!
from flask import Flask, render_template, request, redirect, url_for, abort
from data_manager import DataManager
from models import db
from models import db, User, Movie
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = DataManager()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# --- Hilfsfunktion für OMDb ---
def get_omdb_data(title):
    api_key = "dd74a077"
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('Response') == 'True':
            return {
                'title': data.get('Title'),
                'director': data.get('Director'),
                'year': data.get('Year'),
                'poster': data.get('Poster')
            }
    except Exception:
        return None
    return None


# --- Routen ---
@app.route('/')
def index():
    all_users = data_manager.get_users()
    # Wir übergeben 'users' (die Liste), nicht 'user'
    return render_template('index.html', users=all_users)


@app.route('/users', methods=['POST'])
def add_user():
    user_name = request.form.get('name')
    if user_name:
        data_manager.create_user(user_name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    # 1. Den DataManager die Arbeit machen lassen
    success = data_manager.delete_user(user_id)

    # 2. Zurück zur Startseite leiten
    return redirect(url_for('index'))

@app.route('/users/<int:user_id>')
def list_user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/add_movie', methods=['POST'])
def add_movie(user_id):
    title = request.form.get('title')
    if not title:
        abort(400)

    movie_info = get_omdb_data(title)

    if movie_info:
        data_manager.add_movie(
            movie_info['title'],
            movie_info['director'],
            movie_info['year'],
            movie_info['poster'],
            user_id
        )
    else:
        # Fallback, falls Film nicht gefunden wurde
        data_manager.add_movie(title, "Unbekannt", 0, "https://via.placeholder.com/150", user_id)

    return redirect(url_for('list_user_movies', user_id=user_id))


@app.route('/movies/update/<int:movie_id>', methods=['POST'])
def update_movie_route(movie_id):
    new_title = request.form.get('new_title')
    if new_title:
        data_manager.update_movie(movie_id, new_title)

    # movie = Movie.query.get(movie_id) benötigt den Import von Movie!
    movie = Movie.query.get(movie_id)
    return redirect(url_for('list_user_movies', user_id=movie.user_id))

@app.route('/users/<int:user_id>/movies/delete/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('list_user_movies', user_id=user_id))


if __name__ == '__main__':
    with app.app_context():
        os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
        db.create_all()

    # Hier erzwingen wir Port 5001
    app.run(debug=True, port=5001)