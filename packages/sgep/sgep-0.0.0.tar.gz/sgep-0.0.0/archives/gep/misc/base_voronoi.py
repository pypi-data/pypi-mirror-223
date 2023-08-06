import shapely 

def base_voronoi(points, bounds = ((0, 0), (1920, 1080))):

    # generate voronoi diagram
    voronoi = shapely.voronoi_polygons(
        shapely.MultiPoint(points), 
        extend_to = shapely.LineString(bounds)
    )

    # transform geoms to 2D array
    geoms = [list(g.exterior.coords) for g in voronoi.geoms]

    return geoms 
