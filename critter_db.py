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

    #Then we get the gritter id for url redirection 
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
    


# To test methods
# Remember to activate virtual environment: source ~/cs304/venv/bin/activate
if __name__ == '__main__':
    dbi.conf("crittercave_db")
    conn = dbi.connect() # pass as conn argument for testing methods
    #critter=add_critter(conn,1,"path","Tommy","Tommy is a very bald critter")
    #print(critter)
    #critter_id=get_critter_by_id(conn,2)
    #print(critter_id)
    #delete_critter(conn,4)
    update_critter(conn,3,imagepath="path",description="Wow",name="Sam")