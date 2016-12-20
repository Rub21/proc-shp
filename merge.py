#!/usr/bin/python
from shapely.geometry import LineString, mapping, shape, Point
from fiona import collection
# from shapely.ops import linemerge
from shapely.ops import cascaded_union
from rtree import index
import geoutil
import sys

def __unicode__(self):
  return unicode(self) or u''

geos = []
dictionary={}
rDictionary={}
rCoordinates={}
id=0
idx = index.Index()
with collection(sys.argv[1], "r") as input:
  for geo in input:
    name1 = __unicode__(geo['properties']['NM_TIPO_LO']) + ' ' + __unicode__(geo['properties']['NM_TITULO_']) + ' ' + __unicode__(geo['properties']['NM_NOME_LO'])
    name=name1.title()
    line = shape(geo['geometry'])
    if line.type == 'LineString':
      geo['properties']['name'] = name
      idx.insert(id, line.bounds)
      dictionary[id] = geo
      id=id+1

for key in dictionary:
    line1 = shape(dictionary[key]['geometry'])
    nearestObjs = list(idx.nearest(line1.bounds,20))
    for k in nearestObjs:
        if k != key:
            line2 = shape(dictionary[k]['geometry'])
            if geoutil.isConsecutive(line1,line2):
                line1=geoutil.mergeTwoLines(line1,line2)
    dictionary[key]= {
        'properties': {
            'name': '23'
        },
        'geometry': mapping(line1)
    }




schema = { 'geometry': 'LineString', 'properties': { 'name': 'str' } }
with collection("lineapoly.shp", "w", "ESRI Shapefile", schema) as output:
  for key in dictionary:
    # print geo['properties']
    output.write({
        'properties': {
            'name': '21'
          },
        'geometry': mapping(shape(dictionary[key]['geometry']))
      })