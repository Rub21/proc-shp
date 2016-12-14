#!/usr/bin/python
from shapely.geometry import LineString, mapping, shape, Point
from fiona import collection
# from shapely.ops import linemerge
from shapely.ops import cascaded_union
from rtree import index
import midleLine
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
    if shape(geo['geometry']).type == 'LineString':

      idx.insert(id, shape(geo['geometry']).bounds)
      dictionary[id] = geo
      id=id+1

for key in dictionary:
  nearestObjs = list(idx.nearest(shape(dictionary[key]['geometry']).bounds,30))
  pkey = dict(dictionary[key]['properties'])
  # print pkey['CD_SETOR']
  for k in nearestObjs:
    pk=dict(dictionary[k]['properties'])
    if k != key:
      midline = midleLine.midline(shape(dictionary[key]['geometry']),shape(dictionary[k]['geometry']))
      if midline != None and (not midline.is_closed) :
        int1=midline.intersection(shape(dictionary[key]['geometry'])).is_empty
        int2=midline.intersection(shape(dictionary[k]['geometry'])).is_empty
        if int2 and int1:
            intersects = list(idx.nearest(midline.bounds,10))
            flag=True
            for x in intersects:
               if not shape(dictionary[x]['geometry']).intersection(midline).is_empty:
                flag=False
            if flag:
              geos.append(midline)


schema = { 'geometry': 'LineString', 'properties': { 'name': 'str' } }
with collection("linea.shp", "w", "ESRI Shapefile", schema) as output:
  for geo in geos:
    output.write({
      'properties': {
            'name': str(key)
          },
          'geometry': mapping(geo)
      })
