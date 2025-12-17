"""
(CritterCave)
Contains all database methods relating to accessing and displaying user profiles.
"""

from datetime import datetime
import bcrypt
import pymysql
import cs304dbi as dbi
import critter
import story
import settings

def get_user_info(conn, uid: int):
    """
    Returns info about a given user.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
    Return:
        user's info -> dict[]
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT uid, name, username, created, profilepic
                 FROM user
                 WHERE uid = %s''',
                 [uid])
    return curs.fetchone()


def get_critters_by_user(conn, uid: int):
    """
    Returns all critters made by the specified user with uid.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
    Return:
        user's critters -> dict[]
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT cid, name, imagepath, description, created 
                 FROM critter
                 WHERE uid = %s''',
                 [uid])
    return curs.fetchall()


def get_liked_critters(conn, uid: int):
    """
    Returns a list of all critters the user with uid has liked.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
    Return:
        liked critters -> dict[]
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT DISTINCT critter.cid AS cid, critter.name AS name, critter.imagepath AS imagepath, critter.description AS description, critter.created AS created
                 FROM liked_critter JOIN critter USING (cid)
                 WHERE liked_critter.uid = %s''',
                 [uid])
    return curs.fetchall()


def get_liked_stories(conn, uid: int):
    """
    Returns a list of all stories the user with uid has liked.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
    Return:
        liked stories -> dict[]
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
                 SELECT DISTINCT story.sid, story.uid, story.cid, story.story, 
                 user.username,
                 critter.name
                 FROM liked_story 
                 JOIN story on liked_story.sid = story.sid
                 JOIN user on story.uid=user.uid
                 JOIN critter on story.cid=critter.cid
                 WHERE liked_story.uid = %s''',
                 [uid])
    return curs.fetchall()


def sign_up(conn, name: str, username: str, password: str) -> int: 
    """
    Inserts a new user into the database, returning their uid if successful.
    For duplicate username, returns -1.
    For general errors, returns -2.
    Args:
        conn -> pymysql.connections.Connection
        name -> str
        username -> str
        password -> str
    Return:
        user's uid -> int
    """
    try:
        # Hash the user password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert new user information with default profilepic and darkmode setting
        curs = dbi.cursor(conn)
        curs.execute('''insert into user (name, username, password, created, profilepic, darkmode) 
                        values (%s, %s, %s, %s, %s, %s)''', [name, username, hashed.decode('utf-8'), datetime.now(), 'default.jpg', False])
        conn.commit()

        # Return user uid
        curs.execute('select last_insert_id()')
        row = curs.fetchone()
        return row[0]
    except pymysql.err.IntegrityError as err:
        # Exception for duplicate username error
        details = err.args
        if details[0] == pymysql.constants.ER.DUP_ENTRY:
            print('duplicate key for username {}'.format(username))
            return -1
        else:
            print('error inserting user')
            return -2


def sign_in(conn, username: str, password: str) -> None: 
    """
    Sign in a user, returning the user's uid if successful.
    For incorrect password, returns -1. 
    For non-existent username, returns -2.
    Args:
        conn -> pymysql.connections.Connection
        username -> str
        password -> str
    Return:
        user's uid -> int
    """
    try:
        # Grab user stored password
        curs = dbi.cursor(conn)
        curs.execute('''select uid, password from user where username = %s''', [username])
        uid, stored = curs.fetchone()

        # Check whether entered password matches database using hashing
        hashed = bcrypt.hashpw(password.encode('utf-8'), stored.encode('utf-8'))
        print(f"encrypted: {hashed}")
        hashed_str = hashed.decode('utf-8')
        print(f"descrypted: {hashed_str}")

        if hashed_str == stored:
            # If the login is correct, return uid
            print('Login successful.')
            return uid
        # Else, if the password is incorrect, return -1
        print('Password is incorrect.')
        return -1
    except TypeError:
        # If the username does not exist is incorrect, return -2
        print('Username does not exist.')
        return -2


def delete_user(conn, uid: int) -> None: 
    """
    Delete a user from the database.
    Args:
        conn -> pymysql.connections.Connection
        uid -> int
    Return:
        None
    """
    try:
        curs = dbi.cursor(conn)
        curs.execute('''delete from user where uid = %s''', uid)
        conn.commit()
    except Exception as err:
        conn.rollback()
    return
    

def lookup_user(conn, query: str):
    """
    Lookup a critter by name, returning all critters who match the query.
    If none match, return None.
    Args:
        conn -> pymysql.connections.Connection
        query -> str
    Return:
        list of users -> dict[]
    """
    name_query = f"%{query}%"
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            select uid, name, username, created, profilepic
            from user where username like %s
            """,[name_query])
    users = curs.fetchall()
    if not users:
        return None
    return users


def get_likes_data_critter(conn,cid):
    """
    Lookup a critter rating by, counting how many times that critter is liked in the table.
    Args:
        conn -> pymysql.connections.Connection
        query -> str
    Return:
        num of critters -> dict[]
    """

    curs = dbi.cursor(conn)
    curs.execute('''
                    select count(*) from liked_critter where cid=%s
                ''',[cid])
    total_likes=curs.fetchone()[0]
    return total_likes


def update_like(conn,cid,uid):
    try:
        curs = dbi.cursor(conn)
        curs.execute(
                '''
                INSERT INTO liked_critter (cid, uid)
                VALUES (%s, %s)
                ''',
                [cid, uid]
            )
        conn.commit()
    except Exception as err:
        conn.rollback()
    return