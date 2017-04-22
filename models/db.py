# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################

db.define_table('genres',
                Field('genre_name', label="Genre Name", notnull=True),
                Field('genre_url', label="Genre URL", notnull=True, unique=True),
                Field('genre_info', 'text', label="Genre INFO", notnull=True),
                Field('cultural_origins',label="Cultural Origins", notnull=True),
                Field('popular_in',label="Popular in", notnull=True))


db.define_table('artists',
                Field('artist_name', label="Artist Name", notnull=True),
                Field('artist_url', label="Artist URL", notnull=True, unique=True),
                Field('genre_name', 'reference genres', requires= IS_IN_DB(db,db.genres,'%(genre_name)s'), label="Genre Name"),
                Field('band_or_not','boolean',label="Band or Not ?"),
                Field('first_member',label="First Member Name"),
                Field('second_member',label="Second Member Name"),
                Field('third_member',label="Third Member Name"),
                Field('years_active',label="Years Active"),
                Field('awards',label="Awards"),
                Field('origin',label="Origin"))

db.define_table('albums',
                Field('album_name',label="Album Name", notnull=True),
                Field('album_url',label="Album Url", notnull=True, unique=True),
                Field('genre_name', 'reference genres', requires= IS_IN_DB(db,db.genres,'%(genre_name)s'),label="Genre Name"),
                Field('artist_name', 'reference artists', requires= IS_IN_DB(db,db.artists,'%(artist_name)s'),label="Owner"),
                Field('released','date',label="Released Date"),
                Field('albuminfo','text',label="Album information", notnull=True),
                Field('sold',label="Sold"),
                Field('number_of_songs',label="Number of Songs"),
                Field('studio',label="Studio"),
                Field('album_length',label="Length", notnull=True))

db.define_table('songs',
                Field('song_name',label="Song Name", notnull=True),
                Field('song_url',label="Song Url", notnull=True, unique=True),
                Field('song_length',label="Length"),
                Field('album_url','reference albums', requires= IS_IN_DB(db,db.albums,'%(album_url)s'),label="Album URL"),
                Field('genre_url','reference genres', requires= IS_IN_DB(db,db.genres,'%(genre_url)s'),label="Genre URL"),
                Field('artist_url','reference artists', requires= IS_IN_DB(db,db.artists,'%(artist_url)s'),label="Artist URL"))

db.define_table('quotes',
                Field('quote_text','text', notnull=True),
                Field('quote_owner', notnull=True))

db.define_table('contact',
                Field('name',label="Your Name", notnull=True),
                Field('surname',label="Your Surame", notnull=True),
                Field('email',label="Your E-mail Address",notnull=True),
                Field('message2','text',label="Message",notnull=True))


