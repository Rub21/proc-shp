#!/usr/bin/python

from shapely.geometry import Point, mapping, shape
from fiona import collection

with collection("31471050500_face.shp", "r") as input:
  for geo in input:
    print shape(geo['geometry'])
    print geo['properties']