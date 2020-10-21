#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import datetime
import enum
from sqlalchemy.exc import SQLAlchemyError
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: (DONE) connect to a local postgresql database
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
# Relationship: ARTIST(one)<=======>(many)SHOW(many)<=======>(one)VENUE
#----------------------------------------------------------------------------#

genrelist = enum.Enum("genre",GENRE_CHOICES)
#current_time = "5"
current_time = datetime.datetime.now().strftime('%Y-%m-%d')

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)    
    genre = db.relationship('ArtistGenre', backref='genre_artist')
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    seeking = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    shows = db.relationship('Show', backref='show_artist')


# TODO: (DONE) implement any missing fields, as a database migration using Flask-Migrate

# TODO (DONE) Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column( db.Integer, db.ForeignKey('artist.id'), nullable=False)
    venue_id= db.Column( db.Integer, db.ForeignKey('venue.id'), nullable=False)
    start_time= db.Column(db.Integer, nullable=False) #make this date later: db.Column(db.DateTime, nullable=False)


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    genre = db.relationship('VenueGenre', backref='genre_venue')
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    seeking = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    shows = db.relationship('Show', backref='show_venue')

    # (DONE) TODO: implement any missing fields, as a database migration using Flask-Migrate

#---------ADDED CLASS FOR GENRE TABLES-------------------

class ArtistGenre(db.Model):
    __tablename__ = 'aristgenre'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.Enum(genrelist))
    artist_id = db.Column( db.Integer, db.ForeignKey('artist.id'))

class VenueGenre(db.Model):
    __tablename__ = 'venuegenre'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.Enum(genrelist))
    venue_id = db.Column( db.Integer, db.ForeignKey('venue.id'))

#------END MODELS---------------------------------------------




#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

##---------------------------------------------------------------------------#
# CONTROLLERS
##---------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# VENUE - Controllers
#----------------------------------------------------------------------------#
#  Venues - Create (GET and POST)
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: (DONE)insert form data as a new Venue record in the db, instead
  # TODO: (DONE)modify data to be the data object returned from db insertion

  ##Intantiate classes in form.py
  form = VenueForm()

  ## Get information on form (html)
  data = request.form #data from from

  ## Interact with data generated by wtforms to get "genres" and "seeking"
  #Get genre
  genre_data = form.genres.data # interact with Multiselect option
  #Get seeking state
  seeking = form.seeking.data #interact with seeking checkbox button

  #####DEBUG##############
  print("TEST TO MAKE SURE GENRE IS GOOD")
  for x in genre_data:
    print(x)
  print("SEEKING " + str(form.seeking.data))
  #####DEBUG END##############


  try:
    ## Create new venue
    new_venue = Venue(
      name=data.get("name"),
      #genre added below
      address=data.get("address"),
      city=data.get("city"),
      state=data.get("state"),
      phone=data.get("phone"),
      seeking=seeking,
      seeking_description=data.get("seeking_description"),
      image_link=data.get("image_link"),
      facebook_link=data.get("facebook_link"),
      website=data.get("website_link")
      #shows will be assigned in shows section
      )


    ## Insert/Add new venue to db
    db.session.add(new_venue)

    ## Create new venue genre and add to db
    for genre_select in genre_data:
      #create venue genre
      new_venue_genre = VenueGenre(genre_venue = new_venue, genre=genre_select)
      db.session.add(new_venue_genre)

    #Commit the items to DB
    db.session.commit()

    flash('Venue ' + data.get("name") + ' was successfully listed!')

  except SQLAlchemyError as e:
    db.session.rollback() #Rollback if there is an error
    flash('An error occurred. Venue ' + data.get("name") + ' could not be listed.')

  finally:
    db.session.close() #close the DB session

  return render_template('pages/home.html')

  # on successful db insert, flash success
  #undo comment: flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: (DONE) on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #undo comment: return render_template('pages/home.html')


#  Venues - ALL
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  # current_show_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  city_and_state = ''
  data=[]
  venue_query = Venue.query.group_by(Venue.id, Venue.city, Venue.state).all()

  #use enumerate function to make the list countable
  for count, venue in enumerate(venue_query):
    #uncomment below when ready for time/date
    #upcoming_shows = venue.shows.filter(Show.start_time > current_show_time).all()
    upcoming_shows = venue.shows
    no_of_shows = len(upcoming_shows) #if no shows created, it returns 0
    print("Venue " + str(count+1) + " : " + str(venue.name))
    print("Venue Shows : " + str(no_of_shows))
    print("Venue City and State : " + str(venue.city) + str(venue.state))

    if city_and_state == str(venue.city) + str(venue.state):
      data[len(data) - 1]["venues"].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len(upcoming_shows)
      })

    else:
      city_and_state = str(venue.city)  + str(venue.state)
      data.append({
        "city": venue.city,
        "state": venue.state,
        "venues": [{
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": len(upcoming_shows)
        }]
      })

  return render_template('pages/venues.html', areas=data)

#  Venues - By ID
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.filter_by(id=venue_id).first()
  
  if venue:
    
    #upcoming shows
    upcoming_shows = []
    shows_up = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time >= current_time).all()
    for show in shows_up:
      artist = Artist.query.get(show.venue_id)
      upcoming_shows.append(
          {
            "artist_id": show.venue_id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(show.start_time)
          })
    
    #past shows
    past_shows = []
    shows_past = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time < current_time).all()
    for show in shows_past:
      artist = Artist.query.get(show.venue_id)
      past_shows.append(
          {
            "artist_id": show.venue_id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(show.start_time)
          })
      
    #artist genre
    venuegenre = []
    genres = VenueGenre.query.filter_by(venue_id=venue_id).all()
    print(genres)
    for genre in genres:
      venuegenre.append(
            genre.genre.name
          )
  
    
    
    data_list=[{
          "id": venue.id, 
          "name": venue.name, 
          "genres": venuegenre,
          "address" : venue.address,
          "city": venue.city,
          "state": venue.state,
          "phone": venue.phone,
          "website": venue.website,
          "facebook_link": venue.facebook_link,
          "seeking": venue.seeking,
          "seeking_description": venue.seeking_description,
          "image_link": venue.image_link,
          "past_shows": past_shows,
          "upcoming_shows": upcoming_shows,
          "past_shows_count": len(past_shows),
          "upcoming_shows_count": len(upcoming_shows),
          }]  
      
      
    data = list(filter(lambda d: d['id'] == venue_id, data_list))[0]

    return render_template('pages/show_venue.html', venue=data)
  else:
    return render_template('errors/no_venue.html')

#  Venues - DELETE
#  ----------------------------------------------------------------

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  # TODO: (DONE) Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: (DONE) Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  error = False
  try:
    del_venue = Venue.query.get(venue_id)
    #del_venue = Venue.filter_by(Venue.id==venue_id).first()
    deleted_name = del_venue.name #Get name of item to be deleted
    deleted_id = del_venue.id #Get id of item to be deleted


    db.session.delete(del_venue)
    #Venue.query.get(venue_id).delete()
    db.session.commit()


    flash('Venue: "' + str(deleted_name) + '" with id, '+str(deleted_id) +' was successfully Deleted!')

  except SQLAlchemyError as e:
    db.session.rollback() #Rollback if there is an error
    error=True
    flash('An error occurred.')

  finally:
    db.session.close() #close the DB session

  if error:
    abort(500)
  else:
    return render_template('pages/home.html')


  #return redirect(url_for('show_venue', venue_id=venue_id))

#  Venues - Edit By ID (GET and POST)
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  #venue_query = Venue.query.filter_by(id=venue_id).first()
  venue_query = Venue.query.get(venue_id)



  print(str(venue_query.id))
  venue={
    "id": venue_query.id,
    "name": venue_query.name
    }

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

##Intantiate classes in form.py
  form = VenueForm()

  ## Get information on form (html)
  data = request.form #data from from

  ## Interact with data generated by wtforms to get "genres" and "seeking"
  #Get genre
  genre_data = form.genres.data # interact with Multiselect option
  #Get seeking state
  seeking = form.seeking.data #interact with seeking checkbox button

  #####DEBUG##############
  print("TEST TO MAKE SURE GENRE IS GOOD")
  for x in genre_data:
    print(x)
  print("SEEKING " + str(form.seeking.data))
  #####DEBUG END##############


  try:
    ## Edit venue
    edit_venue = Venue.query.get(venue_id)
    current_venue_name = edit_venue.name #get old name
    #edit_venue = Venue.query.filter(id==venue_id).update(
    #edit_venue = Venue.update().where(Venue.c.id==venue_id).values(
    edit_venue.name=data.get("name")
    edit_venue.address=data.get("address")
    edit_venue.city=data.get("city")
    edit_venue.state=data.get("state")
    edit_venue.phone=data.get("phone")
    edit_venue.seeking=seeking
    edit_venue.seeking_description=data.get("seeking_description")
    edit_venue.image_link=data.get("image_link")
    edit_venue.facebook_link=data.get("facebook_link")
    edit_venue.website=data.get("website_link")
    #shows will be assigned in shows section



    ## Insert/Add edited venue to db
    db.session.add(edit_venue)

    ## Edit venue genre and add to db
    for genre_select in genre_data:
      #Edit venue genre
      edit_venue_genre = VenueGenre(genre_venue = edit_venue, genre=genre_select)
      db.session.add(edit_venue_genre)

    #Commit the Editted items to DB
    db.session.commit()

    flash('Venue: "' + str(current_venue_name) + '" was successfully Editted!')

  except SQLAlchemyError as e:
    db.session.rollback() #Rollback if there is an error
    flash('An error occurred. Venue ' + data.get("name") + ' could not be listed.')

  finally:
    db.session.close() #close the DB session

  #return render_template('pages/home.html')


  return redirect(url_for('show_venue', venue_id=venue_id))


#  Venues - Search
#  ----------------------------------------------------------------

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # ANSWER: Do a search "like" value in the textbox, and return that as JSON
  venue_query = Venue.query.filter(Venue.name.ilike('%' + request.form['search_term'] + '%'))
  
  #delete befor submission
  s = []
  for x in venue_query:
    s.append(x)
  
  ######DEBUG#################
  for x in s:
    print(x.name)

  print ("Query type: " + str(type(venue_query)))
  print ("Data [] type: " + str(type(s)))
  #for u in venue_query:
    #print (u.__dict__)
  ######DEBUG END#############
  
  data = []
  for x in venue_query:
    data.append({"id": x.id, "name": x.name, "num_upcoming_shows": 0})
  
  response = {
     "count": venue_query.count(),
     "data": data
    }
  print(response)
    #todo: add "num_upcoming_shows"
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))





#----------------------------------------------------------------------------#
# ARTISTS - Controllers
#----------------------------------------------------------------------------#
#  Artist - Create (GET and POST) - (DONE)
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: (DONE) insert form data as a new Artist record in the db, instead
  # TODO: (DONE) modify data to be the data object returned from db insertion

  ##Intantiate classes in form.py
  form = ArtistForm()

  ## Get information on form (html)
  data = request.form #data from from

  ## Interact with data generated by wtforms to get "genres" and "seeking"
  #Get genre
  genre_data = form.genres.data # interact with Multiselect option
  #Get seeking state
  seeking = form.seeking.data #interact with seeking checkbox button

  try:
    ## Create new artist
    new_artist = Artist(
      name=data.get("name"),
      #genre added below
      address=data.get("address"),
      city=data.get("city"),
      state=data.get("state"),
      phone=data.get("phone"),
      seeking=seeking,
      seeking_description=data.get("seeking_description"),
      image_link=data.get("image_link"),
      facebook_link=data.get("facebook_link"),
      website=data.get("website_link")
      #shows will be assigned in shows section
      )


    ## Insert/Add new artist to db
    db.session.add(new_artist)

    ## Create new artist genre and add to db
    for genre_select in genre_data:
      #create artist genre
      new_artist_genre = ArtistGenre(genre_artist = new_artist, genre=genre_select)
      db.session.add(new_artist_genre)

    #Commit the items to DB
    db.session.commit()

    flash('Artist ' + data.get("name") + ' was successfully listed!')

  except SQLAlchemyError as e:
    db.session.rollback() #Rollback if there is an error
    flash('An error occurred. Artist ' + data.get("name") + ' could not be listed.')

  finally:
    db.session.close() #close the DB session

  return render_template('pages/home.html')


#  Artists - ALL (GET) - (DONE)
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: (DONE)replace with real data returned from querying the database
  data=[]
  artist_query = Artist.query.group_by(Artist.id, Artist.city, Artist.state).all()
  for artist in artist_query:
    data.append({
        "id": artist.id,
        "name": artist.name
      })
  return render_template('pages/artists.html', artists=data)

#  Artists - By ID (GET) -(DONE)
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: (DONE) replace with real artist data from the artist table, using artist_id
  
  artist = Artist.query.filter_by(id=artist_id).one()

  if artist:

    #upcoming shows
    upcoming_shows = []
    #sort shows by past
    shows_up = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time >= current_time).all()
    for show in shows_up:
      venue = Venue.query.get(show.venue_id)
      upcoming_shows.append(
          {
            "venue_id": show.venue_id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": str(show.start_time)
          })
    
    #past shows
    past_shows = []
    shows_past = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time < current_time).all()
    for show in shows_past:
      venue_past = Venue.query.get(show.venue_id)
      past_shows.append(
          {
            "venue_id": show.venue_id,
            "venue_name": venue_past.name,
            "venue_image_link": venue_past.image_link,
            "start_time": str(show.start_time)
          })

    #artist genre
    artistgenre = []
    genres = ArtistGenre.query.filter_by(artist_id=artist_id).all()
    print(genres)
    for genre in genres:
      artistgenre.append(
            genre.genre.name
          )

    data_list=[{
        'id': artist.id, 
        "name": artist.name, 
        "genres": artistgenre,
        "address" : artist.address,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking": artist.seeking,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
      }]

    data = list(filter(lambda d: d['id'] == artist_id, data_list))[0]
    return render_template('pages/show_artist.html', artist=data)
  else:
    return render_template('errors/no_artist.html')

#  Artists - Edit by ID (GET and POST) -[DONE - except genre]
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  query = Artist.query.get(artist_id)

  #use "form" to edit genre
  artist={
    "id": query.id,
    "name": query.name,
    "genres": ["Jazz"],
    "city": query.city,
    "state": query.state,
    "phone": query.phone,
    "website": query.website,
    "facebook_link": query.facebook_link,
    "seeking": query.seeking,
    "seeking_description": query.seeking_description,
    "image_link": query.image_link
  }
  # TODO: (DONE) populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

#----------POST--------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: (DONE) take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()

  ## Get information on form (html)
  data = request.form #data from from

  ## Interact with data generated by wtforms to get "genres" and "seeking"
  #Get genre
  genre_data = form.genres.data # interact with Multiselect option
  #Get seeking state
  seeking = form.seeking.data #interact with seeking checkbox button

  try:
    ## Edit venue
    edit = Artist.query.get(artist_id)
    current_name = edit.name #get old name
    edit.name=data.get("name")
    edit.address=data.get("address")
    edit.city=data.get("city")
    edit.state=data.get("state")
    edit.phone=data.get("phone")
    edit.seeking=seeking
    edit.seeking_description=data.get("seeking_description")
    edit.image_link=data.get("image_link")
    edit.facebook_link=data.get("facebook_link")
    edit.website=data.get("website_link")
    #shows will be assigned in shows section

    ## Insert/Add edited item to db
    db.session.add(edit)

    ## Edit genre and add to db
    for genres in genre_data:
      #Edit genre
      edit_genre = ArtistGenre(genre_venue = edit, genre=genres)
      db.session.add(edit_genre)

    #Commit the Editted items to DB
    db.session.commit()

    flash('Artist: "' + str(current_name) + '" was successfully Editted!')

  except SQLAlchemyError as e:
    db.session.rollback() #Rollback if there is an error
    flash('An error occurred. Artist ' + data.get("name") + ' could not be listed.')

  finally:
    db.session.close() #close the DB session

  return redirect(url_for('show_artist', artist_id=artist_id))


#  Artists - Search (POST) - [DONE except addition of "num_upcoming_shows"]
#  ----------------------------------------------------------------
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  query = Artist.query.filter(Artist.name.ilike('%' + request.form['search_term'] + '%'))
    
  data = []
  for x in query:
    data.append({"id": x.id, "name": x.name, "num_upcoming_shows": 0})
  
  response = {
     "count": query.count(),
     "data": data
    }
  print(response)
    #todo: add "num_upcoming_shows"

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))



#----------------------------------------------------------------------------#
# SHOWS - Controllers
#----------------------------------------------------------------------------#
#  Shows - Create (GET and POST)
#  ----------------------------------------------------------------
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  form = ShowForm()
  data = request.form
  try:
    ## Create new artist
    new = Show(
      artist_id=data.get("artist_id"),
      venue_id=data.get("venue_id"),
      start_time=data.get("start_time")
      )

    ## Insert/Add new artist to db
    db.session.add(new)

    #Commit the items to DB
    db.session.commit()

    flash('Show  was successfully added!')

  except SQLAlchemyError as e:
    db.session.rollback() #Rollback if there is an error
    flash('An error occurred. Show could not be created.')

  finally:
    db.session.close() #close the DB session

  return render_template('pages/home.html')


#  Shows - ALL [Done]
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }]

  data=[]
  query = Show.query.group_by(Show.start_time, Show.id).all()
  for show in query:
    venue = Venue.query.filter_by(id=show.venue_id).one()
    artist = Artist.query.filter_by(id=show.artist_id).one()
    data.append({
        "venue_id": show.venue_id,
        "venue_name": venue.name,
        "artist_id": show.artist_id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": str(show.start_time)
      })


  return render_template('pages/shows.html', shows=data)



#  ERROR HANDLING
#  ----------------------------------------------------------------
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# App Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
