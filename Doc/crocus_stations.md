

# Station list

## Crocus modeled snow-profiles available on [xgeo.no](http://www.xgeo.no/?p=snoskred)

**TODO**

- Update station list on xgeo.no
- revise naming on ftp.met.no
- agree on Crocus version and OPTIONS.nam settings

Check options:

    &NAM_PGD_GRID          CGRID = 'LONLATVAL'
    
    &NAM_PREP_ISBA_SNOW    CSNOW = 'CRO',
                           NSNOW_LAYER = 50,
                           LSNOW_FRAC_TOT = T
    &NAM_IO_OFFLINE        LPRINT  = T                       ,
                           CFORCING_FILETYPE =    'NETCDF'   ,
                           CSURF_FILETYPE =       'ASCII '   ,
                           CTIMESERIES_FILETYPE = 'NETCDF'   ,
                           LRESTART = T                      ,
                           XTSTEP_OUTPUT = 21600.            ,
                           XTSTEP_SURF = 900.
                           
    &NAM_CROCUSn
                          LSNOWDRIFT= T,
                          LSNOWDRIFT_SUBLIM= F,
                          CSNOWMETAMO = 'C13'


## Utilities

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



# TODO

Compare upgraded stations to Crocus_station list. - see *crocus_stations.json*