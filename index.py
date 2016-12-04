#!/usr/bin/python
from shapely.geometry import mapping, shape, box
from fiona import collection
import togeojson

def __unicode__(self):
  return unicode(self) or u''

with collection("31471050500_face.shp", "r") as input:
  for geo in input:
    # print shape(geo['geometry'])
    # print geo['properties']
    togeojson.printgeo(geo)
