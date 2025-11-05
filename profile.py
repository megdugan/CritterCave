""" 
Contains all methods that will be used to access the database and 
get information that will be displayed on the user's profile
"""

import cs304dbi as dbi
from datetime import datetime

def get_user_info(conn, uid: int):
    """with the user's uid, returns their name and profile pic"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT name,profilepic
                 FROM user
                 WHERE uid = %s''',
                 [uid])
    return curs.fetchone()


def get_stories_for_critter(conn, cid: int):
    """Returns all stories written about the specified critter with cid"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT story.created AS time_created,story.story AS critter_story 
                 FROM story
                 WHERE cid = %s''',
                 [cid])
    return curs.fetchall()


def get_critters_by_user(conn, uid: int):
    """Returns all critters made by the specified user with uid"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT name,imagepath,description,created 
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