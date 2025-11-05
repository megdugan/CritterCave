# CritterCave
# Contains all database methods. (The functions that do most of the work.)

import cs304dbi as dbi
from datetime import datetime

def signup(conn, name, username, password): 
    # hash the user password
    created = datetime.now()
    profilepic = "/default.png"
    darkmode = False
    curs = dbi.dict_cursor(conn)
    # curs.execute( '''blah blah insert stuff''')

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