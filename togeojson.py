#!/usr/bin/python
from shapely.geometry import mapping, shape
from fiona import collection



def __unicode__(self):
  return unicode(self) or u''

  
def printgeo(geo):
  name = __unicode__(geo['properties']['NM_TIPO_LO']) + ' ' + __unicode__(geo['properties']['NM_TITULO_']) + ' ' + __unicode__(geo['properties']['NM_NOME_LO'])
  print {
          'properties': {
            'name': name
          },
          'geometry': mapping(shape(geo['geometry']))
        }
