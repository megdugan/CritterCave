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

import bcrypt
import cs304dbi as dbi

def check_password(conn, uid: int, old_pw, new_pw1, new_pw2):
    curs = dbi.cursor(conn)
    curs.execute('SELECT password FROM user WHERE uid = %s', [uid])
    
    row = curs.fetchone()
    stored_pw = row[0]   # extract string from tuple

    # bcrypt check
    if not bcrypt.checkpw(old_pw.encode('utf-8'), stored_pw.encode('utf-8')):
        print("Password is incorrect.")
        return -1

    # check new passwords match
    if new_pw1 != new_pw2:
        print("New passwords do not match.")
        return -2

    print("Passwords match.")
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
        WHERE uid = %s
        ''', [new_pfp, uid])
    conn.commit()
    flash(f'pfp for uid {uid} updated to {new_pfp}')


