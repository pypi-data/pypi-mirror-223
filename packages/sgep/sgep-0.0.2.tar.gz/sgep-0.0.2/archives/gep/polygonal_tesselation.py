
import shapely
import random 

from gep.polygon_graphing import PolygonGraph
from gep.misc.random_shapes import random_concave_polygon
from gep.misc.random_points import random_points_in_polygon
from gep.tesselation_merging import TesselationMerger
from gep.misc.indexify import indexify

from gep.polygonal_voronoi import polygonal_voronoi

draw = None

def tesselate_polygon(polygon, **kwargs): 
    
    # extract parameters
    points = kwargs.get("points", None)
    relax = kwargs.get("relax", 0)
    
    n_sources = kwargs.get("n_sources", 10)
    sampling_mode = kwargs.get("sampling_mode", "uniform")
    min_buffer = kwargs.get("min_buffer", 1)
    max_buffer = kwargs.get("max_buffer", 1)
    ave_buffer = kwargs.get("ave_buffer", 10) 
    std_dev_buffer = kwargs.get("std_dev_buffer", 5)

    # generate points if necessary 
    if points is None: 
        n_points = kwargs.get("n_points", 100)
        points = random_points_in_polygon(polygon, n_points, relax = relax)

    # compute a voronoi diagram from the polygon
    polygon = shapely.Polygon(polygon)
    points = list(points)
    convex_tesselation = indexify(polygonal_voronoi(polygon, points))
    
    # merge voronoi cells
    polygon_graph = PolygonGraph(convex_tesselation) 
    polygon_graph.make_edge_adjacencies() 
    
    merger = TesselationMerger(
        polygon_graph,
        n_sources=n_sources,
        sampling_mode=sampling_mode,
        min_buffer=min_buffer,
        max_buffer=max_buffer,
        ave_buffer=ave_buffer, 
        std_dev_buffer=std_dev_buffer
    )

    return merger.get_merged_polygons()

