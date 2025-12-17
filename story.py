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
    try:
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
    except Exception as err:
        conn.rollback()
    return


def get_story_by_id(conn, sid:int):
    """
    Get a story by its sid.
    Args:
        conn -> pymysql.connections.Connection
        sid -> int
    Return:
        story info -> dict
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
        select sid, cid, uid, created, story
        from story where sid=%s""", 
        [sid])
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
    try:
        curs=dbi.dict_cursor(conn)

        curs.execute("""
                delete from liked_story where sid=%s""",[sid])

        curs.execute("""
                delete from story where sid=%s""",[sid])
        
        conn.commit()
        print("successfully deleted story")
        return curs.rowcount
    except Exception as err:
        print(err)
        print("failed to delete story")
        conn.rollback()
    return


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
    try:
        curs=dbi.dict_cursor(conn)
        curs.execute("""
                update story set story=%s
                where sid=%s
                """,[story, sid])
        conn.commit()
    except Exception as err:
        conn.rollback()
    return


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
                 SELECT sid, user.uid as uid, user.username, story.created AS time_created, story.story AS critter_story
                 FROM story
                 join critter on story.cid=critter.cid
                 join user on story.uid=user.uid 
                 WHERE critter.cid = %s''',
                 [cid])
    stories = curs.fetchall()
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
                 SELECT sid, story.cid, story.created AS time_created, story.story,
                 critter.cid,critter.uid,critter.imagepath,critter.name,critter.description,critter.created AS critter_story
                 FROM story
                 join critter on critter.cid=story.cid
                 WHERE story.uid = %s''',
                 [uid])
    stories = curs.fetchall()
    return stories