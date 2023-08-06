#
# POLYGONAL VORONOI MODULE
# 

import shapely
import random 

from gep.polygon_graphing import PolygonGraph

from gep.misc.random_shapes import random_concave_polygon
from gep.misc.random_points import random_points_in_polygon

from gep.misc.indexify import indexify

def polygonal_voronoi(polygon, points, **kwargs):  
    polygon = shapely.Polygon(polygon)
    
    points = shapely.MultiPoint(list(points))
    voronoi = shapely.voronoi_polygons(points, **kwargs) 
    
    geoms = []

    for geom in voronoi.geoms: 
        intersection = polygon.intersection(geom)
        if hasattr(intersection, "geoms"): 
            for geom in intersection.geoms: 
                geom = list(geom.exterior.coords)
                if geom[-1] == geom[0]:
                    geom.pop()
                if len(geom) == 0: 
                    continue
                geoms.append(geom)
        else: 
            geom = list(intersection.exterior.coords)
            if len(geom) == 0: 
                continue 
            if geom[-1] == geom[0]:
                geom.pop()
            if len(geom) == 0: 
                continue
            geoms.append(geom)

    return geoms    
