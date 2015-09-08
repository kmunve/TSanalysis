#!/bin/bash


# Orgiginal command from MET workshop
#fimex --input.file=http://thredds.met.no/thredds/dodsC/arome25/arome_norway_default2_5km_20140123_06.nc --input.type=netcdf --extract.selectVariables=x_wind_10m --extract.selectVariables=y_wind_10m --extract.reduceTime.start=2014-01-23T10:00:00 --extract.reduceTime.end=2014-01-23T12:00:00 --extract.reduceToBoundingBox.south=59 --extract.reduceToBoundingBox.north=61 --extract.reduceToBoundingBox.east=11 --extract.reduceToBoundingBox.west=9 --output.file=out.nc --output.type=nc4

# Extract bounding box around Rauland forecasting region
fimex --input.file=./Data/arome_metcoop_default2_5km_latest.nc --input.type=netcdf \
--extract.selectVariables=precipitation_amount \
--extract.selectVariables=precipitation_amount_acc \
--extract.selectVariables=precipitation_amount_high_estimate \
--extract.selectVariables=precipitation_amount_low_estimate \
--extract.selectVariables=precipitation_amount_middle_estimate \
--extract.selectVariables=air_temperature_2m \
--extract.selectVariables=land_area_fraction \
--extract.selectVariables=altitude \
--extract.reduceTime.start=2015-09-04T07:00:00 --extract.reduceTime.end=2015-09-05T06:00:00 \
--extract.reduceToBoundingBox.south=59.55 --extract.reduceToBoundingBox.north=60.02 \
--extract.reduceToBoundingBox.west=7.47 --extract.reduceToBoundingBox.east=9.02 \
--output.file=Data/rauland.nc --output.type=nc4


# Extract bounding box around Lofoten forecasting region
fimex --input.file=./Data/arome_metcoop_default2_5km_latest.nc --input.type=netcdf \
--extract.selectVariables=precipitation_amount \
--extract.selectVariables=precipitation_amount_acc \
--extract.selectVariables=precipitation_amount_high_estimate \
--extract.selectVariables=precipitation_amount_low_estimate \
--extract.selectVariables=precipitation_amount_middle_estimate \
--extract.selectVariables=air_temperature_2m \
--extract.selectVariables=land_area_fraction \
--extract.selectVariables=altitude \
--extract.reduceTime.start=2015-09-04T07:00:00 --extract.reduceTime.end=2015-09-05T06:00:00 \
--extract.reduceToBoundingBox.south=67.82 --extract.reduceToBoundingBox.north=68.48 \
--extract.reduceToBoundingBox.west=12.70 --extract.reduceToBoundingBox.east=15.57 \
--output.file=Data/lofoten.nc --output.type=nc4
