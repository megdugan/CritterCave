# CritterCave
# Contains all database methods. (The functions that do most of the work.)

import cs304dbi as dbi

def add_story(conn, cid: int, uid: int, story: str):
    curs = dbi.dict_cursor(conn)
    created = 
    curs.execute('''
        select name,birthdate from person 
        where month(birthdate) = %s''',[month])
    return