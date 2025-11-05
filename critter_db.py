# CritterCave
# Contains all database methods. (The functions that do most of the work.)

import cs304dbi as dbi
from datetime import datetime
import bcrypt

def signup(conn, name, username, password): 
    '''
    Inserts a user into the database.
    Args:
        conn -> pymysql.connections.Connection
        name -> str
        username -> str
        password -> str
    Return:
        list of movies -> dict[]
    '''
    # hash the user password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # insert new user information with default profilepic and darkmode setting
    curs = dbi.cursor(conn)
    curs.execute('''insert into user (name, username, password, created, profilepic, darkmode) 
                    values (%s, %s, %s, %s, %s, %s, %b)''', [name, username, hashed.decode('utf-8'), datetime.now(), '/static/default.png', False])
    conn.commit()
    # return user uid
    curs.execute('select last_insert_id()')
    row = curs.fetchone()
    return row[0]

def add_story(conn, cid: int, uid: int, story: str):
    curs = dbi.dict_cursor(conn)
    # created = 
    # curs.execute('''
    #     select name,birthdate from person 
    #     where month(birthdate) = %s''',[month])
    return

# To test methods
# Remember to activate virtual environment: source ~/cs304/venv/bin/activate
if __name__ == '__main__':
    dbi.conf("crittercave_db")
    conn = dbi.connect() # pass as conn argument for testing methods