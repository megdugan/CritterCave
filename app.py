from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
import secrets
import cs304dbi as dbi

import profile  # profile / user methods
import critter  # critter methods
import story    # story methods
import settings # settings methods

app = Flask(__name__)

# We need a secret_key to use flash() and sessions
app.secret_key = secrets.token_hex()

# For project work, use your team db
print(dbi.conf('crittercave_db'))

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    return render_template('main.html', page_title='Main Page')

@app.route('/about/')
def about():
    flash('this is a flashed message')
    return render_template('about.html', page_title='About Us')

@app.route('/login/')
def login():
    return

@app.route('/<uid>')
def user_profile():
    return

@app.route('/<cid>')
# page for when you click into a critter to see their stories
def critter_page():
    return

@app.route('/critter_upload')
def critter_upload():
    return
    
@app.route('/<cid>/story_upload')
def story_upload():
    return


if __name__ == '__main__':
    import sys, os
    dbi.conf('crittercave_db')
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
