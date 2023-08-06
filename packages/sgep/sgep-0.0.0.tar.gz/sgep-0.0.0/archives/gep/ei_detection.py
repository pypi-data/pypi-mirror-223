#
# EXTERIOR-INTERIOR DETECTION MODULE 
# 

from gep.structs.edge_bst import EdgeBST
from gep.structs.point_bst import PointBST

from gep.misc.comparators import *

class EI_Detector: 
    def __init__(self, polygons): 
        self.polygons = polygons
        self.edge_polygons = PointBST()

        self.vertex_id = PointBST()
        self.id_vertex = {}
        
        self.outer_edges = set()
        self.outer_polygons = set()

        self.inner_edges = set() 
        self.inner_polygons = set()

        self.run()

    def register_edges(self): 
        polygons = self.polygons 

        vertex_id = 0
        
        for polygon_id in polygons:
            polygon = polygons[polygon_id]

            for i in range(len(polygon)): 
                # identify edge
                j = (i + 1) % len(polygon) 
                
                a = polygon[i] 
                b = polygon[j] 
                
                e = None 

                if self.vertex_id.find(a) is None: 
                    self.vertex_id.insert(a, vertex_id)
                    self.id_vertex[vertex_id] = a
                    vertex_id += 1 
                
                if self.vertex_id.find(b) is None: 
                    self.vertex_id.insert(b, vertex_id) 
                    self.id_vertex[vertex_id] = b
                    vertex_id += 1 

                # normalize edge
                a_id = self.vertex_id.find(a).value
                b_id = self.vertex_id.find(b).value

                if a_id < b_id: 
                    e = (a_id, b_id)
                else: 
                    e = (b_id, a_id)
                
                # register edge if needed
                if self.edge_polygons.find(e) is None: 
                    self.edge_polygons.insert(e, set())

                # add polygon to edge
                self.edge_polygons.find(e).value.add(polygon_id)

    def run(self):
        polygons = self.polygons
        
        self.register_edges() 

        # detect edges with only a single polygon 
        # for edge_id in self.edge_polygons:
        for edge_id in self.edge_polygons.keys(): 
            polygon_ids = self.edge_polygons.find(edge_id).value
            if len(polygon_ids) == 1: 
                self.outer_edges.add(edge_id)
                for polygon_id in polygon_ids: 
                    self.outer_polygons.add(polygon_id)

        for edge_id in self.edge_polygons.keys(): 
            if edge_id not in self.outer_edges: 
                self.inner_edges.add(edge_id)
                polygon_ids = self.edge_polygons.find(edge_id).value
                for polygon_id in polygon_ids: 
                    if polygon_id not in self.outer_polygons: 
                        self.inner_polygons.add(polygon_id)



