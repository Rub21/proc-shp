#!/usr/bin/python
from shapely.geometry import mapping, shape
from fiona import collection
import togeojson
import midleLine
def __unicode__(self):
  return unicode(self) or u''

geos = []
with collection("31471050500_face.shp", "r") as input:
  schema = { 'geometry': 'LineString', 'properties': { 'name': 'str' } }
  with collection("some_buffer.shp", "w", "ESRI Shapefile", schema) as output:
     for geo in input:
      geos.append(geo)
      name = __unicode__(geo['properties']['NM_TIPO_LO']) + ' ' + __unicode__(geo['properties']['NM_TITULO_']) + ' ' + __unicode__(geo['properties']['NM_NOME_LO'])
      output.write({
          'properties': {
          'name': name.title()
          },
          'geometry': mapping(shape(geo['geometry']))
      })

