""" 
Contains all database methods relating to accessing and displaying critters
"""
import cs304dbi as dbi
from datetime import datetime

import profile  # profile / user methods
import story    # story methods
import settings # settings methods

# To test methods
# Remember to activate virtual environment: source ~/cs304/venv/bin/activate
if __name__ == '__main__':
    dbi.conf("crittercave_db")
    conn = dbi.connect() # pass as conn argument for testing methods