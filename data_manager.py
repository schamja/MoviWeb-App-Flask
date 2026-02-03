from models import db, User, Movie

class DataManager:
  # Define Crud operations as methods

  def get_users(self):
      return User.query.all()

  def delete_user(self, user_id):
      user = User.query.get(user_id)
      if user:
          # Löscht den Nutzer (Dank 'backref' in deinen Models werden die Filme
          # oft automatisch mitgelöscht, wenn Cascade-Delete konfiguriert ist)
          db.session.delete(user)
          db.session.commit()
          return True
      return False

  def get_user_movies(self,user_id):
    return Movie.query.filter_by(user_id = user_id).all()

  def create_user(self, name):
    new_user = User(name =name)
    db.session.add(new_user)
    db.session.commit()
    return new_user

  def add_movie(self, name, director, year,poster_url, user_id):
      new_movie =Movie(
          name = name,
          director =director,
          year = year,
          poster_url =poster_url,
          user_id = user_id
      )
      db.session.add(new_movie)
      db.session.commit()


  def update_movie(self, movie_id, new_title):
      movie = Movie.query.get(movie_id)
      if movie:
          movie.name = new_title
          db.session.commit()


  def delete_movie(self, movie_id):
      movie = Movie.query.get(movie_id)
      if movie:
          db.session.delete(movie)  # Hier stand movie_id, muss aber das Objekt movie sein
          db.session.commit()

  def update_movie(self, movie_id, new_title):
      movie = Movie.query.get(movie_id)
      if movie:
          movie.name = new_title
          db.session.commit()  # Wichtig: Speichert die Änderung in der DB