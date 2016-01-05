#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

'''
Datakilde parameter for htsre (HYDRA TIME SERIES ID)

Hydra Time Serie Reader mot E-Klima WCF


Parameter Påkrevd/Valgfri Kommentar

ds=htsre  P  Datametode.
id=<tidsserieid>  P  E-klima tidsserie id.
rt=<tidsoppløsning>  V  Tidsoppløsning.
mth=<metode>  V  Metode.
time=<timeformat>  V  Periodeangivelse.
chdl=<legend tekst>  V  Legend tekst.
cht=<plottetype>  V  Type plott (linje, scatter, etc).
timeo=<timeoffset>  V  Tidsforskyvning på startidspunktet.
axis=<aksegruppe>  V  Gruppering av akser
lnst=<linjestil>  V  Hvordan linje vises
drwd=<bredde på grafserie>  V  Hvor bredt en grafserie er tegnet
clr=<farge på grafserie>  V  Farge grafserie tegnes med


 Eksempel:
chd=ds=htsre,id=18700


id (E-KLIMA ID)

Angir en e-klima serie id.

Skal angis som to tall med punktum som skilletegn. Det første er id, det andre er parameter.

Eksempel: id=18700.17



__author__ = 'kmu'
'''

"http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=20151214T0000;20160113T0000&chs=976x909&lang=no&chlf=desc&chsl=0;+0&chd=ds=htsre,da=29,id=18980.0,rt=1:00,cht=col,mth=sum|ds=htsry,id=metx[18980;0].6001,mth=sum,rt=1:00,cht=col&nocache=0.9692453653216349"

"http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=20160101T0000;20160113T0000&chs=800x400&lang=no&chlf=short&chsl=20160102T000;20160103T00+0&chd=ds=htsre,da=29,id=18980.0,rt=1:00,cht=col,mth=sum|ds=htsry,id=metx[18980;0].6001,mth=sum,rt=1:00,cht=col&nocache=0.9692453653216349"


"""
Liste: 99880,99841,99840,99820,99800,99790,99780,99765,99760,


SA: 99840,99790,99760
RR_1: 99790,99820
RR_24: 99840,99820,99790,99760

<name xsi:type="xsd:string">SVEAGRUVA</name>
<stnr xsi:type="xsd:int">99760</stnr>

Vind:
http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99760.16,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=99760.14,rt=1:00,cht=line,mth=inst
TA/RR:
http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99760.17,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=99760.0,rt=1:00,cht=col,mth=sum



<name xsi:type="xsd:string">AKSELØYA</name>
<stnr xsi:type="xsd:int">99765</stnr>

Vind:
http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99765.16,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=99765.14,rt=1:00,cht=line,mth=inst
TA/RR:
http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99765.17,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=99765.0,rt=1:00,cht=col,mth=sum


<name xsi:type="xsd:string">KAPP MARTIN</name>
<stnr xsi:type="xsd:int">99780</stnr>

<name xsi:type="xsd:string">ISFJORD RADIO</name>
<stnr xsi:type="xsd:int">99790</stnr>

Vind:
http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99790.16,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=99790.14,rt=1:00,cht=line,mth=inst
TA/RR:
http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99790.17,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=99790.0,rt=1:00,cht=col,mth=sum


<name xsi:type="xsd:string">ISFJORD RADIO</name>
<stnr xsi:type="xsd:int">99800</stnr>

<name xsi:type="xsd:string">BARENTSBURG</name>
<stnr xsi:type="xsd:int">99820</stnr>

Vind:
http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99820.16,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=99820.14,rt=1:00,cht=line,mth=inst
TA/RR:
http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99820.17,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=99820.0,rt=1:00,cht=col,mth=sum


<name xsi:type="xsd:string">SVALBARD LUFTHAVN</name>
<stnr xsi:type="xsd:int">99840</stnr>

Vind:
http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99840.16,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=99840.14,rt=1:00,cht=line,mth=inst
TA/RR:
http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99840.17,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=99840.0,rt=1:00,cht=col,mth=sum


<name xsi:type="xsd:string">SVALBARD LH - PLATÅBERGET</name>
<stnr xsi:type="xsd:int">99841</stnr>

<name xsi:type="xsd:string">PYRAMIDEN</name>
<stnr xsi:type="xsd:int">99880</stnr>

Vind:
http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99880.16,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=99880.14,rt=1:00,cht=line,mth=inst
TA/RR:
http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99880.17,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=99880.0,rt=1:00,cht=col,mth=sum



Kan bruke relative verdier både for "time" og for å markere perioder "chsl"

&chd= - foran alle dataserier

hver dataserie har følgende elemneter
- ds
- da
- id
- rt :
- cht : line, col, marker, area
- mth : inst, sum, mean, min, max

Timesnedbør
ds=htsre,da=29,id=XXXXX.0,rt=1:00,cht=col,mth=sum

Temperatur
ds=htsre,da=29,id=XXXXX.17,rt=1:00,cht=line,mth=inst

Vindretning
ds=htsre,da=29,id=XXXXX.14,rt=1:00,cht=line,mth=inst

Vindstyrke
ds=htsre,da=29,id=XXXXX.16,rt=1:00,cht=line,mth=inst

Snødybde:
ds=htsre,da=29,id=XXXXX.2002,rt=1:00,cht=area,mth=inst -  - funker ikke



"""
"http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-25;0&chs=1000x600&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=99840.0,rt=1,cht=col,mth=sum|ds=htsre,da=29,id=99840.17,rt=1:00,cht=line,mth=inst"

"http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=18980.0,rt=1:00,cht=col,mth=sum"


# Nedbør og temperatur
"http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=XXXXX.17,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=XXXXX.0,rt=1:00,cht=col,mth=sum"

# Vind styrke og retning
"http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=XXXXX.16,rt=1:00,cht=line,mth=inst|ds=htsre,da=29,id=XXXXX.14,rt=1:00,cht=line,mth=inst"

# Snødybde
"http://h-web01.nve.no/chartserver/ShowChart.aspx?req=getchart&ver=1.0&time=-5;0&chs=800x400&lang=no&chlf=short&chsl=-5;-4|-3;-2|-1;0&chd=ds=htsre,da=29,id=XXXXX.2002,rt=1:00,cht=area,mth=inst"