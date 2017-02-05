import logging

from flask import Flask, render_template, request, flash, redirect, url_for, abort
from model import Game, Slot
from wtforms import Form, StringField, validators

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/explanation')
def explanation():
    return render_template('explanation.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = StoryCreateForm(request.form)
    if request.method == 'GET':
        return render_template('add_section.html', form=form)
    else:
        game = Game.new()
        url_string = game.get_url_string()
        incomplete_slot = game.get_incomplete_slot()
        incomplete_slot.save(form.section.data)
        flash('Great, your entry has been saved')
        return redirect('/game/' + url_string)

@app.route('/game/<url_string>/add_section', methods=['GET', 'POST'])
def add_section(url_string):
    form = StoryCreateForm(request.form)
    game = Game.get_game(url_string)
    if game == None:
        abort(404)
    incomplete_slot = game.get_incomplete_slot()
    if incomplete_slot is None:
        # Game is complete
        return render_template('complete.html')
    if request.method == 'GET':
        return render_template('add_section.html', form=form)
    else:
        incomplete_slot.save(form.section.data)
        flash('Great, your entry has been saved')
        return redirect('/game/' + url_string)




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
