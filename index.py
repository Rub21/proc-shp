#!/usr/bin/python
from shapely.geometry import mapping, shape
from fiona import collection
import midleLine
import sys

def __unicode__(self):
  return unicode(self) or u''

geos = []
dictionary={}

with collection(sys.argv[1], "r") as input:
  for geo in input:
    name1 = __unicode__(geo['properties']['NM_TIPO_LO']) + ' ' + __unicode__(geo['properties']['NM_TITULO_']) + ' ' + __unicode__(geo['properties']['NM_NOME_LO'])
    name=name1.title()
    if name !='None None None' and shape(geo['geometry']).type == 'LineString':
      if dictionary.has_key(name):
        dictionary[name].append(geo)
      else:
        dictionary[name]=[geo]


schema = { 'geometry': 'LineString', 'properties': { 'name': 'str' } }
with collection("result.shp", "w", "ESRI Shapefile", schema) as output:
  for key in dictionary:
    for i in dictionary[key]:
     for j in dictionary[key]:
      midline = midleLine.midline(shape(i['geometry']),shape(j['geometry']))
      if midline != None:
        output.write({
          'properties': {
            'name': key
          },
          'geometry': mapping(midline)
        })
