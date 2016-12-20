#!/usr/bin/python
from shapely.geometry import LineString, mapping, shape, Point
from fiona import collection
# from shapely.ops import linemerge
from shapely.ops import cascaded_union
from rtree import index
import geoutil
import sys
import fiona
import shapely.geometry
import shapely.ops

def __unicode__(self):
  return unicode(self) or u''

geos = []
dictionarySegments={}
dictionaryLine={}
rDictionary={}
rCoordinates={}
idLine=0
idSegment=0
idx = index.Index()
with collection(sys.argv[1], "r") as input:
  for geo in input:
    name = (__unicode__(geo['properties']['NM_TIPO_LO']) + ' ' + __unicode__(geo['properties']['NM_TITULO_']) + ' ' + __unicode__(geo['properties']['NM_NOME_LO'])).title()
    idGeo=geo['properties']['ID']
    line = shape(geo['geometry'])
    if line.type == 'LineString':
      # safe lines
      if line.is_closed:
        for segmet in geoutil.segmets(line):
          idx.insert(idLine, segmet.bounds)
          segGeom = {
                'properties': {
                    'name': name,
                    'id' : idGeo
                },
                'geometry': mapping(segmet)
            }
          segGeom['properties']['name'] = name
          dictionaryLine[idLine] = segGeom
          idLine=idLine+1
      geo['properties']['name'] = name
      geo['properties']['id'] = idGeo
      idx.insert(idLine, line.bounds)
      dictionaryLine[idLine] = geo
      idLine=idLine+1

      # safe segmets
      for segmet in geoutil.segmets(line):
        segGeom = {
            'properties': {
                  'name': name,
                  'id' : idGeo
              },
              'geometry': mapping(segmet)
          }
        dictionarySegments[idSegment] = segGeom
        idSegment=idSegment+1


dictMerge = {}
for key in dictionarySegments:  
  valueSegmentGeo=shape(dictionarySegments[key]['geometry'])  
  valueSegmentProperties = dict(dictionarySegments[key]['properties'])
  nearestLines = list(idx.nearest(valueSegmentGeo.bounds,10))
  for k in nearestLines:
    overlapLineGeo=shape(dictionaryLine[k]['geometry'])
    overlapLineProperties=dict(dictionaryLine[k]['properties'])
    if valueSegmentProperties['id'] != overlapLineProperties['id'] and geoutil.isParallel(valueSegmentGeo,overlapLineGeo):
      midline = geoutil.midline(valueSegmentGeo,overlapLineGeo)
      if midline != None and (not midline.is_closed) :
        int1=midline.intersection(valueSegmentGeo).is_empty
        int2=midline.intersection(overlapLineGeo).is_empty
        if int2 and int1:
            intersects = list(idx.nearest(midline.bounds,5))
            flag=True
            for x in intersects:
               if not shape(dictionaryLine[x]['geometry']).intersection(midline).is_empty:
                flag=False
            if flag:
              aId = [overlapLineProperties['id'], valueSegmentProperties['id']]
              if valueSegmentProperties['id'] > overlapLineProperties['id']:
                aId = [valueSegmentProperties['id'],overlapLineProperties['id']]
              id =  '-'.join(map(str,aId))
              midgeo = {
                'properties': {
                    'name': overlapLineProperties['name'],
                    'idl': overlapLineProperties['id'],
                    'ids': valueSegmentProperties['id'],
                    'id' : '-'.join(map(str,aId))

                },
                'geometry': mapping(midline)
              }
              if dictMerge.has_key(id):
                dictMerge[id].append(midgeo)
              else:
                dictMerge[id] =[midgeo]
              # geos.append(midgeo)

## Merge Lines
for key in dictMerge:
  coords =[]
  points = []
  # print len(dictMerge[key])
  # mergeline = LineString([]);
  for x in dictMerge[key]:
    eleGeo = shape(x['geometry']);
    eleProperties= x['properties']
    # mergeline.union(eleGeo)
    cs = eleGeo.coords
    for c in cs:
      coords.append(c)
  # print coords
  sortedCoords = sorted(coords , key=lambda k: [k[1], k[0]])

  for y in sortedCoords:
    points.append(Point(y))
  l =  {
        'properties': {
          'name': eleProperties['name'],
          'idl': eleProperties['idl'],
          'ids': eleProperties['ids'],
          'id' : eleProperties['id']
          },
          'geometry': mapping(LineString(points).simplify(0.00001, preserve_topology=True))
          }
  geos.append(l)

schema = { 'geometry': 'LineString', 'properties': { 'name': 'str' ,'idl': 'int:10' ,'ids': 'int:10','id': 'str'} }
with collection("linea.shp", "w", "ESRI Shapefile", schema) as output:
  for geo in geos:
    output.write({
      'properties': {
            'name': geo['properties']['name'],
            'idl': geo['properties']['idl'],
            'ids': geo['properties']['ids'],
            'id' : geo['properties']['id']
          },
          'geometry': mapping(shape(geo['geometry']))
      })

