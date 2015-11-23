#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sqlite3
__author__ = 'kmu'

"""
TODO: add relation between plateau-stations and top-stations
"""

class CrocusStationDB:

    def __init__(self, db_location):
        # Create/open SQLite3 DB
        self.db = sqlite3.connect(db_location)
        # Get a cursor object
        self.cursor = self.db.cursor()

    def close(self):
        # Close DB
        self.db.close()
        print("DB closed")

    def create_station_db(self):
        # Init table
        self.cursor.execute('''
            CREATE TABLE stations(id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        self.db.commit()

    def insert_station(self, station):
        '''

        :param station: dictionary containing the station properties
        :return: void
        '''
        self.cursor.execute('''INSERT INTO stations(amsl,
                            department,
                            fromDay,
                            fromMonth,
                            fromYear,
                            latDec,
                            latLonFmt,
                            lonDec,
                            municipalityNo,
                            name,
                            stnr,
                            toDay,
                            toMonth,
                            toYear,
                            utm_e,
                            utm_n,
                            utm_zone,
                            wmoNo)
                      VALUES(:amsl,
                            :department,
                            :fromDay,
                            :fromMonth,
                            :fromYear,
                            :latDec,
                            :latLonFmt,
                            :lonDec,
                            :municipalityNo,
                            :name,
                            :stnr,
                            :toDay,
                            :toMonth,
                            :toYear,
                            :utm_e,
                            :utm_n,
                            :utm_zone,
                            :wmoNo)''', station)
        self.db.commit()



