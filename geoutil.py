#!/usr/bin/python
from shapely.geometry import Point, LineString, mapping
import json

# import sys
# import shapefile
# line = LineString([Point(51.15234375,62.512317938386914),Point(40.78125,56.26776108757582),Point(14.765625,34.45221847282654),Point(-0.87890625,11.350796722383672)])
# line2 = LineString([Point(79.98046875,59.80063426102869),Point(66.796875,53.014783245859235),Point(52.3828125,42.8115217450979),Point(42.890625,35.31736632923788),Point(31.640625,20.3034175184893),Point(18.10546875,0.8788717828324276)])

def midline(line1, line2):
    coordinates = []
    for coord in line1.coords:
      flag = True
      
      p = midpoint(Point(coord),line2);
      if (Point(coord).distance(p) < 0.0001) and (Point(coord).distance(p) > 0):
        coordinates.append(p)
        flag = False

      # if (Point(coord).distance(p) < 0.0002) and (Point(coord).distance(p) > 0) and hasIntersection(line1,line2) and flag:
      #   coordinates.append(p)

    if len(coordinates)> 1:
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


def pair(list):
    for i in range(1, len(list)):
        yield list[i-1], list[i]

def segmets(line):
  arraySegments=[]
  for seg_start, seg_end in pair(line.coords):
      line_start = Point(seg_start)
      line_end = Point(seg_end)
      segment = LineString([line_start.coords[0],line_end.coords[0]])
      arraySegments.append(segment)
  return arraySegments


def hasIntersection(line1,line2):
  line1Coordinates = line1.coords
  line2Coordinates = line2.coords
  line1CoordFirst = line1Coordinates[0]
  line1CoordLast = line1Coordinates[len(line1Coordinates)-1]
  line2CoordFirst = line2Coordinates[0]
  line2CoordLast = line2Coordinates[len(line2Coordinates)-1]
  inter1 = LineString([Point(line1CoordFirst), Point(line2CoordFirst)]).intersection(LineString([Point(line1CoordLast),Point(line2CoordLast)])).is_empty
  inter2 = LineString([Point(line1CoordLast), Point(line2CoordLast)]).intersection(LineString([Point(line1CoordFirst),Point(line2CoordFirst)])).is_empty
  inter3 = LineString([Point(line1CoordFirst), Point(line2CoordLast)]).intersection(LineString([Point(line1CoordLast),Point(line2CoordFirst)])).is_empty
  inter4 = LineString([Point(line2CoordFirst),Point(line1CoordLast)]).intersection(LineString([Point(line2CoordLast),Point(line1CoordFirst)])).is_empty
  return inter1 or inter2 or inter3 or inter4
