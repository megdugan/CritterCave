""" 
Contains all methods that will be used to access the database and 
get information that will be needed for forms and info shown in settings
"""
import cs304dbi as dbi
from datetime import datetime
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename

def update_name(conn, uid: int, new_name):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 UPDATE user 
                 SET name = %s
                 WHERE uid = %s''',
                 [new_name,uid])
    conn.commit()
    flash(f'name for uid {uid} updated to {new_name}')
    return

def update_username(conn, uid: int, new_username):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 UPDATE user 
                 SET username = %s
                 WHERE uid = %s''',
                 [new_username,uid])
    conn.commit()
    flash(f'name for uid {uid} updated to {new_name}')
    return

def update_darkmode(conn, uid: int, new_mode):
    return

def update_pfp(conn, uid: int, new_pfp):
    return



