""" 
(CritterCave)
Contains all the routing methods
"""

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
import secrets
import os
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

# Configure base path for all file uploads
app.config['uploads'] = '/students/crittercave/uploads'

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    return render_template('main.html', page_title='Main Page')

@app.route('/about/')
def about():
    return render_template('about.html', page_title='About Us')

@app.route('/create/')
def create():
    return render_template('create.html', page_title='Create')

@app.route('/welcome/')
def welcome():
    return render_template('welcome.html', page_title='Welcome')

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
        # change to redirect url_for
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
        # change to redirect url_for
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
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['uploads'], filename)

    
@app.route('/settings/<uid>', methods=['POST', 'GET'])
def settings_page(uid): # fix later to get uid from cookies
    if not uid.isdigit():
        flash('uid must be a string of digits')
        return redirect(url_for('index'))
    uid = int(uid)
    conn = dbi.connect()
    curr_user_info = profile.get_user_info(conn,uid)
    print(curr_user_info)
    if request.method == 'GET':
        return render_template(
            'settings.html',
            curr_user_info=curr_user_info
            )
    
    # POST: figure out which form was submitted
    action = request.form.get('action')
    
    if action == 'Update Profile Picture':
        file = request.files.get('profile-pic')
        user_filename = file.filename
        
        # handle saving file
        # Ensure the user uploads an image and name
        if file and user_filename == '':
            flash('Please add a critter image.')
            return render_template('critter_upload.html')
        
        nm = "pfp" + str(uid)
        ext = user_filename.split('.')[-1]
        filename = secure_filename(f"{nm}.{ext}")

        pathname = os.path.join(app.config['uploads'], filename)
        
        file.save(pathname)
        os.chmod(pathname, 0o444)


        # Store ONLY the filename in the DB
        settings.update_pfp(conn, uid, filename)
        flash("Profile picture updated!")
        
        return render_template('settings.html',
            curr_user_info=curr_user_info)

    elif action == 'Update Profile Info':
        new_name = request.form.get('display-name')
        new_username = request.form.get('username')
        if len(new_name) < 1:
            flash("Please enter a name.")
            return render_template('settings.html',
            curr_user_info=curr_user_info)
            
        if len(new_username) < 1:
            flash("Please enter a username.")
            return render_template('settings.html',
            curr_user_info=curr_user_info)
            
        settings.update_personal_info(conn,uid,new_name,new_username)
        flash("Profile information updated!")
        curr_user_info = profile.get_user_info(conn, uid)
        
        return render_template('settings.html',
            curr_user_info=curr_user_info)
        
    
    elif action == 'Update Password':
        old_pw = request.form.get('old_pw')
        new_pw1 = request.form.get('new_pw1')
        new_pw2 = request.form.get('new_pw2')
        
        pw_check = settings.check_password(conn,uid,old_pw,new_pw1,new_pw2)
        
        if len(new_pw1) < 6:
            flash("New password must have at least 6 characters. Please try again.")
            return render_template(
            'settings.html',
            curr_user_info=curr_user_info
            )
        
        if pw_check == -1:
            flash("Incorrect password. Please try again.")
            return render_template(
            'settings.html',
            curr_user_info=curr_user_info
            )
        elif pw_check == -2:
            flash("Please make sure the new passwords match")
            return render_template(
            'settings.html',
            curr_user_info=curr_user_info
            )
        
        # passwords must match --> update password
        settings.update_password(conn, uid, new_pw1)
        flash('Password successfully updated.')
        
        return render_template(
            'settings.html',
            curr_user_info=curr_user_info
            )
        

    elif action == 'update_appearance':
        appearance = request.form.get('appearance')
        # update appearance pref
        flash("Appearance updated!")

    else:
        flash("This is not yet implemented")

    return redirect(url_for('settings_page', uid=uid))
        

@app.route('/critter/<cid>')
# page for when you click into a critter to see their stories
def critter_page(cid):
    print(f'looking up critter with cid {cid}')
    if not cid.isdigit():
        flash('cid must be a string of digits')
        return redirect( url_for('index'))
    
    # getting critter info
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
    
    # getting story info
    stories_by_user = story.get_stories_for_critter_by_user(conn, cid, uid)
    stories_not_by_user = story.get_stories_for_critter_not_by_user(conn, cid, uid)
    print("stories_by_user")
    print(stories_by_user)
    print("stories_not_by_user")
    print(stories_not_by_user)
    return render_template(
        'critter.html',
        user=user,
        critter_info=critter_info,
        stories_by_user=stories_by_user,
        stories_not_by_user=stories_not_by_user
    )

@app.route('/critter_upload/', methods=['POST', 'GET'])
def critter_upload():
    """
    Renders critter-upload form and adds the results to 
    the database.
    """

    if request.method == 'GET':
        # Send the update form
        return render_template('critter_upload.html')
    else:
        # Method is post, form has been filled out
        conn = dbi.connect()
        session['uid'] = 1
        uid = session['uid']
        f = request.files['critter-pic']
        user_filename = f.filename
        name = request.form.get('critter-name')
        desc = request.form.get('critter-desc')

        # Ensure the user uploads an image and name
        if f and user_filename == '':
            flash('Please add a critter image.')
            return render_template('critter_upload.html')
        if name == '':
            flash('Please name the critter.')
            return render_template('critter_upload.html')
        
        # check lengths
        if len(name) > 50:
            flash('Critter name must be under 50 characters')
            return render_template('critter_upload.html')
        if len(desc) > 250:
            flash('Description must be under 250 characters')
            return render_template('critter_upload.html')

        # Add the critter to the database
        try:
            critterID = critter.add_critter(conn, uid, app.config['uploads'], name, desc)
        except:
            flash('An error occurred when uploading the critter. Please try again')
            return render_template('critter_upload.html')
        pet = critter.get_critter_by_id(conn, critterID['last_insert_id()'])

        # Add the photo to the uploads folder, using critter{cid} as the name
        cid = pet['cid']
        nm = "critter" + str(cid)
        ext = user_filename.split('.')[-1]
        filename = secure_filename(f"{nm}.{ext}")
        pathname = os.path.join(app.config['uploads'], filename)
        print(pathname)
        f.save(pathname)
        os.chmod(pathname, 0o444)
        
        # Update the critter element in database to have the correct image path
        critter.update_critter(conn, cid, filename, name, desc)

        # Forward the user to the new critter's page
        return redirect(url_for('critter_page', cid=cid))

@app.route('/critter/<cid>/story_upload/', methods=["GET", "POST"])
def story_upload(cid):
    """
    Renders story-upload form and adds the results to 
    the database.
    """

    if request.method == 'GET':
        # Send the update form
        return render_template('story_upload.html')
    else:
        # Method is post, form has been filled out
        # Add the story to the database
        conn = dbi.connect()
        session['uid'] = 1
        uid = session['uid']
        desc = request.form.get('critter-story')
        
        # check lengths
        if len(desc) > 2000:
            flash('The story cannot be longer than 2000 characters')
            return render_template('story_upload.html')

        # Ensure the user uploads a story
        if desc == '':
            flash('Please write a story.')
            return render_template('story_upload.html')
        
        # Add the story to the database
        try:
            story.add_story(conn, cid, uid, desc)
        except:
            flash('An error occurred when uploading the story. Please try again')
            return render_template('story_upload.html')
        return redirect(url_for('critter_page', cid=cid))

@app.route('/query/', methods=['GET'])
def lookup_form():
    '''
    Returns the rendered page for the query inputted to the lookup form.
    If the query result has multiple items, renders a list a clickable list of the items.
    Otherwise, renders the page of the item itself.

    Args:
        None
    Return:
        String of the rendered template -> str
    '''
    query_type = request.args.get('kind')
    query = request.args.get('query')
    conn = dbi.connect()
    if query_type == 'critter':
        critters = critter.lookup_critter(conn, query)
        if not critters:
            flash('No critters matched the query. Please try again.')
            return redirect(url_for('index'))
        if len(critters) == 1:
            return redirect(url_for('critter_page', cid=critters[0]['cid']))  # if there is only one result, go straight to the critter's page
        return render_template('critter_lookup.html', query = query, critters = critters) # renders a clickable list of critters
    if query_type == 'user':
        users = profile.lookup_user(conn, query)
        if not users:
            flash('No users matched the query. Please try again.')
            return redirect(url_for('index'))
        if len(users) == 1:
            return redirect(url_for('user_profile', uid=users[0]['uid']))  # if there is only one result, go straight to the user's page
        return render_template('user_lookup.html', query = query, users = users) # renders a clickable list of users

# @app.route('/lookup/critter/<name>')
# def critter_lookup(name):
#     '''
#     Render the critter lookup page for a given name query.
#     If no critters match, flash a message.
    
#     Args:
#         name -> string
#     Return:
#         string of the rendered template -> str
#     '''
#     return render_template(
#         'critter_lookup.html',
#     )


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
