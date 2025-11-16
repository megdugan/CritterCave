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

    # Get the story id (sid)
    curs.execute('select last_insert_id()')
    row = curs.fetchone()
    return row

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
    
    
def get_stories_for_critter(conn, cid: int):
    """Returns all stories written about the specified critter with cid"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT story.created AS time_created,story.story AS critter_story 
                 FROM story
                 WHERE cid = %s''',
                 [cid])
    return curs.fetchall()

def get_stories_for_critter_by_user(conn, cid: int, uid: int):
    """Returns all stories writen about the specified critter with cid written by the specified user with uid"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT story.created AS time_created,story.story AS critter_story 
                 FROM story
                 WHERE cid = %s AND uid = %s''',
                 [cid,uid])
    return curs.fetchall()

def get_stories_for_critter_not_by_user(conn, cid: int, uid: int):
    """Returns all stories writen about the specified critter with cid NOT written by the specified user with uid"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT story.created AS time_created,story.story AS critter_story 
                 FROM story
                 WHERE cid = %s AND uid <> %s''',
                 [cid,uid])
    return curs.fetchall()

# To test methods
if __name__ == '__main__':
    dbi.conf("crittercave_db")
    conn = dbi.connect() # pass as conn argument for testing methods
    story=add_story(conn,1,1,"Tommy was playing with scissors...")
    print(story)