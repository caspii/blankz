import logging

from flask import Flask, render_template, request, flash, redirect, url_for, abort, session
from model import Game, Slot, SlotState
from wtforms import Form, StringField, HiddenField, validators


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/explanation')
def explanation():
    return render_template('explanation.html')


@app.route('/add_section/', methods=['GET'])
@app.route('/add_section/<game_key>/', methods=['GET'])
def add_section_get(game_key=None):
    form = StoryCreateForm(request.form)
    if game_key == None:
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
            return render_template('complete.html')
    form.slot_key.data = free_slot.get_slot_key()
    form.game_key.data = game_key
    return render_template('add_section.html', form=form)

@app.route('/add_section/', methods=['POST'])
def add_section_post():
    form = StoryCreateForm(request.form)
    if form.validate():
        free_slot = Slot.get_slot(form.slot_key.data)
        free_slot.save(form.section.data)
        game_key = form.game_key.data
        flash('Great, your entry has been saved')
        return redirect('/game/' + game_key)
    return render_template('add_section.html', form=form)


@app.route('/game/<game_key>')
def game(game_key):
    game = Game.get_game(game_key)
    if game == None:
        abort(404)
    complete_slot_count = len(game.get_completed_slots())
    if game.slot_count == complete_slot_count:
        return render_template('complete.html')
    else:
        return render_template('incomplete.html', slot_count=game.slot_count,
            complete_slot_count=complete_slot_count)


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


class StoryCreateForm(Form):
    #story_title = StringField('Give your story a name', [validators.Length(min=1, max=25), validators.DataRequired()])
    section = StringField('Section', [validators.Length(min=3, max=240)])
    game_key = HiddenField()
    slot_key = HiddenField()
