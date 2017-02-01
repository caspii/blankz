import logging

from flask import Flask, render_template, request, flash, redirect, url_for
from model import Game, Slot
from google.appengine.ext import ndb

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/explanation')
def explanation():
    return render_template('explanation.html')

@app.route('/add_section', methods=['GET', 'POST'])
def add_section():
    print("Add_section")
    if request.method == 'GET':
        return render_template('add_section.html')
    else:
        new_game_key = Game().put()
        Slot(game=new_game_key, text='Sweet').put()
        Slot(game=new_game_key, text='DUDE').put()
        url_string = new_game_key.urlsafe()
        return redirect('/incomplete/' + url_string)


@app.route('/incomplete/<key>')
def incomplete(key):
    flash('Great, your entry has been saved')
    return render_template('incomplete.html')

@app.route('/complete')
def complete():
    flash('Great, your entry has been saved')
    return render_template('complete.html')



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
