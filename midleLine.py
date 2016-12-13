#!/usr/bin/python
from shapely.geometry import Point, LineString, mapping
import json

# import sys
# import shapefile
# line1 = LineString([Point(51.15234375,62.512317938386914),Point(40.78125,56.26776108757582),Point(14.765625,34.45221847282654),Point(-0.87890625,11.350796722383672)])
# line2 = LineString([Point(79.98046875,59.80063426102869),Point(66.796875,53.014783245859235),Point(52.3828125,42.8115217450979),Point(42.890625,35.31736632923788),Point(31.640625,20.3034175184893),Point(18.10546875,0.8788717828324276)])

def midline(line1, line2):
  coordinates = []
  for coord in line1.coords:
    p = midpoint(Point(coord),line2);
    # print Point(coord).distance(p)
    if (Point(coord).distance(p) < 0.0002) and (Point(coord).distance(p) > 0):
      coordinates.append(p)
  if len(coordinates)>1:
    return LineString(coordinates)
  else:
    return None

def midpoint(point, line):
    np = line.interpolate(line.project(point))
    return Point((point.x+np.x)/2, (point.y+np.y)/2)
# print json.dumps(mapping(midline(line1,line2)))

def midpoint2(point, line):
    p = midpoint(point,line);
    if (point.distance(p) < 0.0002) and (point.distance(p) > 0):
      return p
    else:
      return None
