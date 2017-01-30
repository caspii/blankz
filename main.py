import logging

from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/explanation')
def explanation():
    return render_template('explanation.html')

@app.route('/add_section')
def add_section():
    return render_template('add_section.html')

@app.route('/incomplete')
def incomplete():
    flash("Great, your entry has been saved")
    return render_template('incomplete.html')

@app.route('/complete')
def complete():
    flash("Great, your entry has been saved")
    return render_template('complete.html')



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
