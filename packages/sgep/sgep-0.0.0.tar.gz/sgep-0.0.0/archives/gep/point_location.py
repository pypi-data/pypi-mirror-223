#
# POINT LOCATION MODULE 
#

import shapely 
import gep.misc.globals as globals_

from dsap.queues.structs.priority_queue import PriorityQueue

from gep.misc.triangulate import triangulate 


class NormalPointLocator: 
    def __init__(self, polygons, **kwargs):
        self.polygons = polygons 
        self.polygons_ = [ shapely.Polygon(polygon) for polygon in self.polygons ] 

    def locate(self, needle): 
        needle_ = shapely.Point(needle) 
        for i in range(len(self.polygons_)): 
            polygon_ = self.polygons_[i] 
            if polygon_.contains(needle_):
                return i 
        return None 

class STRTPointLocator: 
    def __init__(self, polygons, **kwargs): 
        self.polygons = polygons 
        self.polygons_ = [ shapely.Polygon(polygon) for polygon in self.polygons ] 

        self.tree = None 

        self.build_tree()

    def build_tree(self): 
        bboxes = []
        polygons = self.polygons

        for i in range(len(polygons)): 
            polygon = polygons[i]
            polygon_ = self.polygons_[i] 
            bounds = polygon_.bounds 
            bbox = shapely.box(*bounds) 
            bboxes.append(bbox) 

        self.tree = shapely.STRtree(bboxes)
        self.bboxes = bboxes 
    
    def locate(self, needle): 
        tree = self.tree
        needle_ = shapely.Point(needle)
        for i in tree.query(needle_, predicate="intersects"): 
            polygon_ = self.polygons_[i] 
            if polygon_.contains(needle_): 
                return i    
        return None


class DTSTRTPointLocator: 
    def __init__(self, polygons, **kwargs): 
        self.polygons = polygons 
        self.polygons_ = [ shapely.Polygon(polygon) for polygon in self.polygons ] 

        self.tree = None  
        self.triangles_ = [] 
        self.indexer = [] 

        self.make_triangles() 

    def make_triangles(self): 
        polygons = self.polygons 

        bboxes = []
        
        for i in range(len(polygons)): 
            polygon = polygons[i] 
            polygon_ = self.polygons_[i] 
            triangles = triangulate(polygon) 
            
            for triangle in triangles: 
                triangle_ = shapely.Polygon(triangle)
                
                bounds = triangle_.bounds 
                bbox = shapely.box(*bounds) 
                bboxes.append(bbox) 


                self.triangles_.append(triangle_) 
                self.indexer.append(i) 

        self.tree = shapely.STRtree(bboxes) 

    def locate(self, needle): 
        needle_ = shapely.Point(needle)

        tree = self.tree 

        for i in tree.query(needle_, predicate="intersects"): 
            triangle_ = self.triangles_[i] 
            
            if triangle_.contains(needle_): 
                polygon_i = self.indexer[i] 
                return polygon_i

        return None



def make_point_locator(polygons, **kwargs): 
    method = kwargs.get("method", "dstrt") 
    
    if method == "normal": 
        return NormalPointLocator(polygons, **kwargs) 
    elif method == "strt": 
        return STRTPointLocator(polygons, **kwargs) 
    elif method == "dtstrt": 
        return DTSTRTPointLocator(polygons, **kwargs) 
    else: 
        raise Exception(f"Unknown method {method}")