import logging

from flask import Flask, render_template, request, flash, redirect, url_for, abort
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
    if request.method == 'GET':
        return render_template('add_section.html')
    else:
        new_game = Game()
        new_game_key = Game().put()
        new_game.create_slots(new_game_key)
        url_string = new_game_key.urlsafe()
        flash('Great, your entry has been saved')
        return redirect('/game/' + url_string)


@app.route('/game/<url_string>')
def game(url_string):
    game_key = ndb.Key(urlsafe=url_string)
    game = game_key.get()
    if game == None:
        abort(404)
    # print(game)
    slots = Slot.query(ndb.AND(Slot.game == game.key, Slot.state == 3))
    # Print completed slots
    for slot in slots:
        print(slot)
    if game.complete:
        return render_template('complete.html')
    else:
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

@app.errorhandler(404)
def page_not_found(e):
    logging.info('An error occurred during a request.')
    return render_template('404.html'), 404
