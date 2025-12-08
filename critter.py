""" 
(CritterCave)
Contains all database methods relating to accessing and displaying critters.
"""

from datetime import datetime
import bcrypt
import cs304dbi as dbi
import profile
import story
import settings

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
            select * from critter where cid=%s""", 
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
            select * from critter where name like %s
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
            '''delete from story where cid=%s''',
            [cid])
        stories_deleted = curs.rowcount
        curs.execute("""
                delete from critter where cid=%s
                """,[cid])
        critters_deleted = curs.rowcount
        conn.commit()
        return critters_deleted, stories_deleted
    except Exception as e:
        conn.rollback()
        return

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
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            update critter set imagepath=%s,name=%s,description=%s
            where cid=%s""",
            [imagepath, name, description, cid])
    conn.commit()