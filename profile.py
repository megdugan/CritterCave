"""
(CritterCave)
Contains all database methods relating to accessing and displaying user profiles
"""
import cs304dbi as dbi
from datetime import datetime
import bcrypt
import pymysql

import critter  # critter methods
import story    # story methods
import settings # settings methods

def get_user_info(conn, uid: int):
    """with the user's uid, returns their name and profile pic"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT *
                 FROM user
                 WHERE uid = %s''',
                 [uid])
    return curs.fetchone()



def get_critters_by_user(conn, uid: int):
    """Returns all critters made by the specified user with uid"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT cid, name, imagepath, description, created 
                 FROM critter
                 WHERE uid = %s''',
                 [uid])
    return curs.fetchall()


def get_liked_critters(conn, uid: int):
    """Returns a list of all critters the user with uid has liked"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT critter.name AS name,critter.imagepath AS image,critter.description AS desc
                 FROM liked_critter JOIN critter ON cid
                 WHERE liked_critter.uid = %s'''
                 [uid])
    return curs.fetchall()


def get_liked_stories(conn, uid: int):
    """Returns a list of all stories the user with uid has liked"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT story.story AS story
                 FROM liked_story JOIN story ON sid
                 WHERE liked_story.uid = %s'''
                 [uid])
    return curs.fetchall()


def sign_up(conn, name, username, password) -> int: 
    '''
    Inserts a new user into the database.
    Returns the new user's uid if successful.
    For duplicate username, returns -1.
    For general errors, returns -2.
    Args:
        conn -> pymysql.connections.Connection
        name -> str
        username -> str
        password -> str
    Return:
        user's uid -> int
    '''
    try:
        # hash the user password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # insert new user information with default profilepic and darkmode setting
        curs = dbi.cursor(conn)
        curs.execute('''insert into user (name, username, password, created, profilepic, darkmode) 
                        values (%s, %s, %s, %s, %s, %s)''', [name, username, hashed.decode('utf-8'), datetime.now(), '/static/default.png', False])
        conn.commit()
        # return user uid
        curs.execute('select last_insert_id()')
        row = curs.fetchone()
        return row[0]
    # exception for duplicate username error
    except pymysql.err.IntegrityError as err:
        details = err.args
        if details[0] == pymysql.constants.ER.DUP_ENTRY:
            print('duplicate key for username {}'.format(username))
            return -1
        else:
            print('error inserting user')
            return -2

def sign_in(conn, username, password) -> None: 
    '''
    Sign in a user.
    Returns the user's uid if successful.
    For incorrect password, returns -1. 
    For non-existent username, returns -2.
    Args:
        conn -> pymysql.connections.Connection
        username -> str
        password -> str
    Return:
        user's uid -> int
    '''
    try:
        # grab user stored password
        curs = dbi.cursor(conn)
        curs.execute('''select uid, password from user where username = %s''', [username])
        uid, stored = curs.fetchone()

        # check whether entered password matches database using hashing
        hashed = bcrypt.hashpw(password.encode('utf-8'), stored.encode('utf-8'))
        hashed_str = hashed.decode('utf-8')
        
        if hashed_str == stored:
            print('Login successful.')
            # if the login is correct, return uid
            return uid

        print('Password is incorrect.')
        # if the password is incorrect, return -1
        return -1
    
    except TypeError:
        print('Username does not exist.')
        # if the username does not exist, return -1
        return -2

def delete_user(conn, uid) -> None: 
    '''
    Delete a user from the database.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
    Return:
        None
    '''
    curs = dbi.cursor(conn)
    curs.execute('''delete from user where uid = %s''', uid)
    conn.commit()
    return

if __name__ == '__main__':
    dbi.conf('crittercave_db')
    conn = dbi.connect()

    # test user with username = test, uid = 7
    
    # sign_up(conn, 'test user', 'test', 'password')
    # print(get_user_info(conn, 7))

    print(f"non-existant username, expecting uid -1: {sign_in(conn, 'nobody', 'hi')}")
    print(f"incorrect password, expecting uid -1: {sign_in(conn, 'test', 'password1')}")
    print(f"valid login, expecting uid 7: {sign_in(conn, 'test', 'password')}")