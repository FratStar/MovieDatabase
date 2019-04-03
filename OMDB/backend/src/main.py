import requests, json, sys, ast, datetime, re, urllib
from flask import Flask, render_template, jsonify, request, make_response
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from .entities.Conn import db, app
from .entities.Movie import Movie, Ratings, Directors, Genre, Actors, Studio, Writer, Lang, Release_Country, Movie_Cast, Movie_Genres, Movie_Writers, Movie_Lang, Movie_Rel_Country



Bootstrap(app)
CORS(app)

db.create_all()     #Creates database and its tables (In this setup the db already exists but this just creates the tables anyway.)

global r            #Creating global response variable to allow for data to be passed between each functions
global json_data    #Creating global variable to hold json data so that it may be called requested once and use for all subsequent functions

def add_actor_data(): 
    json_data = r.json() #assigns json response to global variable
    exists = Movie.query.filter_by(title=json_data['Title']).scalar() is not None #querys database and determines if the movie title is there (scalar does the check) not really doing anything in this artifact of iterating the code can delete
    ActorName = str(json_data['Actors']) #transforms json response into string data type to be manipulated by string functions
    ActorName = ActorName.split(', ') #There isn't a scenario in a movie where there is a single actor so data is spliut into a string array
    for a in ActorName:
        exists = Actors.query.filter_by(name=a).scalar() is not None  #Checks database for the the actor's name  if it isn't there add it to the data base if not do not add them to the data base.
        if not exists:
            actor_data = Actors(a)
            db.session.add(actor_data)
            db.session.commit()

def add_writer_data():    
    add_mov()
    json_data = r.json()
    WriterName = str(json_data['Writer'])
    result = WriterName.find(',') #Searches comma for multiple writers.
    if result != -1:
        WriterName = WriterName.split(', ') # if there us a comma split the writers into an array
        for w in WriterName:
            w = re.sub(r" ?\([^)]+\)", "", w) #take said array and remove any text that is in a paretheseis etc. We just wnat the name
            exists = Writer.query.filter_by(name=w).scalar() is not None # checks to see if writer name exists adds then adds it to the db if it doesn't exist
            if not exists:
                writer_data = Writer(w)
                db.session.add(writer_data)
                db.session().commit()
    else:   #takes if there is a single writer take the name remove any unnecessary carachters and add to db
        WriterName = str(json_data['Writer'])
        WriterName = re.sub(r" ?\([^)]+\)", "", WriterName)
        exists = Writer.query.filter_by(name=WriterName).scalar() is not None
        if not exists:
            writer_data = Writer(WriterName)
            db.session.add(writer_data)
            db.session().commit()

def add_directors(): #same process as actors
    json_data = r.json()
    if json_data['Director'] != 'N/A':
        director_name = str(json_data['Director'])
        exists = Directors.query.filter_by(name=director_name).scalar() is not None
        if not exists:
            director_data = Directors(director_name)
            db.session.add(director_data)
            db.session.commit()

def add_studio():#same process as actors
    json_data = r.json()
    if json_data['Production'] != 'N/A':
        studio_name = str(json_data['Production'])
        exists = Studio.query.filter_by(studioname=studio_name).scalar() is not None
        if not exists:
            studio_data = Studio(studio_name)
            db.session.add(studio_data)
            db.session.commit()

def add_genres(): #same process as writers minus the regular expressions
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
        exists = Genre.query.filter_by(genre=genre_names).scalar() is not None
        if not exists:
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
     #   if json_data['Language']!='N/A':
      #      lang = str(json_data['Language'].split(', ')[0])
        if json_data['Released']!='N/A':
            rel_dt = json_data['Released']
            rel_dt = datetime.datetime.strptime(rel_dt, '%d %b %Y')
      #  if json_data['Country']!='N/A':
       #     country = str(json_data['Country'].split(', ')[0])
        plot = str(json_data['Plot'])
        movie_data = Movie(title, year, runtime, rel_dt.date(), plot, Directors.query.with_entities(Directors.id).filter_by(name=str(json_data['Director'])), Studio.query.with_entities(Studio.id).filter_by(studioname=str(json_data['Production'])))
        db.session.add(movie_data)
        db.session.commit()

def add_ratings():
    json_data = r.json()
    #Movieid = Movie.query.with_entities(Movie.id).filter_by(title=str(json_data['Title'])) # search for specific movie id to add to data base
    if json_data['Metascore']!='N/A':
        metascore = float(json_data['Metascore'])
        rating_data = Ratings(Movie.query.with_entities(Movie.id).filter_by(title=str(json_data['Title'])),'Metacritic',metascore)  #added metacritic score to database while grabbing movie id from the Movies tables
        db.session.add(rating_data)
        db.session.commit()

    else:
        metascore=-1
        rating_data = Ratings(Movie.query.with_entities(Movie.id).filter_by(title=str(json_data['Title'])),'Metacritic',metascore) #if there is no meta score assign it to -1. We don't anticipate a situation where this will ever be true but we have to hanlde it nonetheless
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

def add_country():
    json_data = r.json()
    if json_data['Country']!='N/A':
        country_names = str(json_data['Country'])
        result = country_names.find(',')
        if result != -1:
            country_names = country_names.split(', ')
            for cn in country_names:
                exists = Release_Country.query.filter_by(name=cn).scalar() is not None
                if not exists:
                    country_data = Release_Country(cn)
                    db.session.add(country_data)
                    db.session.commit()
    else:
        exists = Release_Country.query.filter_by(name=country_names).scalar() is not None
        if not exists:
            country_data = Release_Country(country_names)
            db.session.add(country_data)
            db.session().commit()

def add_movie_country():
    json_data = r.json()
    if json_data['Country']!='N/A':
        country_names = str(json_data['Country'])
        result = country_names.find(',')
        MovieID = Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year'])
        if result != -1:
            country_names = country_names.split(', ')
            for cn in country_names:
                CountryID = Release_Country.query.with_entities(Release_Country.id).filter_by(name=cn)
                exists = Movie_Rel_Country.query.filter_by(country_id=CountryID, movies_id=MovieID).scalar() is not None
                if not exists:
                    country_data = Movie_Rel_Country(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']), Release_Country.query.with_entities(Release_Country.id).filter_by(name=cn))
                    db.session.add(country_data)
                    db.session().commit()
        else:
            CountryID = Release_Country.query.with_entities(Release_Country.id).filter_by(name=country_names)
            exists = Movie_Rel_Country.query.filter_by(country_id=CountryID, movies_id=MovieID).scalar() is not None
            if not exists:
                    country_data = Movie_Rel_Country(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']), Release_Country.query.with_entities(Release_Country.id).filter_by(name=country_names))
                    db.session.add(country_data)
                    db.session().commit()


def add_language():
    json_data = r.json()
    if json_data['Language']!='N/A':
        lang_names = str(json_data['Language'])
        result = lang_names.find(',')
        if result != -1:
            lang_names = lang_names.split(', ')
            for ln in lang_names:
                exists = Lang.query.filter_by(language=ln).scalar() is not None
                if not exists:
                    lang_data = Lang(ln)
                    db.session.add(lang_data)
                    db.session.commit()
        else:
            exists = Lang.query.filter_by(language=lang_names).scalar() is not None
            if not exists:
                lang_data = Lang(lang_names)
                db.session.add(lang_data)
                db.session().commit()

def add_movie_lang():
    json_data = r.json()
    if json_data['Language']!='N/A':
        lang_names = str(json_data['Language'])
        result = lang_names.find(',')
        MovieID = Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year'])
        if result != -1:
            lang_names = lang_names.split(', ')
            for ln in lang_names:
                LangID = Lang.query.with_entities(Lang.id).filter_by(language=ln)
                exists = Movie_Lang.query.filter_by(language_id=LangID, movies_id=MovieID).scalar() is not None
                if not exists:
                    lang_data = Movie_Lang(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']), Lang.query.with_entities(Lang.id).filter_by(language=ln))
                    db.session.add(lang_data)
                    db.session.commit()
        else:
            LangID = Lang.query.with_entities(Lang.id).filter_by(language=lang_names)
            exists = Movie_Lang.query.filter_by(language_id=LangID, movies_id=MovieID).scalar() is not None
            if not exists:
                lang_data = Movie_Lang(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']), Lang.query.with_entities(Lang.id).filter_by(language=lang_names))
                db.session.add(lang_data)
                db.session.commit()

#this function looks at actors and the movie id in the movie cast tables and if that combination is not there they are added to the table

def add_movie_cast():
    json_data = r.json()
    ActorName = str(json_data['Actors'])
    ActorName = ActorName.split(', ')
    MovieID = Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year'])
    for a in ActorName:
        ActorID = Actors.query.with_entities(Actors.id).filter_by(name=a)
        exists = Movie_Cast.query.filter_by(actors_id=ActorID, movies_id=MovieID).scalar() is not None
        if not exists:
            cast_data = Movie_Cast(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']), Actors.query.with_entities(Actors.id).filter_by(name=a))
            db.session.add(cast_data)
            db.session.commit()
        

#this function looks at genre id and the movie id in the movie cast tables and if that combination is not there they are added to the table

def add_movie_genre():
    json_data = r.json()
    genre_names = str(json_data['Genre'])
    result = genre_names.find(',')
    MovieID = Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year'])
    if result != -1:
        genre_names = genre_names.split(", ")
        for gn in genre_names:
            GenreID = Genre.query.with_entities(Genre.id).filter_by(genre=gn)
            exists = Movie_Genres.query.filter_by(genre_id=GenreID, movies_id=MovieID).scalar() is not None
            if not exists:
                genre_data = Movie_Genres(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']),Genre.query.with_entities(Genre.id).filter_by(genre=gn))
                db.session.add(genre_data)
                db.session.commit()
    else:
        GenreID = Genre.query.with_entities(Genre.id).filter_by(genre=genre_names)
        exists = Movie_Genres.query.filter_by(genre_id=GenreID, movies_id=MovieID).scalar() is not None
        if not exists:
            genre_data = Movie_Genres(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']), Genre.query.with_entities(Genre.id).filter_by(genre=genre_names))
            db.session.add(genre_data)
            db.session.commit()

#this function looks at writer id and the movie id in the movie cast tables and if that combination is not there they are added to the table
         
def add_movie_writer():
    json_data = r.json()
    WriterName = str(json_data['Writer'])
    result = WriterName.find(',')
    MovieID = Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year'])
    if result != -1:
        WriterName = WriterName.split(", ")
        for w in WriterName:
            w = re.sub(r" ?\([^)]+\)", "", w)
            WriterID = Writer.query.with_entities(Writer.id).filter_by(name=w)
            exists = Movie_Writers.query.filter_by(writer_id=WriterID, movies_id=MovieID).scalar() is not None
            if not exists:
                writer_data = Movie_Writers(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']), Writer.query.with_entities(Writer.id).filter_by(name=w))
                db.session.add(writer_data)
                db.session.commit()
    else:
        WriterName = re.sub(r" ?\([^)]+\)", "", WriterName)
        WriterID = Writer.query.with_entities(Writer.id).filter_by(name=WriterName)
        exists = Movie_Writers.query.filter_by(writer_id=WriterID, movies_id=MovieID).scalar() is not None
        if not exists:
            writer_data = Movie_Writers(Movie.query.with_entities(Movie.id).filter_by(title=json_data['Title'], year=json_data['Year']), Writer.query.with_entities(Writer.id).filter_by(name=WriterName))
            db.session.add(writer_data)
            db.session.commit()


#rest api paths / is basically useless, but /movie takes in two methods get and post. Post methods trigger population of the table after pulling data from the api, get methods pulls the data from the api and that's it
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/movie', methods=['GET'])
def get_movie():
    title = str(json_data['Title'])
    year = str(json_data['Year'])
    title = urllib.parse.quote(title)
    r = requests.get(f'http://www.omdbapi.com/?t={title}&y={year}&tomatoes=true&apikey=e165dea8')
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
    r = requests.get(f'http://www.omdbapi.com/?t={title}&y={year}&tomatoes=true&apikey=e165dea8')
    add_actor_data()
    add_writer_data()
    add_directors()        
    add_studio()
    add_genres()
    add_language()
    add_country()        
    add_mov()
    add_mov()
    add_ratings()
    add_movie_cast()
    add_movie_genre()
    add_movie_writer()
    add_movie_country()
    add_movie_lang()
    return 'Sucess'
  
if __name__ == '__main__':
    app.run(debug=True)
