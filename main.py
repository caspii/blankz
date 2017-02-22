import logging
import humantime
import sendmail

from flask import Flask, render_template, request, flash, redirect, url_for, abort, session, make_response
from model import Game, Slot, SlotState
from wtforms import Form, StringField, HiddenField, validators, FieldList
from wtforms.fields.html5 import EmailField
from texts import get_texts_for_slot



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
            game.status = "Story that %s of %s people have joined. " \
                % (game.completed_slot_count, game.slot_count)
            game.status += "Created " + elapse_time
        previous_games.append(game)
    return render_template('landing.html', previous_games=previous_games)

@app.route('/explanation')
def explanation():
    session.pop('last_created_key', None) # Disarm back key mechanism
    return render_template('explanation.html')

@app.route('/about')
def about():
    return render_template('about.html')

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
    form = StoryCreateForm(request.form)
    form.sections.append_entry()
    form.sections.append_entry()
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
    section_texts = get_texts_for_slot(free_slot.slot_order)
    return render_template('add_section.html', form=form,
        section_texts=section_texts)

@app.route('/add_section/', methods=['POST'])
def add_section_post():
    form = StoryCreateForm(request.form)
    free_slot = Slot.get_slot(form.slot_key.data)
    if form.validate():
        free_slot.save(form.sections.data)
        game_key = form.game_key.data
        session['last_created_key'] = game_key # Arm back key mechanism
        flash('Great, your entry has been saved')
        return redirect('/game/' + game_key)
    else:
        section_texts = get_texts_for_slot(free_slot.slot_order)
        return render_template('add_section.html', form=form,
            section_texts=section_texts)


@app.route('/game/<game_key>',methods=['GET','POST'])
def game(game_key):
    try:
        game = Game.get_game(game_key)
    except Exception as e:
        logging.exception("Game could not be retrieved")
        abort(404)
    if game is None:
        abort(404)
    form = EmailSaveForm(request.form)
    completed_slots = game.get_completed_slots()
    if request.method == 'POST' and form.validate():
        # save email here
        game.save_email(form.email.data)
        flash("Your email address was saved")
    if game.slot_count == len(completed_slots):
        story_text = tuple(a.text for a in completed_slots)
        # Send story completed mail, unless this has already happened.
        if game.email_sent == False:
            sendmail.gameComplete(game)
            print "SENDING MAIL"
            game.set_email_sent()
        else:
            print "NOT SENDING MAIL"

        return render_template('complete.html', story_text=story_text)
    else:
        missing_slots = game.slot_count - len(completed_slots)
        response = make_response(render_template('incomplete.html',
            missing_slots=missing_slots, game_key=game_key, form=form))
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
    sections = FieldList(StringField('Section', [validators.Length(min=3, max=240)]))
    game_key = HiddenField()
    slot_key = HiddenField()

class EmailSaveForm(Form):
    email = EmailField('email', [validators.DataRequired(), validators.Email()])
