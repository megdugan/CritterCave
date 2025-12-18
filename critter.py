""" 
(CritterCave)
Contains all database methods relating to accessing and displaying critters.
"""

from datetime import datetime
import cs304dbi as dbi

def add_critter(conn, uid: int, imagepath: str, name: str, description: str):
    """
    Add a new critter to the database.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
        imagepath -> str
        name -> str
        description -> str
    Return:
        critter cid -> int
    """
    try:
        time=datetime.now()
        curs=dbi.dict_cursor(conn)
        curs.execute("""
                insert into critter(uid,imagepath,name,description,created)
                values (%s,%s, %s,%s,%s) """,
                [uid, imagepath, name, description, time])
        conn.commit()
        # Get the critter id (cid)
        curs.execute('select last_insert_id()')
        row = curs.fetchone()
        return row
    except Exception as err:
        conn.rollback()
        return


def get_critter_by_id(conn, cid: int):
    """
    Get information about a critter.
    Args:
        conn -> pymysql.connections.Connection
        cid -> int
    Return:
        critter info -> dict
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            select cid, uid, imagepath, name, description, created
            from critter where cid=%s""", 
            [cid])
    return curs.fetchone()


def lookup_critter(conn, query:str):
    """
    Lookup a critter by name.
    If none match, return None.
    Args:
        conn -> pymysql.connections.Connection
        query -> string
    Return:
        list of critters -> dict[]
    """
    name_query = f"%{query}%"
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            SELECT critter.cid, critter.uid, critter.imagepath, critter.name, critter.description, critter.created,
            user.username,
            COUNT(liked_critter.cid) AS like_count
            FROM critter
            LEFT JOIN user ON critter.uid = user.uid
            LEFT JOIN liked_critter ON critter.cid = liked_critter.cid
            WHERE critter.name LIKE %s
            GROUP BY critter.cid, critter.uid, critter.imagepath, critter.name, critter.description, critter.created, user.username;
                """,[name_query])
    critters = curs.fetchall()
    if not critters:
        return None
    return critters


def get_all_critters(conn):
    """
    Get all critters' information.
    Args:
        conn -> pymysql.connections.Connection
    Return:
        critter info -> list(dict)
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
        select user.uid as uid, username, cid, imagepath, critter.name as name, 
            description, critter.created as created
        from critter inner join user on critter.uid = user.uid
        order by created desc""")
    return curs.fetchall()


def delete_critter(conn, cid: int):
    """
    Delete a critter from the database.
    Args:
        conn -> pymysql.connections.Connection
        cid -> int
    Return:
        None
    """
    curs=dbi.dict_cursor(conn)
    try:
        curs.execute('start transaction;')
        curs.execute(
            '''delete from liked_story
            where sid in (
            select sid from story
            where cid = %s)''',
            [cid])
        curs.execute(
            '''delete from liked_critter where cid=%s''',
            [cid])
        curs.execute(
            '''delete from story where cid=%s''',
            [cid])
        stories_deleted = curs.rowcount
        curs.execute("""
                delete from critter where cid=%s
                """,[cid])
        critters_deleted = curs.rowcount
        conn.commit()
        print("in try; commit completed")
        return critters_deleted, stories_deleted
    except Exception as e:
        print("in except")
        print(e)
        conn.rollback()
        return 0,0
    

def update_critter(conn, cid: int, imagepath: str, name: str, description:str):
    """
    Update a critter's info.
    Args:
        conn -> pymysql.connections.Connection
        cid -> int
        imagepath -> str
        name -> str
        description -> str
    Return:
        None
    """
    try:
        curs=dbi.dict_cursor(conn)
        curs.execute("""
                update critter set imagepath=%s,name=%s,description=%s
                where cid=%s""",
                [imagepath, name, description, cid])
        conn.commit()
        return True
    except Exception as err:
        conn.rollback()
        return False

def get_likes_data_stories(conn,sid):
    """
    Lookup a critter rating by, counting how many times that critter's stories are liked in the table.
    Args:
        conn -> pymysql.connections.Connection
        query -> str
    Return:
        num of critters -> dict[]
    """

    curs = dbi.cursor(conn)
    curs.execute('''
                    select count(*) from liked_story where sid=%s
                ''',[sid])
    total_likes=curs.fetchone()[0]
    return total_likes


def update_story_likes(conn,sid,uid):
    """
    Update story likes by inserting a new like into the liked_story table.
    Args:
        conn -> pymysql.connections.Connection
        sid -> int
        uid -> int
    Return:
        None"""
    try:
        curs = dbi.cursor(conn)
        curs.execute(
                '''
                insert into liked_story (sid,uid)
                values (%s,%s)
                ''',[sid,uid])
        conn.commit()
    except Exception as err:
        curs.rollback()
    return