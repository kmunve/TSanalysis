import sqlite3

__author__ = 'kmu'

# Create SQLite3 DB
db = sqlite3.connect('./Data/stations.db')

# Get a cursor object
cursor = db.cursor()
# Init table
cursor.execute('''
    CREATE TABLE stations(id INTEGER PRIMARY KEY,
        stnr INTEGER unique,
        name TEXT,
        wmoNo INTEGER,
        fromDay INTEGER,
        fromMonth INTEGER,
        fromYear INTEGER,
        toDay INTEGER,
        toMonth INTEGER,
        toYear INTEGER,
        latLonFmt TEXT,
        latDec DOUBLE,
        lonDec DOUBLE,
        utm_e INTEGER,
        utm_n INTEGER,
        utm_zone INTEGER,
        amsl INTEGER,
        municipalityNo INTEGER,
        department TEXT)
        ''')
db.commit()


# Close DB
db.close()
