#
# gep.misc.areas
# :: Computes areas of different shapes.
# 

import math 

from .distance import euclidean_distance
from gep.misc.triangulate import triangulate

def circle_area(radius): 
    return math.PI * (radius ** 2)

def square_area(side): 
    return side ** 2 

def rectangle_area(width, height): 
    return width * height

def triangle_area(triangle): 
    a = euclidean_distance(triangle[0], triangle[1])
    b = euclidean_distance(triangle[1], triangle[2])
    c = euclidean_distance(triangle[2], triangle[3]) 

    s = (a + b + c) / 2
    
    a = (s * (s - a) * (s - b) * (s - c)) ** (1/2)

    return a

def polygon_area(polygon):
    triangles = triangulate(polygon) 
    area = 0 
    for triangle in triangles: 
        area += triangle_area(triangle)
    return area 



