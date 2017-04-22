def index():
    form = FORM(INPUT(_name='q', requires=IS_NOT_EMPTY(), _placeholder='Find a song...'),
                _action=URL('default', 'search'), _method='post')
    quote_list = db(db.quotes).select()
    return dict(form=form, quotes=quote_list)


def albums():
    form = FORM(INPUT(_name='album', requires=IS_NOT_EMPTY(), _placeholder='Find an album...'),

                _action=URL('default', 'search_album'), _method='post')
    album_list = db(db.albums).select()
    return dict(form=form, albums=album_list)


def artists():
    form = FORM(INPUT(_name='artist', requires=IS_NOT_EMPTY(), _placeholder='Find an artist...'),

                _action=URL('default', 'search_artist'), _method='post')
    artist_list = db(db.artists).select()
    return dict(form=form, artists=artist_list)


def genres():
    form = FORM(INPUT(_name='genre', requires=IS_NOT_EMPTY(), _placeholder='Find a genre...'),

                _action=URL('default', 'search_genre'), _method='post')
    genre_list = db(db.genres).select()
    return dict(form=form, genres=genre_list)


def search():
    form = FORM(INPUT(_name='q', requires=IS_NOT_EMPTY(), _placeholder='Find another song...'),

                _action=URL('default', 'search'), _method='post')
    search_result = db((db.songs.song_name.contains(request.vars.q))).select()
    return dict(form=form,search_result=search_result)


def search_album():
    form = FORM(INPUT(_name='album', requires=IS_NOT_EMPTY(), _placeholder='Find an album...'),

                _action=URL('default', 'search_album'), _method='post')
    search_result2 = db((db.albums.album_name.contains(request.vars.album))).select()
    return dict(form=form,albums=search_result2)


def search_artist():
    form = FORM(INPUT(_name='artist', requires=IS_NOT_EMPTY(), _placeholder='Find an artist...'),

                _action=URL('default', 'search_artist'), _method='post')
    search_result3 = db((db.artists.artist_name.contains(request.vars.artist))).select()
    return dict(form=form,artists=search_result3)


def search_genre():
    form = FORM(INPUT(_name='genre', requires=IS_NOT_EMPTY(), _placeholder='Find a genre...'),

                _action=URL('default', 'search_genre'), _method='post')
    search_result4 = db((db.genres.genre_name.contains(request.vars.genre))).select()
    return dict(form=form,genres=search_result4)


def alltracks():
    song_list = db(db.songs).select()
    return dict(all_tracks=song_list)



def contact():
    if auth.user:
        form = SQLFORM(db.contact)
        if form.process().accepted:
           response.flash = 'Your message has been sent.'
    else:
        redirect('index')
    return dict(form=form)



def about():
    return locals()


def album():
    album_id = db(db.albums.album_url == request.args[0]).select(db.albums.id).first()
    song_list = db(db.songs.album_url == album_id).select()
    return dict(album_list=song_list)


def genre():
    genre_id = db(db.genres.genre_url == request.args[0]).select(db.genres.id).first()
    songlist = db(db.songs.genre_url == genre_id).select()
    return dict(genre_list=songlist)


def artist():
    artist_id = db(db.artists.artist_url == request.args[0]).select(db.artists.id).first()
    song_list = db(db.songs.artist_url == artist_id).select()
    return dict(artist_list=song_list)


def report():
    return locals()


def management():
    return locals()


def user():
    auth.settings.logged_url = URL('user', args='profile')
    return dict(form=auth())


def artist_management():
    db.artists.artist_url.writable = db.artists.artist_url.readable = False

    if not auth.user:
        redirect(URL('default', 'index'))
    elif auth.user.id == 1:
        grid = SQLFORM.grid(db.artists,
                            csv=False,
                            searchable=False,
                            user_signature=True,
                            paginate=20,
                            maxtextlength=40,
                            deletable=True,
                            editable=True,
                            details=True)
    else:
        redirect(URL('default', 'index'))
    return locals()


def album_management():
    db.albums.album_url.writable = db.albums.album_url.readable = False
    if not auth.user:
        redirect(URL('default', 'index'))
    elif auth.user.id == 1:
        grid = SQLFORM.grid(db.albums,
                            csv=False,
                            user_signature=True,
                            searchable=False,
                            paginate=20,
                            maxtextlength=30,
                            deletable=True,
                            editable=True,
                            details=True)
    else:
        redirect(URL('default', 'index'))
    return locals()


def song_management():
    db.songs.song_url.writable = db.songs.song_url.readable = False
    if not auth.user:
        redirect(URL('default', 'index'))
    elif auth.user.id == 1:
        grid = SQLFORM.grid(db.songs,
                            csv=False,
                            user_signature=True,
                            searchable=False,
                            paginate=20,
                            maxtextlength=50,
                            deletable=True,
                            editable=True,
                            details=True)
    else:
        redirect(URL('default', 'index'))
    return locals()

def contact_management():
    if not auth.user:
        redirect(URL('default', 'index'))
    elif auth.user.id == 1:
        grid = SQLFORM.grid(db.contact,
                            csv=False,
                            user_signature=True,
                            searchable=False,
                            paginate=20,
                            maxtextlength=30,
                            deletable=True,
                            editable=False,
                            details=True,
                            create=False)
    else:
        redirect(URL('default', 'index'))
    return locals()


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
