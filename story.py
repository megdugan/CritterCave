""" 
(CritterCave)
Contains all database methods relating to accessing and displaying stories
"""

import cs304dbi as dbi
from datetime import datetime

import profile  # profile / user methods
import critter  # critter methods
import settings # settings methods

def add_story(conn, cid:int, uid:int, story:str):
    """
    This method will add a new story to the database based on 
    on the user entering the story on a post.
    """
    time=datetime.now()
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        insert into story(cid, uid, created, story)
        values (%s,%s,%s,%s)''', [cid, uid, time, story])
    conn.commit()
    
    # Does anything need to be done to update the critter page
    # that the story is displayed on?

def get_story_by_id(conn, sid:int):
    """
    This method will grab a story by its sid (story id)
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
        select * from story where sid=%s""", [sid])
    return curs.fetchone()

def delete_story(conn,sid:int):
    """
    This method will delete a story by its sid (story id)
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            delete from story where sid=%s""",[sid])
    conn.commit()

def update_story(conn, sid:int, story:str):
    """
    This method will update a story by its sid (story id)
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            update story set story=%s
            where sid=%s
            """,[story, sid])
    conn.commit()