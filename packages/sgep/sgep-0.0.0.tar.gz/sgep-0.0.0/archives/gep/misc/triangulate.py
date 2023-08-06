#
# geom.misc.triangulate
# :: Triangulate a polygon using delaunay method.
# 

import time
import shapely 

def triangulate(polygon, inner_points = []): 
    inner_points = inner_points
    all_points = polygon + inner_points
    polygon_ = shapely.Polygon(polygon)
    all_points_ = shapely.MultiPoint(all_points)

    triangles_ = shapely.delaunay_triangles(all_points_)
    filtered_triangles = []

    for i in range(len(triangles_.geoms)): 
        triangle_ = triangles_.geoms[i]
        triangle = list(triangle_.exterior.coords)
        centroid_ = triangle_.centroid 
        if polygon_.contains(centroid_): 
            filtered_triangles.append(triangle)

    return filtered_triangles