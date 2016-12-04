#!/usr/bin/python
from shapely.geometry import mapping, shape
from fiona import collection
from mapbox import Static
import json


def __unicode__(self):
  return unicode(self) or u''


def printgeo(geo):
  # name = __unicode__(geo['properties']['name'])
  print {
          'type': 'Feature',
          'properties': {
            'name': 'name'
          },
          # 'geometry': mapping(shape(geo['geometry']))
          'geometry': json.dumps(mapping(geo))

        }
