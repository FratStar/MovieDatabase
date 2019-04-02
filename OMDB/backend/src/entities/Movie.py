from .Conn import db

#Establishes table schema as classes and determines the methods that contains the data note the foreign keys it means there needs to be a specific order things are added to the database

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    lang = db.Column(db.String(85), )
    mov_rel_dt = db.Column(db.Date, nullable=False)
    mov_rel_country = db.Column(db.String(74))
    mov_plot = db.Column(db.String(450))
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    studio_id = db.Column(db.Integer, db.ForeignKey('studio.id'))
    ratings = db.relationship('Ratings', backref='Movie', lazy=True)
    Cast = db.relationship('Actors', secondary='movie_cast' )
    mov_writers = db.relationship('Writer', secondary='movie_writers')
    mov_genres = db.relationship('Genre', secondary='movie_genres' )
    def __init__(self, title, year, runtime, lang, mov_rel_dt, mov_rel_country, mov_plot, director_id, studio_id):
        self.title = title
        self.year = year
        self.runtime = runtime
        self.lang = lang
        self.mov_rel_dt = mov_rel_dt
        self.mov_rel_country = mov_rel_country
        self.mov_plot = mov_plot
        self.director_id = director_id
        self.studio_id = studio_id


class Directors(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    moviesd = db.relationship('Movie', backref='director',lazy=True)
    def __init__(self, name):
        self.name = name

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50), unique=True, nullable=False)
    moviesg = db.relationship("Movie", secondary="movie_genres")
    def __init__(self, genre):
        self.genre = genre

class Actors(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    moviesa = db.relationship("Movie", secondary="movie_cast")
    def __init__(self, name):
        self.name = name

class Studio(db.Model):
    __tablename__ = 'studio'
    id = db.Column(db.Integer, primary_key=True)
    studioname = db.Column(db.String(50), unique=True, nullable=False)
    moviess = db.relationship('Movie', backref='prod')
    def __init__(self, studioname):
        self.studioname = studioname

class Ratings(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    outlet = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float(15),  nullable=False)
    def __init__(self, movie_id, outlet, score):
        self.movie_id = movie_id
        self.outlet = outlet
        self.score = score

class Writer(db.Model):
    __tablename__ = 'writer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    moviesw = db.relationship("Movie", secondary="movie_writers")
    def __init__(self, name):
        self.name = name

class Movie_Cast(db.Model):
    __tablename__ = 'movie_cast'
    id = db.Column(db.Integer, primary_key=True)
    movies_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    actors_id = db.Column(db.Integer, db.ForeignKey('actors.id'))
    movie = db.relationship(Movie, backref=db.backref('movie_cast', cascade="all, delete-orphan"))
    actor = db.relationship(Actors, backref=db.backref('movie_cast', cascade="all, delete-orphan"))
    def __init__(self, movies_id, actors_id):
        self.movies_id = movies_id
        self.actors_id = actors_id


class Movie_Writers(db.Model):
    __tablename__ = 'movie_writers'
    id = db.Column(db.Integer, primary_key=True)
    movies_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    writer_id = db.Column(db.Integer, db.ForeignKey('writer.id'))
    movie = db.relationship(Movie, backref=db.backref('movie_writers', cascade="all, delete-orphan"))
    writer = db.relationship(Writer, backref=db.backref('movie_writer', cascade="all, delete-orphan"))
    def __init__(self, movies_id, writer_id):
        self.movies_id = movies_id
        self.writer_id = writer_id

class Movie_Genres(db.Model):
    __tablename__ = 'movie_genres'
    id = db.Column(db.Integer, primary_key=True)
    movies_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    movie = db.relationship(Movie, backref=db.backref('movie_genres', cascade="all, delete-orphan"))
    genre = db.relationship(Genre, backref=db.backref('movie_genres', cascade="all, delete-orphan"))
    def __init__(self, movies_id, genre_id):
        self.movies_id = movies_id
        self.genre_id = genre_id


