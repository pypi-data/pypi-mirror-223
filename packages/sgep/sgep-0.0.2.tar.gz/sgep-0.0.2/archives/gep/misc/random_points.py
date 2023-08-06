#
# geom.misc.random_points 
# :: Generate random points on different surfaces.
# 

import random
import shapely
from gep.misc.triangulate import triangulate

draw = None

def random_aabb_point(a, b):
    point = None
    x = random.uniform(a[0], b[0])
    y = random.uniform(a[1], b[1])
    point = (x, y)
    return point 

def random_aabb_points(a, b, n_points):
    points = set() 
    while len(points) < n_points: 
        point = random_aabb_point(a, b) 
        points.add(point) 
    return points  

def random_point_in_line(a, b, exclusive = True): 
    width = b[0] - a[0]
    height = b[1] - a[1]

    if width == 0: 
        return random.choice([(a[0], a[1]), (b[0], b[1])])

    slope = height / width 
    
    width_theta  = random.uniform(0, width) 
    height_theta = width_theta * slope 
    
    x = a[0] + width_theta 
    y = a[1] + height_theta  
    point = (x, y)

    return point 

def random_points_in_line(a, b, n_points): 
    points = set() 
    while len(points) < n_points: 
        point = random_point_in_line(a, b) 
        points.add(point) 
    return points  

def random_point_in_triangle(triangle): 
    ab_point = None 
    bc_point = None 

    mode = random.randint(0, 2)
    
    if mode == 0:  
        ab_point = random_point_in_line(triangle[0], triangle[1]) 
        bc_point = random_point_in_line(triangle[1], triangle[2]) 
    elif mode == 1:
        ab_point = random_point_in_line(triangle[1], triangle[2]) 
        bc_point = random_point_in_line(triangle[2], triangle[0]) 
    elif mode == 2: 
        ab_point = random_point_in_line(triangle[2], triangle[0]) 
        bc_point = random_point_in_line(triangle[0], triangle[1]) 

    bisector = (ab_point, bc_point)
    point = random_point_in_line(bisector[0], bisector[1]) 

    return point

def random_points_in_triangle(triangle, n_points): 
    points = set() 
    while len(points) < n_points: 
        point = random_point_in_triangle(triangle) 
        points.add(point) 
    return points  

def random_point_in_polygon_precomp(polygon): 
    from gep.misc.areas import triangle_area

    areas = []
    area = 0

    triangles = triangulate(polygon)

    i = 0
    for triangle in triangles:
        tri_area = triangle_area(triangle)
        areas.append(tri_area)
        area += tri_area
        i += 1 
    
    for i in range(len(areas)): 
        areas[i] = areas[i] / area 

    return triangles, areas


def random_point_in_polygon(polygon, triangles = None, areas = None): 
    if triangles is None: 
        triangles, areas = random_point_in_polygon_precomp(polygon)    
    
    # select triangle to generate a point from based on probability 
    # on area, bigger polygons gets generated in more often
    triangle = random.choices(triangles, areas, k = 1)[0]
    
    point = random_point_in_triangle(triangle)

    return point

def random_points_in_polygon(polygon, n_points, relax = 0): 
    from gep.polygonal_voronoi import polygonal_voronoi
    
    polygon_ = shapely.Polygon(polygon)

    # triangulate the polygon and get the areas of each triangle 
    triangles, areas = random_point_in_polygon_precomp(polygon)  
    
    # generate points in the polygon 
    points = set() 
    while len(points) < n_points: 
        point = random_point_in_polygon(polygon, triangles, areas) 
        points.add(point) 

    # relax points by moving them to centroids
    if relax > 0: 
        for i in range(relax):
            tesselation = polygonal_voronoi(polygon, points)
            centroids = [] 
            
            for geom in tesselation:
                geom_ = shapely.Polygon(geom)
                centroid_ = geom_.centroid 
                centroid = list(centroid_.coords)[0] 
                
                # remove centroid if it is not anymore in the polygon 
                if not polygon_.contains(centroid_): 
                    continue

                centroids.append(centroid)

            points = centroids 
                
    return points  

