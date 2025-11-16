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

def add_critter(conn,uid,imagepath,name,desc):
    """ This method will add a new critter to the database based on 
    on the user entering the critters name and descritpion"""
    time=datetime.now()
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            insert into critter(uid,imagepath,name,description,created)
             values (%s,%s, %s,%s,%s) """,
             [uid,imagepath,name,desc,time])
    conn.commit()

    # Get the critter id (cid)
    curs.execute('select last_insert_id()')
    row = curs.fetchone()
    return row

def get_critter_by_id(conn,cid):
    """
    This method will grab critters by their critter id
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            select * from critter where cid=%s
            """,[cid])
    return curs.fetchone()

def delete_critter(conn,cid):
    """
    This method will delete critters by their critter id
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            delete from critter where cid=%s
            """,[cid])
    conn.commit()

def update_critter(conn,cid,imagepath,name,description):
    """
    This method will update critters by their critter id
    """
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            update critter set imagepath=%s,name=%s,description=%s
            where cid=%s
            """,[imagepath,name,description,cid])
    conn.commit()
    
def lookup_critter(conn, query):
    '''
    Lookup a critter by name.
    Returns a list of critters who match the query.
    If none match, return None.
    
    Args:
        conn -> pymysql.connections.Connection
        query -> string
    Return:
        list of critters -> dict[]
    '''
    name_query = f"%{query}%"
    curs=dbi.dict_cursor(conn)
    curs.execute("""
            select * from critter where name like %s
            """,[name_query])
    critters = curs.fetchall()
    if not critters:
        return None
    return critters

# To test methods
# Remember to activate virtual environment: source ~/cs304/venv/bin/activate
if __name__ == '__main__':
    dbi.conf("crittercave_db")
    conn = dbi.connect() # pass as conn argument for testing methods
    # critter=add_critter(conn,1,"path","Tommy","Tommy is a very bald critter")
    # print(critter)
    # critter=add_critter(conn,1,"path","Wow","Sam")
    # print(critter)
    #critter_id=get_critter_by_id(conn,2)
    #print(critter_id)
    #delete_critter(conn,4)
    # update_critter(conn,3,imagepath="path",description="Wow",name="Sam")