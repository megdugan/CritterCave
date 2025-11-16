""" 
(CritterCave)
Contains all database methods relating to accessing and displaying user settings
"""

import cs304dbi as dbi
from datetime import datetime
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename

import profile  # profile / user methods
import critter  # critter methods
import story    # story methods
import bcrypt

def check_password(conn, uid: int, old_pw, new_pw1, new_pw2):
    curs = dbi.cursor(conn)
    curs.execute('''select password from user where uid = %s''', [uid])
    stored = curs.fetchone()[0]

    # check whether entered password matches database using hashing
    hashed = bcrypt.hashpw(old_pw.encode('utf-8'), stored.encode('utf-8'))
    hashed_str = hashed.decode('utf-8')
    
    if hashed_str != stored:
        print('Password is incorrect.')
        # if the password is incorrect, return -1
        return -1
    
    elif new_pw1 != new_pw2:
        print('The new passwords do not match')
        return -2
    
    print('Passwords match.')
    # if the login is correct, return uid
    return 1

def update_personal_info(conn, uid: int, new_name, new_username):
    curs = dbi.dict_cursor(conn)
    curs.execute(
        '''
        UPDATE user SET
            name = %s,
            username = %s
        WHERE uid = %s
        ''',
        [new_name,new_username,uid]
    )
    conn.commit()
    flash(f'name for uid {uid} updated to {new_name}, username updated to {new_username}')
    
def update_password(conn, uid: int, new_pw):
    # hash the user password
    hashed = bcrypt.hashpw(new_pw.encode('utf-8'), bcrypt.gensalt())
    # insert new user information with default profilepic and darkmode setting
    curs = dbi.cursor(conn)
    curs.execute(
        '''
        UPDATE user SET
            password = %s
        WHERE uid = %s
        ''',
        [hashed.decode('utf-8'), uid]
    )
    conn.commit()

def update_name(conn, uid: int, new_name):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 UPDATE user 
                 SET name = %s
                 WHERE uid = %s''',
                 [new_name,uid])
    conn.commit()
    flash(f'name for uid {uid} updated to {new_name}')

def update_username(conn, uid: int, new_username):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 UPDATE user 
                 SET username = %s
                 WHERE uid = %s''',
                 [new_username,uid])
    conn.commit()
    flash(f'username for uid {uid} updated to {new_username}')

def update_darkmode(conn, uid: int, new_mode):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 UPDATE user 
                 SET darkmode = %s
                 WHERE uid = %s''',
                 [new_mode,uid])
    conn.commit()
    flash(f'darkmode for uid {uid} updated to {new_mode}')

def update_pfp(conn, uid: int, new_pfp):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 UPDATE user 
                 SET profilepic = %s
                 WHERE uid = %s''',
                 [new_pfp,uid])
    conn.commit()
    flash(f'pfp for uid {uid} updated to {new_pfp}')


