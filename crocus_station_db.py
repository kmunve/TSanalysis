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
        try:
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
        except Exception as e:
            # Roll back any change if something goes wrong
            self.db.rollback()
            raise e
        finally:
            # Close the db connection
            self.db.close()

    def insert_station(self, station):
        """

        :param station: dictionary containing the station properties
        :return: void
        """
        try:
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
        except sqlite3.IntegrityError as err:
            # Roll back any change if something goes wrong
            self.db.rollback()
            print("WARNING:", err, "- ignoring station", station['stnr'])

    def get_all_stations(self):
        """

        :return:
        """
        try:
            self.cursor.execute('''SELECT id, stnr, name, latDec, lonDec, utm_e, utm_n, amsl FROM stations''')
            all_rows = self.cursor.fetchall()
        except Exception as e:
            raise e

        return all_rows



