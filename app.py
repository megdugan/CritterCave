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

@app.route('/login/')
def login():
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
def critter_page(cid):
    print(f'looking up critter with cid {cid}')
    if not cid.isdigit():
        flash('cid must be a string of digits')
        return redirect( url_for('index'))
    cid = int(cid)
    conn = dbi.connect()
    critter_info = critter.get_critter_by_id(conn,cid)
    uid = critter_info['uid']
    user = profile.get_user_info(conn,uid)
    if user is None:
        flash(f'No profile found with uid={uid}')
        return redirect(url_for('index'))
    if critter_info is None:
        flash(f'No critter found with cid={cid}')
        return redirect(url_for('index'))
    return render_template(
        'critter.html',
        user=user,
        critter_info=critter_info
    )

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
