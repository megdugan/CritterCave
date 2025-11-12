""" 
(CritterCave)
Contains all the routing methods
"""

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

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        # if method is get, send a blank form
        return render_template('signup.html', page_title='Sign Up')
    else:
        # if method is post, get contents of filled in form
        conn = dbi.connect()
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        print(name)
        print(username)
        print(password)
        uid = profile.sign_up(conn, name, username, password)
        # if duplicate key error, flash message
        if uid == -2:
            flash(f"Username [ {username} ] is taken. Please try again.")
            return redirect(url_for('signup'))
        # if a different error occured, flash message
        if uid == -1:
            flash("An error has occured.")
            return redirect(url_for('signup'))
        # if successful, redirect to user's page
        user = profile.get_user_info(conn,uid)
        critters = profile.get_critters_by_user(conn,uid)
        return render_template('profile.html', user=user, critters=critters)

@app.route('/signin/')
def signin():
    return

@app.route('/profile/<uid>')
def user_profile(uid):
    print(f'looking up user with uid {uid}')
    if not uid.isdigit():
        flash('uid must be a string of digits')
        return redirect( url_for('index'))
    uid = int(uid)
    conn = dbi.connect()
    user = profile.get_user_info(conn,uid)
    critters = profile.get_critters_by_user(conn,uid)
    if user is None:
        flash(f'No profile found with uid={uid}')
        return redirect(url_for('index'))
    return render_template(
        'profile.html',
        user=user,
        critters=critters
    )

@app.route('/critter/<cid>')
# page for when you click into a critter to see their stories
def critter_page():
    return

@app.route('/critter_upload/')
def critter_upload():
    return
    
@app.route('/critter/<cid>/story_upload/')
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
