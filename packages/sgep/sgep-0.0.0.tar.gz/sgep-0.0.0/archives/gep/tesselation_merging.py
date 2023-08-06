#
# TESSELATION MERGING MODULE
# 
import gep.misc.globals as globals_

import shapely
import numpy
import scipy
import numpy

from gep.polygon_graphing import PolygonGraph
from gep.misc.indexify import indexify
from gep.misc.areas import polygon_area

from dsap.queues.structs.deque import Deque

import random 

class TesselationMerger:
    def __init__(self, polygon_graph, **kwargs): 
        self.polygon_graph = polygon_graph

        self.visited = {}
        self.groups = {}  
        self.polygon_merge_counts = {}
        self.merged_polygons = {}
        self.groups = {}

        # PARAMETERS #

        self.n_sources = kwargs.get("n_sources", 10)
       
        self.sampling_mode = kwargs.get("sampling_mode", "normal")
       
        self.min_buffer = kwargs.get("min_buffer", 50)
        self.max_buffer = kwargs.get("max_buffer", 100)

        self.ave_buffer = kwargs.get("ave_buffer", 10), 
        self.std_dev_buffer = kwargs.get("std_dev_buffer", 5)

        #############

        self.polygon_ids = list(self.polygon_graph.polygons.keys())
        self.sources = None 
        self.visited = set()

        self.queues = {}
        self.source_groups = {}
        self.source_idx = {}

        self.init_sources()
        self.init_source_groups()
        self.draw_sources()
        self.init_queues()
        self.propagate() 
        self.merge_polygons()
        self.remove_holes()
        self.clean_up()


    def n_cells(self):
        return len(self.polygon_graph.polygons)

    def init_sources(self): 
        self.sources = random.choices(self.polygon_ids, k=self.n_sources)
      
        index = 0
        for source_id in self.sources: 
            self.source_idx[source_id] = index
            index += 1

    def init_source_groups(self): 
        sources = self.sources 
        for source_id in sources: 
            self.source_groups[source_id] = set([source_id])

    def draw_sources(self):
        sources = self.sources 
        for source_id in sources: 
            polygon = self.polygon_graph.polygons[source_id]

    def init_queues(self):
        sources = self.sources 
        for source_id in sources: 
            self.queues[source_id] = Deque()
            neighbors = self.polygon_graph.neighbors[source_id]
            for neighbor_id in neighbors: 
                self.queues[source_id].enqueue_back(neighbor_id)
                self.visited.add(source_id)

    def propagate(self): 
        sources = self.sources

        while len(self.visited) < self.n_cells():
            for source_id in self.sources: 
                source_queue = self.queues[source_id] 
                buffer_size = self.get_buffer_size() 
                source_idx = self.source_idx[source_id]

                while buffer_size > 0 and source_queue.size() > 0:
                    next_neighbor_id = source_queue.front().value 

                    if next_neighbor_id in self.visited:
                        buffer_size -= 1
                        source_queue.dequeue_front()
                        continue
                        
                    self.expand(source_queue, next_neighbor_id)
                    self.source_groups[source_id].add(next_neighbor_id) 
                    self.visited.add(next_neighbor_id)

                    source_queue.dequeue_front()
                    buffer_size -= 1 
    
    
    def expand(self, source_queue, neighbor_id): 
        neighbors = self.polygon_graph.neighbors[neighbor_id] 
        for neighbor_id in neighbors: 
            if neighbor_id in self.visited: 
                continue 
            else: 
                source_queue.enqueue_back(neighbor_id)

    def get_buffer_size(self):
        buffer_size = None
        if self.sampling_mode == "uniform": 
            if self.min_buffer == self.max_buffer:
                buffer_size = self.min_buffer
            else: 
                buffer_size = random.randint(
                    self.min_buffer, self.max_buffer
                ) 
        elif self.sampling_mode == "normal": 
            buffer_size = max(
                1, 
                int(numpy.random.normal(
                    self.ave_buffer, self.std_dev_buffer
                ))
            ) 
        return buffer_size

    def merge_polygons(self):
        for source_id in self.source_groups: 
            polygon_ids = self.source_groups[source_id]
            polygons = [] 
            for polygon_id in polygon_ids: 
                polygon = self.polygon_graph.polygons[polygon_id]
                polygon_ = shapely.Polygon(polygon)
                polygons.append(polygon_) 
            union = shapely.unary_union(polygons) 
            self.merged_polygons[source_id] = list(union.exterior.coords)  

    def remove_holes(self):
        # create tree 
        bboxes = []
        indexer = []

        for group_id in self.merged_polygons:
            polygon = self.merged_polygons[group_id] 
            polygon_ = shapely.Polygon(polygon) 
            bounds = polygon_.bounds 
            bbox = shapely.box(*bounds)
            bboxes.append(bbox) 
            indexer.append(group_id)

        self.tree = shapely.STRtree(bboxes) 

        # find hole polygons 
        to_delete = set()

        for inner_id in self.merged_polygons: 
            inner_poly = self.merged_polygons[inner_id] 
            inner_poly_ = shapely.Polygon(inner_poly)

            for i in self.tree.query(inner_poly_, predicate="intersects"): 

                outer_id = indexer[i]

                if inner_id == outer_id: 
                    continue

                outer_poly = self.merged_polygons[outer_id]
                outer_poly_ = shapely.Polygon(outer_poly) 

                if outer_poly_.contains(inner_poly_): 
                    to_delete.add(inner_id) 


        # delete hole polygons
        for inner_id in to_delete:  
            del self.merged_polygons[inner_id]
            
    def get_merged_polygons(self): 
        return list(self.merged_polygons.values())

    def clean_up(self): 
        self.source_groups = None