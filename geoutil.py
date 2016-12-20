#!/usr/bin/python
from shapely.geometry import Point, LineString, mapping
import json
import numpy as np

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

      if (Point(coord).distance(p) < 0.0002) and (Point(coord).distance(p) > 0) and hasIntersection(line1,line2) and flag:
       coordinates.append(p)

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

def isConsecutive(line1,line2):
  line1Coordinates = line1.coords
  line2Coordinates = line2.coords
  line1CoordFirst = line1Coordinates[0]
  line1CoordLast = line1Coordinates[len(line1Coordinates)-1]
  line2CoordFirst = line2Coordinates[0]
  line2CoordLast = line2Coordinates[len(line2Coordinates)-1]
  inter1 = set(line1CoordFirst) == set(line2CoordFirst)
  inter2 = set(line1CoordFirst) == set(line2CoordLast)
  inter3 = set(line1CoordLast) == set(line2CoordFirst)
  inter4 = set(line1CoordLast) == set(line2CoordLast)
  return inter1 or inter2 or inter3 or inter4

def mergeTwoLines(line1,line2):
  coords = list(line1.coords) + list(line2.coords)
  sortedCoords = sorted(coords , key=lambda k: [k[1], k[0]])
  points =[]
  for c in coords:
    points.append(Point(c))
  return LineString(points)


def isParallel(line1, line2):
  line1Coordinates = line1.coords
  line2Coordinates = line2.coords
  line1CoordFirst = line1Coordinates[0]
  line1CoordLast = line1Coordinates[len(line1Coordinates)-1]
  # line2CoordFirst = line2Coordinates[0]
  # line2CoordLast = line2Coordinates[len(line2Coordinates)-1]
  np1 = line2.interpolate(line2.project(Point(line1CoordFirst)))
  np2 = line2.interpolate(line2.project(Point(line1CoordLast)))
  angle1 = get_angle1(list(np1.coords)[0],line1CoordFirst,line1.coords[1])
  angle2 = get_angle1(list(np2.coords)[0],line1CoordLast,line1.coords[len(line1.coords)-2])
  l1 = LineString([line1CoordFirst,np1])
  l2 = LineString([line1CoordLast,np2])
  valueAngle = (angle1> 70 and angle1 < 110) or (angle2> 70 and angle2 < 110)
  if l1.length < 0.0005 and l2.length < 0.0005  and valueAngle: #hasIntersection(line1,line2)
    return True
  return False


def get_angle(p0, p1=np.array([0,0]), p2=None):
    if p2 is None:
        p2 = p1 + np.array([1, 0])
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)
    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return abs(np.degrees(angle))


def get_angle1(p0, p1, p2):
# for p0p1p2 corner
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)

    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return abs(np.degrees(angle))