#!/usr/bin/python
from shapely.geometry import LineString, mapping, shape
from fiona import collection
# from shapely.ops import linemerge
from shapely.ops import cascaded_union
import midleLine
import sys

def __unicode__(self):
  return unicode(self) or u''

geos = []
dictionary={}
rDictionary={}
rCoordinates={}
with collection(sys.argv[1], "r") as input:
  for geo in input:
    name1 = __unicode__(geo['properties']['NM_TIPO_LO']) + ' ' + __unicode__(geo['properties']['NM_TITULO_']) + ' ' + __unicode__(geo['properties']['NM_NOME_LO'])
    name=name1.title()
    if name !='None None None' and shape(geo['geometry']).type == 'LineString':
      if dictionary.has_key(name):
        dictionary[name].append(geo)
      else:
        dictionary[name]=[geo]


for key in dictionary:
  for i in dictionary[key]:
    for j in dictionary[key]:
      midline = midleLine.midline(shape(i['geometry']),shape(j['geometry']))
      if midline != None:
        if rDictionary.has_key(key):
          for c in midline.coords:
            rCoordinates[key].append(c)
          rDictionary[key].append(midline);
        else:
          rCoordinates[key]=[]
          for c in midline.coords:
            rCoordinates[key].append(c)
          rDictionary[key]=[midline]


# schema = { 'geometry': 'LineString', 'properties': { 'name': 'str' } }
# with collection("result.shp", "w", "ESRI Shapefile", schema) as output:
#   for key in rDictionary:
#     # print rCoordinates[key]
#     # sortedCoords = sorted(rCoordinates[key] , key=lambda k: [k[1], k[0]])

#     output.write({
#       'properties': {
#         'name': key
#       },
#       'geometry': mapping(LineString(rCoordinates[key]))
#     })
        
        


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
