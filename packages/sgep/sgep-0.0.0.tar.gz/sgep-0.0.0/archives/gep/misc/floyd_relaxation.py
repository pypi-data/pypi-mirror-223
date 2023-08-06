import shapely
from geom_helpers.randomness.random_points import random_aabb_points

def floyd_relax_once(points): 
    voronoi = shapely.voronoi_polygons(shapely.MultiPoint(list(points)))
    centroids = []
    for geom in voronoi.geoms: 
        centroids.append(list(geom.centroid.coords)[0])
    return centroids

def floyd_relax(points, k): 
    for i in range(k):
        points = floyd_relax_once(points) 
    return points

if __name__ == "__main__": 
    import svgwrite 
    points = random_aabb_points((0, 0), (1920, 1080), 1000) 
    n_points = relax_once(points) 

    draw = svgwrite.Drawing(filename="outputs/output.svg", size=(1920, 1080)) 

    for point in points:
        draw.add(draw.circle(center=point, fill="grey", r=3))

    for point in n_points:
        draw.add(draw.circle(center=point, fill="green", r=3))

    draw.save()

