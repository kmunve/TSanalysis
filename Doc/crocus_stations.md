

# Station list

The following tools are used to work with [eklima](www.eklima.no) stations.

### eklima_stations.json
*eklima_stations.json* in folder *Test* contains a list of station-ids of the stations used for different purposes.

*crocus_stations* is a list over stations where Crocus model results are available at [xgeo.no](www.xgeo.no).

*third_party_stations* is a list over stations from available stations from neither MET, NVE, SVV or JBV.

### stations.db 
*stations.db* is a SQLite database where the properties of each Crocus station are stored.
The table *stations* has the following fields:

- id INTEGER PRIMARY KEY AUTOINCREMENT,
- stnr INTEGER unique,
- name TEXT,
- wmoNo INTEGER,
- fromDay INTEGER,
- fromMonth INTEGER,
- fromYear INTEGER,
- toDay INTEGER,
- toMonth INTEGER,
- toYear INTEGER,
- latLonFmt TEXT,
- latDec DOUBLE,
- lonDec DOUBLE,
- utm_e INTEGER,
- utm_n INTEGER,
- utm_zone INTEGER,
- amsl INTEGER,
- municipalityNo INTEGER,
- department TEXT

### crocus_station_db.py 
The database is initiated and maintained within **crocus_station_db.py**, which defines the **CrocusStationDB** class.

### station_lists.py

*crocus_station_list()*  reads the station-ids in *crocus_stations.json* and retreives the station properties by a 
*wsklima* request. The returned dictionary can be inserted to *stations.db* with *CrocusStationDB.insert_station()*.
