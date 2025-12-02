""" 
(CritterCave)
Contains all database methods relating to accessing and displaying critters
"""

import cs304dbi as dbi
from datetime import datetime
import bcrypt

import profile  # profile / user methods
import story    # story methods
import settings # settings methods

def add_critter(conn, uid, imagepath, name, description):
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

def get_critter_by_id(conn, cid):
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

def delete_critter(conn,cid):
    """
    Delete a critter from the database.
    Args:
        conn -> pymysql.connections.Connection
        cid -> int
    Return:
        None
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            delete from critter where cid=%s
            """,[cid])
    conn.commit()

def update_critter(conn,cid,imagepath,name,description):
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
            [imagepath,name,description,cid])
    conn.commit()
    
def lookup_critter(conn, query):
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