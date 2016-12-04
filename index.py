#!/usr/bin/python
from shapely.geometry import mapping, shape
from fiona import collection
import togeojson
import midleLine
def __unicode__(self):
  return unicode(self) or u''

geos = []
with collection("31471050500_face.shp", "r") as input:
  for geo in input:
    geos.append(geo)
    # print shape(geo['geometry'])
    # print geo['properties']
    # togeojson.printgeo(geo)
    # print shape(geo['geometry']).bounds

for geo in geos:
  name1 = __unicode__(geo['properties']['NM_TIPO_LO']) + ' ' + __unicode__(geo['properties']['NM_TITULO_']) + ' ' + __unicode__(geo['properties']['NM_NOME_LO'])
  for g in geos:
    name2 = __unicode__(g['properties']['NM_TIPO_LO']) + ' ' + __unicode__(g['properties']['NM_TITULO_']) + ' ' + __unicode__(g['properties']['NM_NOME_LO'])
    if geo['properties']['ID'] != g['properties']['ID'] and name1 == name2:
      # print g['geometry']
      midline = midleLine.midline(shape(geo['geometry']),shape(g['geometry']))
      # midline['properties']['name'] = name1
      togeojson.printgeo(midline)




