#!/usr/bin/python
from shapely.geometry import box
import sys
import shapefile
import midleLine

sf = shapefile.Reader("31471050500/31471050500_face.shp")
shapes = sf.shapeRecords()
codes = []
data = []

for index in range(len(shapes)):
   shape =shapes[index]
   print shape.record[5] + ' ' + shape.record[6] + ' ' + shape.record[7]
   


   # print shape.shape.type
# for shape in shapes:
#   codes.append(shape.record[5] + ' ' + shape.record[6] + ' ' + shape.record[7])
#   data.append(shape.shape.bbox)


print len(codes)
print len(data)
