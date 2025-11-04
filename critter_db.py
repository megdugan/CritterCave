import cs304dbi as dbi
from datetime import datetime

def signup(conn, name, username, password): 
    # hash the user password
    created = datetime.now()
    profilepic = "/default.png"
    darkmode = False
    curs = dbi.dict_cursor(conn)
    # curs.execute( '''blah blah insert stuff''')

# run main to test methods
# remember to activate virtual environment: source ~/cs304/venv/bin/activate
if __name__ == '__main__':
    dbi.conf("crittercave_db")
    conn = dbi.connect() # pass as conn argument for testing methods