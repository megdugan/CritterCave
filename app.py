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
import profile
import critter
import story
import settings

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
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))

    conn = dbi.connect()
    critter_info = critter.get_all_critters(conn)
    return render_template('main.html', critters=critter_info)

@app.route('/old_main/')
def old_main():
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))

    return render_template('old_main.html')

@app.route('/about/')
def about():
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))

    return render_template('about.html')

@app.route('/create/')
def create():
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))

    return render_template('create.html')

@app.route('/welcome/')
def welcome():
    return render_template('welcome.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    Display the sign up page / form (signup.html).
    If the sign up is successful, route to the user's profile.
    Otherwise, flash an error message.
    """
    if request.method == 'GET':
        # if method is get, send a blank form
        return render_template('signup.html', page_title='Sign Up')
    else:
        # if method is post, get contents of filled in form
        conn = dbi.connect()
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        uid = profile.sign_up(conn, name, username, password)
        # set the session for uid 
        session['uid']=uid
        session['logged_in']=True
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
        flash(f"testing if logged in {session['logged_in']}")
        # change to redirect url_for
        return render_template('profile.html', user=user, critters=critters) 

@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    """
    Display the sign in page / form (signin.html).
    If the sign up is successful, route to the user's profile.
    Otherwise, flash an error message.
    """
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

        #Set the session for uid 
        session['uid']=uid
        session['logged_in']=True
        
        print(type(uid))
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
        flash(f"testing if logged in {session['logged_in']}")
        # change to redirect url_for
        return redirect(url_for('user_profile',uid=uid))

@app.route('/profile/<uid>')
def user_profile(uid):
    """
    View a user's profile (profile.html).
    If the user views their own profile, show options to access settings and upload a story.
    """
    # session code 
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))
    # if this is not the users profile
    if int(session['uid'])!=int(uid):
        # if the user isn't viewing their own profile
        print(f'looking up user with uid {uid}')
        if not uid.isdigit():
            flash('uid must be a string of digits')
            return redirect( url_for('index'))
        # get user info and critters to display
        uid = int(uid)
        conn = dbi.connect()
        user = profile.get_user_info(conn,uid)
        user['created'] = user['created'].strftime("%m/%d/%Y")[:10]
        critters = profile.get_critters_by_user(conn,uid)
        if user is None:
            flash(f'No profile found with uid={uid}')
            return redirect(url_for('index'))
        # display profile without settings and add critter button (not logged in user)
        return render_template(
            'profile_for_none_user.html',
            user=user,
            critters=critters
        )
    print(f'looking up user with uid {uid}')
    if not uid.isdigit():
        # if the uid is of wrong type, flash message and redirect to home
        flash('uid must be a string of digits')
        return redirect( url_for('index'))
    # get user info and critters to display
    uid = int(uid)
    conn = dbi.connect()
    user = profile.get_user_info(conn,uid)
    user['created'] = user['created'].strftime("%m/%d/%Y")[:10]
    critters = profile.get_critters_by_user(conn,uid)
    if user is None:
        # if the user doesn't exist, flash message and redirect to home
        flash(f'No profile found with uid={uid}')
        return redirect(url_for('index'))
    return render_template(
        'profile.html',
        user=user,
        critters=critters
    )

@app.route('/logout/')
def logout():
    """
    Log a user out of the session.
    If the user is not logged in, flash an error message.
    """
    if 'uid' in session:
        session.pop('logged_in')
        session.pop('uid')
        flash('You are logged out!') 
        return redirect(url_for('welcome'))
    else:
        flash("You are not logged in!")
        return redirect(url_for('welcome'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Access an uploaded image/file for display.
    """
    # session code 
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))
    return send_from_directory(app.config['uploads'], filename)

    
@app.route('/settings/', methods=['POST', 'GET'])
def settings_page(): # fix later to get uid from cookies
    # session code 
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))
    # get user info for form
    uid = session['uid']
    uid = int(session['uid'])
    conn = dbi.connect()
    curr_user_info = profile.get_user_info(conn,uid)
    print(curr_user_info)
    if request.method == 'GET':
        return render_template(
            'settings.html',
            curr_user_info=curr_user_info
            )
    action = request.form.get('action')
    if action == 'Update Profile Picture':
        # if action is update pfp, update the user's profile pic
        file = request.files.get('profile-pic')
        user_filename = file.filename
        # handle saving file
        # ensure the user uploads an image and name
        if file and user_filename == '':
            flash('Please add a critter image.')
            return render_template('critter_upload.html')
        nm = "pfp" + str(uid)
        ext = user_filename.split('.')[-1]
        filename = secure_filename(f"{nm}.{ext}")
        pathname = os.path.join(app.config['uploads'], filename)
        file.save(pathname)
        os.chmod(pathname, 0o444)
        # store ONLY the filename in the DB
        settings.update_pfp(conn, uid, filename)
        flash("Profile picture updated!")
        # render the settings page with user's info
        return render_template('settings.html',
            curr_user_info=curr_user_info)
    elif action == 'Update Profile Info':
        # if action is update profile info, update the user's name or username
        new_name = request.form.get('display-name')
        new_username = request.form.get('username')
        if len(new_name) < 1:
            # if new name is None, flash error message
            flash("Please enter a name.")
            return render_template('settings.html',
            curr_user_info=curr_user_info)
        if len(new_name) > 50:
            # if new name is too long, flash error message
            flash("Name must be under 50 characters.")
            return render_template('settings.html',
            curr_user_info=curr_user_info)
        if len(new_username) < 1:
            # if new username is None, flash error message
            flash("Please enter a username.")
            return render_template('settings.html',
            curr_user_info=curr_user_info)
        if len(new_username) > 50:
            # if new username is too long, flash error message
            flash("Username must be under 50 characters.")
            return render_template('settings.html',
            curr_user_info=curr_user_info)
        try:
            # attempt to update the user's settings
            settings.update_personal_info(conn,uid,new_name,new_username)
        except:
            # if unsuccessful, flash an error message
            flash("An error occurred when updating the profile information. Please try again.")
            return render_template('settings.html',
            curr_user_info=curr_user_info)
        flash("Profile information updated!")
        curr_user_info = profile.get_user_info(conn, uid)
        # rerender settings page
        return render_template('settings.html',
            curr_user_info=curr_user_info)
    elif action == 'Update Password':
        # if action is update password, check user current password and update new password
        old_pw = request.form.get('old_pw')
        new_pw1 = request.form.get('new_pw1')
        new_pw2 = request.form.get('new_pw2')
        # check old password, and check that new password was typed correctly
        pw_check = settings.check_password(conn,uid,old_pw,new_pw1,new_pw2)
        if len(new_pw1) < 6:
            # if new password is too short, flash error message
            flash("New password must have at least 6 characters. Please try again.")
            return render_template(
            'settings.html',
            curr_user_info=curr_user_info)
        if len(new_pw1) > 60:
            # if new password is too long, flash error message
            flash("New password must be under 60 characters. Please try again.")
            return render_template(
            'settings.html',
            curr_user_info=curr_user_info)
        if pw_check == -1:
            # if original password is incorrect, flash error message
            flash("Incorrect password. Please try again.")
            return render_template(
            'settings.html',
            curr_user_info=curr_user_info
            )
        elif pw_check == -2:
            # if password matching failed, flash error message
            flash("Please make sure the new passwords match")
            return render_template(
            'settings.html',
            curr_user_info=curr_user_info
            )
        # passwords must match --> update password
        try:
            # if all is correct, attempt to update password
            settings.update_password(conn, uid, new_pw1)
        except:
            # for errors, flash general message
            flash('An error occurred when updating the password. Please try again.')
        flash('Password successfully updated.')
        # rerender settings page
        return render_template(
            'settings.html',
            curr_user_info=curr_user_info
            )
    elif action == 'update_appearance':
        # if action is update appearance, upate darkmode settings
        appearance = request.form.get('appearance')
        # update appearance pref
        # ADD THIS CODE
        flash("Appearance updated!")
    else:
        flash("This is not yet implemented")
    return redirect(url_for('settings_page', uid=uid))

@app.route('/critter/<cid>')
def critter_page(cid):
    """
    Route to a critter's page to view it's info and stories (critter.html).
    """
    # session code 
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))
    uid = session['uid']
    print(f'looking up critter with cid {cid}')
    if not cid.isdigit():
        # if the critter cid is wrong type, flash error message
        flash('cid must be a string of digits')
        return redirect( url_for('index'))
    # get critter info
    cid = int(cid)
    conn = dbi.connect()
    critter_info = critter.get_critter_by_id(conn,cid)
    critter_info['created'] = critter_info['created'].strftime("%m/%d/%Y")[:10]
    creator_uid = int(critter_info['uid'])
    creator_info = profile.get_user_info(conn, creator_uid)
    if creator_info is None:
        # error message for user uid of Nonetype
        flash(f'No profile found with uid={creator_uid}')
        return redirect(url_for('index'))
    if critter_info is None:
        # error message for critter cid of Nonetype
        flash(f'No critter found with cid={cid}')
        return redirect(url_for('index'))
    # get story info
    stories = story.get_stories_for_critter(conn, cid, creator_uid)
    stories_by_user = [story for story in stories if story["original"] == True]
    stories_not_by_user = [story for story in stories if story["original"] == False]
    # render the critter template it's info and all of it's stories
    for s in stories:
        print(s)
    return render_template(
        'critter.html',
        user=creator_info,
        critter_info=critter_info,
        stories_by_user=stories_by_user,
        stories_not_by_user=stories_not_by_user
    )
    
@app.route('/story/<cid>/<sid>')
def story_page(cid, sid):
    """
    Route to a story's page to view it's info and with options to delete or update if the story was written by the user.
    """
    # session code 
    print(f"sid: {sid}")
    print(f"cid: {cid}")
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))
    uid = session['uid']
    print(f'looking up critter with cid {cid}')
    if not cid.isdigit():
        # if the critter cid is wrong type, flash error message
        flash('cid must be a string of digits')
        return render_template('main.html')
    # get critter info
    cid = int(cid)
    conn = dbi.connect()
    critter_info = critter.get_critter_by_id(conn,cid)
    creator_uid = int(critter_info['uid'])
    creator_info = profile.get_user_info(conn,creator_uid)
    if creator_info is None:
        # error message for user uid of Nonetype
        flash(f'No profile found with uid={creator_uid}')
        return render_template('main.html')
    if critter_info is None:
        # error message for critter cid of Nonetype
        flash(f'No critter found with cid={cid}')
        return render_template('main.html')
    
    # get story info
    if not sid.isdigit():
        # if the critter cid is wrong type, flash error message
        flash('cid must be a string of digits')
        return redirect( url_for('critter_page', cid=cid))
    sid = int(sid)
    story_info = story.get_story_by_id(conn, sid)
    if story_info == None:
        flash('Invalid link')
        return render_template('main.html')
    print(story_info)
    print(critter_info)
    return render_template('story.html', story_info=story_info, critter_info=critter_info)
    
    

@app.route('/critter_upload/', methods=['POST', 'GET'])
def critter_upload():
    """
    Renders critter-upload form and adds the results to the database.
    """
    # session code 
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))
    if request.method == 'GET':
        # method is get, user entered the page
        # send the upload form
        return render_template('critter_upload.html')
    else:
        # method is post, form has been filled out
        # get critter info from form
        conn = dbi.connect()
        uid = session['uid']
        f = request.files['critter-pic']
        user_filename = f.filename
        name = request.form.get('critter-name')
        desc = request.form.get('critter-desc')
        # ensure the user uploads an image and name
        if f and user_filename == '':
            # if the filename is none, flash error message and re-render
            flash('Please add a critter image.')
            return render_template('critter_upload.html')
        if name == '':
            # if the critter wasn't named, flash error message and re-render
            flash('Please name the critter.')
            return render_template('critter_upload.html')
        # ensure that the name and description are the correct length
        if len(name) > 50:
            # if the name is too long, flash message and re-render
            flash('Critter name must be under 50 characters')
            return render_template('critter_upload.html')
        if len(desc) > 250:
            # if the description is too long, flash message and re-render
            flash('Description must be under 250 characters')
            return render_template('critter_upload.html')
        try:
            # try to add the critter to the database
            critterID = critter.add_critter(conn, uid, app.config['uploads'], name, desc)
        except:
            # if this doesn't work, flash an error message
            flash('An error occurred when uploading the critter. Please try again')
            return render_template('critter_upload.html')
        pet = critter.get_critter_by_id(conn, critterID['last_insert_id()'])
        # add the photo to the uploads folder, using critter{cid} as the name
        cid = pet['cid']
        nm = "critter" + str(cid)
        ext = user_filename.split('.')[-1]
        filename = secure_filename(f"{nm}.{ext}")
        pathname = os.path.join(app.config['uploads'], filename)
        print(pathname)
        f.save(pathname)
        os.chmod(pathname, 0o444)
        # update the critter element in database to have the correct image path
        critter.update_critter(conn, cid, filename, name, desc)
        # forward the user to the new critter's page
        return redirect(url_for('critter_page', cid=cid))
    
@app.route('/critter/delete_citter/<cid>', methods=["GET", "POST"])
def delete_critter(cid):
    '''
    Renders a form to delete the specified critter and remove it from the database.
    Will also delete any stories that were written about that critter.
    
    :param cid: the primary key in the database of the critter to delete
    '''
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))
    uid = session['uid']
    
    try:
        cid = int(cid)
    except:
        flash('invalid url')
        user = profile.get_user_info(conn,uid)
        if user is None:
            flash(f'No profile found with uid={uid}')
            return redirect(url_for('index'))
        if user is None:
            flash(f'No profile found with uid={uid}')
            return redirect(url_for('index'))
        return redirect(url_for('user_profile',
            uid=uid))
        
    conn = dbi.connect()
    critter_info = critter.get_critter_by_id(conn,cid)
    
    if critter_info is None:
        flash(f'No critter found with cid={cid}')
        return redirect(url_for('index'))
    if request.method == 'GET':
        # Render the delete form
        return render_template('delete_critter.html',
                               critter_info=critter_info)
    else:
        action = request.form.get('action')
        if action == 'Delete':
            # if button clicked == confirm deletion:
            critters_deleted, stories_deleted = critter.delete_critter(conn, cid)
            if critters_deleted == 0:
                flash('Critter not found or already deleted.')
            else:
                flash(f'Deleted {critters_deleted} critter and {stories_deleted} related stories.')
            
            return redirect(url_for('user_profile',
                uid=uid))
            
@app.route('/story/delete_story/<sid>', methods=["GET", "POST"])   
def delete_story(sid):
    '''
    Renders a form to delete the specified story and remove it from the database.
    
    :param sid: the primary key in the database of the story to delete
    '''
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))
    uid = session['uid']
    
    try:
        sid = int(sid)
    except:
        flash('invalid url')
        user = profile.get_user_info(conn,uid)
        if user is None:
            flash(f'No profile found with uid={uid}')
            return redirect(url_for('index'))
        return redirect(url_for('user_profile',
            uid=uid))
        
    conn = dbi.connect()
    story_info = story.get_story_by_id(conn,sid)
    print("in delete story")
    
    if story_info is None:
        print("no story")
        flash(f'No story found with sid={sid}')
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        print("get delete story page")
        
        critter_info = critter.get_critter_by_id(conn, story_info['cid'])
        return render_template('delete_story.html', story_info=story_info, critter_info=critter_info)
    else:
        print("post")
        action = request.form.get('action')
        if action == 'Delete':
            print("delete")
            # if button clicked == confirm deletion:
            stories_deleted = story.delete_story(conn, sid)
            print("deleted?")
            if stories_deleted == 0:
                flash('Story not found or already deleted.')
            else:
                flash(f'Number of stories deleted: {stories_deleted}.')
            
            return redirect(url_for('user_profile',
                uid=uid))
    

@app.route('/critter/<cid>/story_upload/', methods=["GET", "POST"])
def story_upload(cid):
    """
    Renders story-upload form and adds the results to the database.
    """
    if 'uid' not in session:
        # session code 
        flash("Please Login in first!")
        return redirect(url_for('signin'))
    print(f'looking up critter with cid {cid}')
    if not cid.isdigit():
        # if the critter cid is wrong type, flash error message
        flash('cid must be a string of digits')
        return redirect( url_for('index'))
    # get critter info for form
    cid = int(cid)
    conn = dbi.connect()
    critter_info = critter.get_critter_by_id(conn, cid)
    # get user info for form
    uid = critter_info['uid']
    user = profile.get_user_info(conn,uid)
    if request.method == 'GET':
        # method is get, user entered the page
        # send the upload form
        if user is None:
            # if the user doesn't exist, flash message and redirect
            flash(f'No profile found with uid={uid}')
            return redirect(url_for('index'))
        if critter_info is None:
            # if the critter doesn't exist, flash message and redirect
            flash(f'No critter found with cid={cid}')
            return redirect(url_for('index'))
        # render the blank form
        return render_template('story_upload.html', 
                               user=user, 
                               critter_info=critter_info)
    else:
        # method is post, form has been filled out
        # add the story to the database
        conn = dbi.connect()
        # get the user's uid from session
        uid = session['uid']
        # get the story from form
        new_story = request.form.get('critter-story')
        # ensure the user uploads a story
        if new_story == '':
            # if the story is blank, flash a message and re-render form
            flash('Please write a story.')
            return render_template('story_upload.html', 
                               user=user, 
                               critter_info=critter_info)
        # check length of story to avoid error
        if len(new_story) > 2000:
            # if the story length is too long, flash a message and re-render form
            flash('The story cannot be longer than 2000 characters')
            return render_template('story_upload.html', 
                               user=user, 
                               critter_info=critter_info)
        try:
            # try to add the story to the database
            story.add_story(conn, cid, uid, new_story)
        except:
            # if this doesn't work, flash an error message
            flash('An error occurred when uploading the story. Please try again')
            return render_template('story_upload.html')
        return redirect(url_for('critter_page', cid=cid))

@app.route('/query/', methods=['GET'])
def lookup_form():
    """
    Sends the user the lookup form.
    When the user has filled out the form, display a lookup result according to their query.
    """
    # session code 
    if 'uid' not in session:
        flash("Please Login in first!")
        return redirect(url_for('signin'))
    # get the query type (either critter's name or user's username)
    query_type = request.args.get('kind')
    query = request.args.get('query')
    conn = dbi.connect()
    if query_type == 'critter':
        # if the query type is critter, get critters matching the query
        critters = critter.lookup_critter(conn, query)
        if not critters:
            # if no critters match the query, flash a message
            flash('No critters matched the query. Please try again.')
            return redirect(url_for('index'))
        for c in critters:
            # save critter's creator and created time for display as well
            c['creator'] = profile.get_user_info(conn, c['uid'])['username']
            c['created'] = c['created'].strftime("%m/%d/%Y")
        if len(critters) == 1:
            # if only one critter matches the query, redirect directly to that critter's page
            return redirect(url_for('critter_page', cid=critters[0]['cid']))
        # render a clickable list of critters
        return render_template('critter_lookup.html', query = query, critters = critters)
    if query_type == 'user':
        # if the query type is user, get users matching the query
        users = profile.lookup_user(conn, query)
        if not users:
            # if no users match the query, flash a message
            flash('No users matched the query. Please try again.')
            return redirect(url_for('index'))
        for u in users:
            # save user's account creation time and number of critters for display as well
            u['created'] = u['created'].strftime("%m/%d/%Y")
            u['num_critters'] = len(profile.get_critters_by_user(conn, u['uid']))
        if len(users) == 1:
            # if only one user matches the query, redirect directly to that user's page
            return redirect(url_for('user_profile', uid=users[0]['uid']))
        # render a clickable list of users
        return render_template('user_lookup.html', query = query, users = users)

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
