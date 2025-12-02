""" 
(CritterCave)
Contains all database methods relating to accessing and displaying user settings.
"""

from datetime import datetime
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
import bcrypt
import cs304dbi as dbi
import profile
import critter
import story

def check_password(conn, uid: int, old_password: str, new_password1: str, new_password2: str):
    """
    Check password for new password setting.
    Also check that the new password matches.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
        old_password -> str
        new_password1 -> str
        new_password2 -> str
    Return:
        success -> int
    """
    curs = dbi.cursor(conn)
    curs.execute('SELECT password FROM user WHERE uid = %s', [uid])
    row = curs.fetchone()
    # extract string from tuple
    stored_password = row[0]
    # bcrypt check
    if not bcrypt.checkpw(old_password.encode('utf-8'), stored_password.encode('utf-8')):
        print("Password is incorrect.")
        return -1
    # check new passwords match
    if new_password1 != new_password2:
        print("New passwords do not match.")
        return -2
    print("Passwords match.")
    return 1

def update_personal_info(conn, uid: int, new_name:str, new_username:str):
    """
    Update the personal info of a user.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
        new_name -> str
        new_username -> str
    Return:
        None
    """
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

def update_password(conn, uid: int, new_password: str):
    """
    Update a user's password.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
        new_password -> str
    Return:
        None
    """
    # hash the user password
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
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

def update_name(conn, uid: int, new_name: str):
    """
    Update a user's name.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
        new_name -> str
    Return:
        None
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 UPDATE user 
                 SET name = %s
                 WHERE uid = %s''',
                 [new_name,uid])
    conn.commit()
    flash(f'name for uid {uid} updated to {new_name}')

def update_username(conn, uid: int, new_username: str):
    """
    Update a user's username.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
        new_username -> str
    Return:
        None
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 UPDATE user 
                 SET username = %s
                 WHERE uid = %s''',
                 [new_username,uid])
    conn.commit()
    flash(f'username for uid {uid} updated to {new_username}')

def update_darkmode(conn, uid: int, new_mode):
    """
    Update a user's darkmode setting.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
        new_mode -> boolean or tinyint (1/true, 0/false) (?)
    Return:
        None
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 UPDATE user 
                 SET darkmode = %s
                 WHERE uid = %s''',
                 [new_mode, uid])
    conn.commit()
    flash(f'darkmode for uid {uid} updated to {new_mode}')

def update_pfp(conn, uid: int, new_pfp: str):
    """
    Update a user's profile photo.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
        new_pfp -> str
    Return:
        None
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        UPDATE user 
        SET profilepic = %s
        WHERE uid = %s
        ''', [new_pfp, uid])
    conn.commit()
    flash(f'pfp for uid {uid} updated to {new_pfp}')