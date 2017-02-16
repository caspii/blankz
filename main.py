import logging
import humantime

from flask import Flask, render_template, request, flash, redirect, url_for, abort, session, make_response
from model import Game, Slot, SlotState
from wtforms import Form, StringField, HiddenField, validators
from texts import get_text_for_slot



app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def get_previous_games(cookies):
    """Return a list of previous game keys from the cookied that are passed in"""
    cookie_string = cookies.get('previous_games')
    previous_games = []
    if cookie_string is not None:
        previous_games = cookie_string.split("+")
    return previous_games

def has_seen_game(cookies, game_key):
    """Returns a boolean denoting whether user has visited this game before """
    previous_games = get_previous_games(cookies)
    if previous_games is not None and game_key in previous_games:
        return True
    else:
        return False

@app.route('/')
def landing():
    previous_games_key_list = get_previous_games(request.cookies)
    previous_games = []
    for key in previous_games_key_list:
        game = Game.get_game(key)
        if game == None:
            continue
        game.url = game.get_game_key()
        game.completed_slot_count = len(game.get_completed_slots())
        if game.completed_slot_count == 0:
            continue
        elapse_time = humantime.pretty_date(game.date_created)
        if (game.slot_count == game.completed_slot_count):
            game.status = "Completed story created " + elapse_time
        else:
            game.status = "Story with %s of %s blanks filled in. " \
                % (game.completed_slot_count, game.slot_count)
            game.status += "Created " + elapse_time
        previous_games.append(game)
    print previous_games
    return render_template('landing.html', previous_games=previous_games)

@app.route('/explanation')
def explanation():
    session.pop('last_created_key', None) # Disarm back key mechanism
    return render_template('explanation.html')

@app.route('/join/<game_key>')
def join(game_key):
    game = Game.get_game(game_key)
    if game == None:
        abort(404)
    completed_slots = game.get_completed_slots()
    if game.slot_count == len(completed_slots):
        flash('Sorry, you cannot contribute to the story because it is already complete ')
        return redirect('/game/' + game_key)
    if has_seen_game(request.cookies,game_key):
        flash('You\'ve already added your contribution to this story')
        return redirect('/game/' + game_key)
    else:
        return render_template('explanation.html', game_key=game_key)

@app.route('/add_section/', methods=['GET'])
@app.route('/add_section/<game_key>/', methods=['GET'])
def add_section_get(game_key=None):
    print "ADD SECTION CALLED"
    form = StoryCreateForm(request.form)
    if game_key == None:
        if 'last_created_key' in session:
            # User came here via back button. Fire back key mechanism
            return redirect('/add_section/' + session['last_created_key'])
        # We're creating a new story
        game = Game.new()
        game_key = game.get_game_key()
        free_slot = game.get_free_slot()
    else:
        # We're adding to an existing story
        game = Game.get_game(game_key)
        if game == None:
            abort(404)
        free_slot = game.get_free_slot()
        if free_slot is None:
            # Game is complete
            return redirect('/game/' + game_key)
    form.slot_key.data = free_slot.get_slot_key()
    form.game_key.data = game_key
    section_texts = get_text_for_slot(free_slot.slot_order)
    return render_template('add_section.html', form=form,
        section_texts=section_texts)

@app.route('/add_section/', methods=['POST'])
def add_section_post():
    form = StoryCreateForm(request.form)
    free_slot = Slot.get_slot(form.slot_key.data)
    if form.validate():
        free_slot.save(form.section.data)
        game_key = form.game_key.data
        session['last_created_key'] = game_key # Arm back key mechanism
        flash('Great, your entry has been saved')
        return redirect('/game/' + game_key)
    else:
        print "Validation error"
        section_texts = get_text_for_slot(free_slot.slot_order)
        return render_template('add_section.html', form=form,
            section_texts=section_texts)


@app.route('/game/<game_key>')
def game(game_key):
    game = Game.get_game(game_key)
    if game == None:
        abort(404)
    completed_slots = game.get_completed_slots()
    if game.slot_count == len(completed_slots):
        story_text = tuple(a.text for a in completed_slots)
        return render_template('complete.html', story_text=story_text)
    else:
        response = make_response(render_template('incomplete.html',
            slot_count=game.slot_count,
            completed_slot_count=len(completed_slots),
            game_key=game_key))
        previous_games = set(get_previous_games(request.cookies))
        previous_games.add(game_key)
        cookie_string = "+".join(previous_games)
        response.set_cookie('previous_games', cookie_string, max_age=10 * 365 * 24 * 60 * 60)
        return response


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('A 500 error occurred during a request.')
    return 'An internal error occurred.', 500


@app.errorhandler(404)
def page_not_found(e):
    logging.info('A 404 error occurred during a request.')
    return render_template('404.html'), 404


class StoryCreateForm(Form):
    #story_title = StringField('Give your story a name', [validators.Length(min=1, max=25), validators.DataRequired()])
    section = StringField('Section', [validators.Length(min=3, max=240)])
    game_key = HiddenField()
    slot_key = HiddenField()
