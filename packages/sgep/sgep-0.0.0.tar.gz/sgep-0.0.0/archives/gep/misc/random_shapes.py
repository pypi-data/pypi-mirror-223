#
# geom.misc.random_shapes
# :: Generates random shapes.
#  

import random 
import shapely

from .random_points import *
from gep.misc.base_voronoi import base_voronoi
from gep.tesselation_merging import TesselationMerger

draw = None

def random_convex_polygon(a, b, n_points): 
    points = list(random_aabb_points(a, b, n_points * 2))
    hull = shapely.convex_hull(shapely.MultiPoint(points))
    return list(hull.exterior.coords)

def random_concave_polygon(a, b, n_points, ratio=0.1): 
    points = list(random_aabb_points(a, b, n_points * 2))
    hull = shapely.concave_hull(shapely.MultiPoint(points), ratio=ratio)
    return list(hull.exterior.coords)

def random_triangle(a, b): 
    points = list(random_aabb_points(a, b, 3))
    return points

def random_circle(a, b, radius = None):
    width = abs(a[0] - b[0])
    height = abs(a[1] - b[1]) 
    if radius == None:
        radius = random.randint(1, min(width, height))
    cx = random.uniform(radius, width - radius)
    cy = random.uniform(radius, height - radius)
    return ((cx, cy), radius)

def random_base_voronoi(n_points, bounds = ((0, 0), (1920, 1080))):
    # generate points
    points = list(random_aabb_points(bounds[0], bounds[1], n_points))
    return base_voronoi(points, bounds), points

def random_tesselated_polygon(a, b, n_points, k_points, **kwargs): 
    from gep.polygonal_tesselation import tesselate_polygon

    relax = kwargs.get("relax", 0) 
    ratio = kwargs.get("ratio", 0.1)
    
    n_sources = kwargs.get("n_sources", 10)
    sampling_mode = kwargs.get("sampling_mode", "uniform")
    min_buffer = kwargs.get("min_buffer", 1)
    max_buffer = kwargs.get("max_buffer", 1)
    ave_buffer = kwargs.get("ave_buffer", 10) 
    std_dev_buffer = kwargs.get("std_dev_buffer", 5)

    # generate polygon
    polygon = random_concave_polygon(a, b, n_points, ratio)
    
    # generate points 
    points = random_points_in_polygon(polygon, k_points, relax) 

    # create tesselation
    tesselation = tesselate_polygon(
        polygon, 
        points=points, 
        n_sources=n_sources,
        sampling_mode=sampling_mode,
        min_buffer=min_buffer,
        max_buffer=max_buffer,
        ave_buffer=ave_buffer, 
        std_dev_buffer=std_dev_buffer
    )

    return tesselation, polygon
