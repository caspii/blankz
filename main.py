import logging

from flask import Flask, render_template, request, flash, redirect, url_for, abort
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
@app.route('/add_section/<url_string>/', methods=['GET'])
def add_section_get(url_string=None):
    form = StoryCreateForm(request.form)
    if url_string == None:
        # We're creating a new story
        return render_template('add_section.html', form=form)
    else:
        # We got a key and are adding to an existing story
        game = Game.get_game(url_string)
        if game == None:
            abort(404)
        incomplete_slot = game.get_incomplete_slot()
        if incomplete_slot is None:
            # Game is complete
            return render_template('complete.html')
        form.slot_key.data = incomplete_slot.get_url_string()
        form.game_key.data = url_string
        return render_template('add_section.html', form=form, url_string=url_string)

@app.route('/add_section/', methods=['POST'])
def add_section_post():
    form = StoryCreateForm(request.form)
    if form.game_key.data == "":
        print "Creating game"
        # We're creating a new story
        game = Game.new()
        url_string = game.get_url_string()
        incomplete_slot = game.get_incomplete_slot()
        incomplete_slot.save(form.section.data)
        return redirect('/game/' + url_string)
        flash('Great, your entry has been saved')
    else:
        # We got a key and are adding to an existing story
        url_string = form.game_key.data
        game = Game.get_game(url_string)
        if game == None:
            abort(404)
        incomplete_slot = Slot.get_slot(form.slot_key.data)
        if incomplete_slot.state == SlotState.Complete:
            # Slot was completed in the meantime
            flash('Somebody beat you to it, your entry was not saved')
        else:
            incomplete_slot = Slot.get_slot(form.slot_key.data)
            incomplete_slot.save(form.section.data)
            flash('Great, your entry has been saved')
        return redirect('/game/' + url_string)



# @app.route('/store_section', methods=['POST'])
# def store_section():

@app.route('/game/<url_string>')
def game(url_string):
    game = Game.get_game(url_string)
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
