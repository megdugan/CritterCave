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
        # print(name)
        # print(username)
        # print(password)
        uid = profile.sign_up(conn, name, username, password)
        # if duplicate key error, flash message
        if uid == -1:
            flash(f"Username [ {username} ] is taken. Please try again.")
            return render_template('signup.html')
        # if a different error occured, flash message
        if uid == -2:
            flash("An error has occured.")
            return render_template('signup.html')
        # if successful, redirect to user's page
        user = profile.get_user_info(conn,uid)
        critters = profile.get_critters_by_user(conn,uid)
        flash(f"Welcome to Critter Cave, {user['name']}.")
        return render_template('profile.html', user=user, critters=critters)

@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        # if method is get, send a blank form
        return render_template('signin.html', page_title='Sign In')
    else:
        # if method is post, get contents of filled in form
        conn = dbi.connect()
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        print(password)
        uid = profile.sign_in(conn, username, password)
        # if duplicate key error, flash message
        if uid == -1:
            flash("Incorrect password. Please try again.")
            return render_template('signin.html')
        # if a different error occured, flash message
        if uid == -2:
            flash(f"Username [ {username} ] does not exist. Please sign up or try again.")
            return render_template('signin.html')
        # if successful, redirect to user's page
        user = profile.get_user_info(conn,uid)
        critters = profile.get_critters_by_user(conn,uid)
        flash(f"Welcome back, {user['name']}.")
        return render_template('profile.html', user=user, critters=critters)

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

@app.route('/critter_upload/', methods=['POST', 'GET'])
def critter_upload():
    print(f'Uploading a critter')

    if request.method == 'GET':
        # Send the update form
        return render_template('criiter_upload.html')
    else:
        # Method is post, and button is update, form has been filled out
        # Add the critter to the database
        conn = dbi.connect()
        uid = session['uid']
        imagePath = None
        name = request.form.get('critter-name')
        desc = request.form.get('critter-desc')
        critter = critter.add_critter(conn, uid, imagePath, name, desc)
        uid = critter['uid']
        cid = critter['cid']

        # Add the photo to the uploads folder, using critter{cid} as the name
        nm = "critter" + uid
        f = request.files['critter-pic']
        user_filename = f.filename
        ext = user_filename.split('.')[-1]
        filename = secure_filename('{}.{}'.format(nm,ext))
        pathname = os.path.join(app.config['uploads'],filename)
        f.save(pathname)

        # Update the critter element in database to have the correct image path
        critter.update_critter(conn, cid, pathname, name, desc)

        # Forward the user to the new critter's page
        return redirect(url_for('critter_page'), cid=cid)
    
@app.route('/critter/<cid>/story_upload/')
def story_upload(cid):
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
