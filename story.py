""" 
(CritterCave)
Contains all database methods relating to accessing and displaying stories.
"""

from datetime import datetime
import cs304dbi as dbi
import profile
import critter
import settings

def add_story(conn, cid:int, uid:int, story:str):
    """
    Add a new story for a critter.
    Args:
        conn -> pymysql.connections.Connection
        cid -> int
        uid -> int
        story -> str
    Return:
        story id -> int
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
    Get a story by it's sid.
    Args:
        conn -> pymysql.connections.Connection
        sid -> int
    Return:
        story info -> dict
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
        select * from story where sid=%s""", [sid])
    story = curs.fetchone()
    story["creator_info"] = profile.get_user_info(conn, story["uid"])
    return story

def delete_story(conn, sid:int):
    """
    Delete a story.
    Args:
        conn -> pymysql.connections.Connection
        sid -> int
    Return:
        None
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            delete from story where sid=%s""",[sid])
    conn.commit()
    return curs.rowcount

def update_story(conn, sid:int, story:str):
    """
    Update a story.
    Args:
        conn -> pymysql.connections.Connection
        sid -> int
        story -> str
    Return:
        None
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            update story set story=%s
            where sid=%s
            """,[story, sid])
    conn.commit()

def get_stories_for_critter(conn, cid: int, uid: int):
    """
    Get all of the stories for a critter.
    Stories made by creator have "original": True
    Args:
        conn -> pymysql.connections.Connection
        cid -> int
        uid -> int (uid of critter's creator)
    Return:
        critter stories -> dict[]
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT sid, uid, story.created AS time_created, story.story AS critter_story
                 FROM story
                 WHERE cid = %s''',
                 [cid])
    stories = curs.fetchall()
    for story in stories:
        story["original"] = story["uid"] == uid
        story["creator_info"] = profile.get_user_info(conn, story["uid"])
    return stories

def get_stories_by_user(conn, uid: int):
    """
    Get all of the stories made by a specific user.
    Args:
        conn -> pymysql.connections.Connection
        cid -> int
        uid -> int (uid of critter's creator)
    Return:
        critter stories -> dict[]
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT sid, cid, story.created AS time_created, story.story AS critter_story
                 FROM story
                 WHERE uid = %s''',
                 [uid])
    stories = curs.fetchall()
    for story in stories:
        story["critter_info"] = critter.get_critter_by_id(conn, story["cid"])
    print(stories)
    return stories