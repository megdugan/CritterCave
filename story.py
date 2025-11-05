""" 
Contains all database methods relating to accessing and displaying stories
"""

import cs304dbi as dbi
from datetime import datetime

import profile  # profile / user methods
import critter  # critter methods
import settings # settings methods

def add_story(conn, cid: int, uid: int, story: str):
    curs = dbi.dict_cursor(conn)
    # created = 
    # curs.execute('''
    #     select name,birthdate from person 
    #     where month(birthdate) = %s''',[month])
    return