import requests, json, sys, ast, datetime, re, urllib
from flask import Flask, render_template, jsonify, request, make_response
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from .entities.Conn import db, app
from .entities.Movie import Movie, Ratings, Directors, Genre, Actors, Studio, Writer, Movie_Cast, Movie_Genres, Movie_Writers



Bootstrap(app)
CORS(app)

db.create_all()

global r
global json_data

def add_actor_data():
    json_data = r.json()
    exists = Movie.query.filter_by(title=json_data['Title']).scalar() is not None
    ActorName = str(json_data['Actors'])
    ActorName = ActorName.split(', ')
    for a in ActorName:
        exists = Actors.query.filter_by(name=a).scalar() is not None
        if not exists:
            global actor_data   
            actor_data = Actors(a)
            db.session.add(actor_data)
            db.session.commit()

def add_writer_data():
    json_data = r.json()
    WriterName = str(json_data['Writer'])
    result = WriterName.find(',')
    if result != -1:
        WriterName = WriterName.split(', ')
        for w in WriterName:
            w = re.sub(r" ?\([^)]+\)", "", w)
            exists = Writer.query.filter_by(name=w).scalar() is not None
            if not exists:
                global writer_data 
                writer_data = Writer(w)
                db.session.add(writer_data)
                db.session().commit()
    else:
        WriterName = str(json_data['Writer'])
        writer_data = Writer(WriterName)
        db.session.add(writer_data)
        db.session().commit()

def add_directors():
    json_data = r.json()
    if json_data['Director'] != 'N/A':
        director_name = str(json_data['Director'])
        exists = Directors.query.filter_by(name=director_name).scalar() is not None
        if not exists:
            director_data = Directors(director_name)
            db.session.add(director_data)
            db.session.commit()

def add_studio():
    json_data = r.json()
    if json_data['Production'] != 'N/A':
        studio_name = str(json_data['Production'])
        exists = Studio.query.filter_by(studioname=studio_name).scalar() is not None
        if not exists:
            studio_data = Studio(studio_name)
            db.session.add(studio_data)
            db.session.commit()

def add_genres():
    json_data = r.json()
    genre_names = str(json_data['Genre'])
    result = genre_names.find(',')
    if result != -1:
        genre_names = genre_names.split(", ")
        for gn in genre_names:
            exists = Genre.query.filter_by(genre=gn).scalar() is not None
            if not exists:
                genre_data = Genre(gn)
                db.session.add(genre_data)
                db.session.commit()
    else:
        genre_data = Genre(genre_names)
        db.session.add(genre_data)
        db.session().commit()

def add_mov():
    json_data = r.json()
    exists = Movie.query.filter_by(title=json_data['Title']).scalar() is not None # check if movie exist
    if not exists:
        title = str(json_data['Title'])
        # Goes through the json dataset and extracts information if it is available
        if json_data['Year']!='N/A':
            year = int(json_data['Year'])
        if json_data['Runtime']!='N/A':
            runtime = int(json_data['Runtime'].split()[0])
        if json_data['Language']!='N/A':
            lang = str(json_data['Language'].split(', ')[0])
        if json_data['Released']!='N/A':
            rel_dt = json_data['Released']
            rel_dt = datetime.datetime.strptime(rel_dt, '%d %b %Y')
        if json_data['Country']!='N/A':
            country = str(json_data['Country'].split(', ')[0])
        plot = str(json_data['Plot'])
        global movie_data
        movie_data = Movie(title, year, runtime, lang, rel_dt.date(), country, plot, Directors.query.with_entities(Directors.id).filter_by(name=str(json_data['Director'])), Studio.query.with_entities(Studio.id).filter_by(studioname=str(json_data['Production'])))
        db.session.add(movie_data)
        db.session.commit()

def add_ratings():
    json_data = r.json()
    #Movieid = Movie.query.with_entities(Movie.id).filter_by(title=str(json_data['Title'])) # search for specific movie id to add to data base
    if json_data['Metascore']!='N/A':
        metascore = float(json_data['Metascore'])
        rating_data = Ratings(Movie.query.with_entities(Movie.id).filter_by(title=str(json_data['Title'])),'Metacritic',metascore)
        db.session.add(rating_data)
        db.session.commit()
    else:
        metascore=-1
        rating_data = Ratings(Movie.query.with_entities(Movie.id).filter_by(title=str(json_data['Title'])),'Metacritic',metascore)
        db.session.add(rating_data)
        db.session.commit()
    if json_data['imdbRating']!='N/A':
        imdb_rating = float(json_data['imdbRating'])
        rating_data = Ratings(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title']),'IMDB',imdb_rating)
        db.session.add(rating_data)
        db.session.commit()
    else:
        imdb_rating=-1
        rating_data = Ratings(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title']),'IMDB',imdb_rating)
        db.session.add(rating_data)
        db.session.commit()

def add_movie_cast():
    json_data = r.json()
    ActorName = str(json_data['Actors'])
    ActorName = ActorName.split(', ')
    for a in ActorName:
        ActorID = Actors.query.with_entities(Actors.id).filter_by(name=a)
        exists = Movie_Cast.query.filter_by(actors_id=ActorID).scalar() is not None
        if not exists:
            cast_data = Movie_Cast(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']), Actors.query.with_entities(Actors.id).filter_by(name=a))
            db.session.add(cast_data)
            db.session.commit()

def add_movie_genre():
    json_data = r.json()
    genre_names = str(json_data['Genre'])
    result = genre_names.find(',')
    if result != -1:
        genre_names = genre_names.split(", ")
        for gn in genre_names:
            GenreID = Genre.query.with_entities(Genre.id).filter_by(genre=gn)
            exists = Movie_Genres.query.filter_by(genre_id=GenreID).scalar() is not None
            if not exists:
                genre_data = Movie_Genres(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']),Genre.query.with_entities(Genre.id).filter_by(genre=gn))
                db.sesson.add(genre_data)
                db.sesson.commit()
    else:
        genre_data = Movie_Genres(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']), Genre.query.with_entities(Genre.id).filter_by(genre=genre_names))
        db.session.add(genre_data)
def add_movie_writer():
    json_data = r.json()
    WriterName = str(json_data['Writer'])
    result = WriterName.find(',')
    if result != -1:
        WriterName = WriterName.split(", ")
        for w in WriterName:
            w = re.sub(r" ?\([^)]+\)", "", w)
            WriterID = Writer.query.with_entities(Writer.id).filter_by(name=w)
            exists = Movie_Writers.query.filter_by(writer_id=WriterID).scalar() is not None
            if not exists:
                writer_data = Movie_Writers(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']), Writer.query.with_entities(Writer.id).filter_by(name=w))
                db.session.add(writer_data)
                db.session.commit()
    else:
        WriterName = re.sub(r" ?\([^)]+\)", "", WriterName)
        writer_data = Movie_Writers(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']), Writer.query.with_entities(Writer.id).filter_by(name=WriterName))
        db.session.add(writer_data)
        db.session.commit()

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/movie', methods=['GET'])
def get_movie():
    title = str(json_data['Title']) 
    year = str(json_data['Year'])
    title = urllib.parse.quote(title)
    r = requests.get(f'http://www.omdbapi.com/?t={title}&y={year}&apikey=e165dea8')
    data = r.json()
    #print(data, file=sys.stdout)
    return jsonify(data)

@app.route('/movie', methods=['POST'])
def add_Movie():
    global json_data
    json_data = request.get_json()
    title = str(json_data['Title'])
    year = str(json_data['Year'])
    title = urllib.parse.quote(title)
    global r
    r = requests.get(f'http://www.omdbapi.com/?t={title}&y={year}&apikey=e165dea8')
    add_actor_data()
    add_writer_data()
    add_directors()        
    add_studio()
    add_genres()    
    add_mov()
    add_ratings()
    add_movie_cast()
    add_movie_genre()
    add_movie_writer()
  
if __name__ == '__main__':
    app.run(debug=True)
