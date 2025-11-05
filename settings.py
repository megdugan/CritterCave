""" 
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


