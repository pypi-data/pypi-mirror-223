#
# EDGE CHAINING MODULE 
# 

from gep.structs.point_bst import PointBST
from gep.ei_detection import EI_Detector
from gep.misc.comparators import *

class EdgeChain: 
    def __init__(self, context): 
        self.track = []

        self.start = None 
        self.end   = None 

        self.a = None 
        self.b = None

        self.clockwise = False

        self.polygon_ids = set()
        self.polygon_id = {} 
        
        self.context = context

    def vertices(self):
        indices = [self.start] + self.track + [self.end] 
        return [ self.context.index_point[index] for index in indices ]

class EdgeChainer: 
    def __init__(self, polygons): 
        self.polygons = polygons
        
        self.point_index = PointBST() 
        self.index_point = {}
        self.point_id = 1 
        self.point_degrees = {}
        self.point_refs = PointBST()

        self.edges = set()
        
        self.multivertices = {}

        self.polygon_edge_chains = {}
        self.edge_chains = {}

        # normalize points
        self.normalize_points()

        # construct point index
        self.make_point_index()
        
        # find edge set
        self.find_edges()
        
        # find degrees of points
        self.find_point_degrees()
        
        # find multivertices
        self.find_multivertices()

        # find edge associated with each polygon
        self.find_edge_chains()

        # find chains of each polygon 
        self.find_polygon_edge_chains()

    def normalize_points(self):
        polygons = self.polygons 
        
        for polygon_id in polygons:
            points = polygons[polygon_id]
            if points[-1] == points[0]: 
                points.pop()

    def make_point_index(self):
        polygons = self.polygons 

        for polygon_id in polygons:
            points = polygons[polygon_id]

            for i in range(len(points)):
                point = points[i] 

                if self.point_index.find(point) is None:

                    self.point_index.insert(point, self.point_id)
                    self.index_point[self.point_id] = point
                    self.point_refs.insert(point, {})
                   
                    self.point_id += 1 

                self.point_refs.find(point).value[polygon_id] = i

    
    def find_edges(self): 
        polygons = self.polygons 

        for polygon_id in self.polygons: 
            points = self.polygons[polygon_id] 
            
            for i in range(len(points)): 
                j = (i + 1) % len(points) 

                # find endpoints of edges
                a = points[i]
                b = points[j]

                a_idx = self.point_index.find(a).value
                b_idx = self.point_index.find(b).value

                # normalize edges
                e = None 
                if a_idx < b_idx: 
                    e = (a_idx, b_idx) 
                else: 
                    e = (b_idx, a_idx) 

                # register edge 
                if e not in self.edges: 
                    self.edges.add(e) 
        
    def find_point_degrees(self): 
        for edge in self.edges: 
            a, b = edge 

            if a not in self.point_degrees:
                self.point_degrees[a] = 0 
            if b not in self.point_degrees: 
                self.point_degrees[b] = 0 

            self.point_degrees[a] += 1 
            self.point_degrees[b] += 1 
    
    def find_multivertices(self): 
        # find multivertices
        for point_id in self.point_degrees: 
            if self.point_degrees[point_id] > 2: 
                self.multivertices[point_id] = set() 

        # find polygons associated with multivertices
        polygons = self.polygons
        
        for polygon_id in polygons: 
            points = polygons[polygon_id]
            
            for point in points: 
                point_id = self.point_index.find(point).value
                if point_id in self.multivertices: 
                    self.multivertices[point_id].add(polygon_id)

    def find_edge_chains(self): 
        for multivertex in self.multivertices: 
            polygon_ids = self.multivertices[multivertex] 

            for polygon_id in polygon_ids:
                polygon = self.polygons[polygon_id]
                mv_point = self.index_point[multivertex]
                mv_index = self.point_refs.find(mv_point).value[polygon_id]
                self.find_backward_chain(polygon_id, mv_index) 
                self.find_forward_chain(polygon_id, mv_index)


    def find_backward_chain(self, polygon_id, mv_index): 
        # find chain info
        poly = self.polygons[polygon_id] 

        start_id = self.point_index.find(poly[mv_index]).value  
        end_id = None  
        a = None 
        b = start_id 
        tl = 1
        track = [start_id]

        l = len(poly) 
        t = 0 
        current_id = mv_index - 1
        while t < l: 
            idx = current_id % l             
            point_index = self.point_index.find(poly[idx]).value 
            
            track.append(point_index)
            tl += 1

            if a is None:
                a = point_index 
            
            if point_index in self.multivertices:
                end_id = point_index

                break

            b = point_index 

            t += 1
            current_id -= 1

        # register chain 
        SE  = (start_id, end_id) 
        AB  = (a, b)
        rSE = (end_id, start_id)
        rAB = (b, a)

        already_exists = False

        # add polygon to reverse chain if chain already exists
        if self.has_edge_chain(rSE, rAB): 
            edge_chain = self.edge_chains[rSE][rAB]
            edge_chain.polygon_ids.add(polygon_id)
            already_exists = True
        
        # add polygon to chain if chain already exists
        if self.has_edge_chain(SE, AB): 
            edge_chain = self.edge_chains[SE][AB]
            edge_chain.polygon_ids.add(polygon_id)
            already_exists = True

        # register new chain
        if not already_exists:
            edge_chain = EdgeChain(self)
            edge_chain.start = end_id 
            edge_chain.end = start_id 
            edge_chain.ab = rAB
            edge_chain.polygon_ids = set([polygon_id])
            edge_chain.polygon_id = polygon_id
            edge_chain.track = track[::-1][1:-1] 
            
            if rSE not in self.edge_chains: 
                self.edge_chains[rSE] = {} 

            self.edge_chains[rSE][rAB] = edge_chain

    def find_forward_chain(self, polygon_id, mv_index): 
        # find chain info
        poly = self.polygons[polygon_id] 

        start_id = self.point_index.find(poly[mv_index]).value  
        end_id = None  
        a = None 
        b = start_id 
        tl = 1
        track = [start_id]

        l = len(poly) 
        t = 0 
        current_id = mv_index + 1
        while t < l: 
            idx = current_id % l             
            point_index = self.point_index.find(poly[idx]).value 
            
            track.append(point_index)
            tl += 1

            if a is None:
                a = point_index 
            
            if point_index in self.multivertices:
                end_id = point_index
                
                break
            
            b = point_index 

            t += 1
            current_id += 1

        # register chain 
        SE  = (start_id, end_id) 
        AB  = (a, b)
        rSE = (end_id, start_id)
        rAB = (b, a)

        polygon_ids = None 

        # remove backward chain if it already exists
        if self.has_edge_chain(rSE, rAB): 
            polygon_ids = self.edge_chains[rSE][rAB].polygon_ids
            del self.edge_chains[rSE][rAB]
        
        # remove already existing chain
        if self.has_edge_chain(SE, AB): 
            polygon_ids = self.edge_chains[SE][AB].polygon_ids
            del self.edge_chains[SE][AB]

        # register chain
        polygon_ids.add(polygon_id)
       
        edge_chain = EdgeChain(self)
        edge_chain.start = start_id 
        edge_chain.end = end_id 
        edge_chain.ab = AB
        edge_chain.polygon_id = polygon_id
        edge_chain.polygon_ids = polygon_ids 
        edge_chain.track = track[1:-1] 
        
        if SE not in self.edge_chains: 
            self.edge_chains[SE] = {} 
        
        self.edge_chains[SE][AB] = edge_chain 

    def find_polygon_edge_chains(self):
        polygons = self.polygons 

        for polygon_id in polygons:
            self.polygon_edge_chains[polygon_id] = []

            points = polygons[polygon_id]
            l = len(points)

            # find the index of the first multivertex
            mv_index = 0
            for i in range(len(points)): 
                point_index = self.point_index.find(points[i]).value 
                if point_index in self.multivertices: 
                    mv_index = i
                    break 

            
            # loop through the polygon once to find vertex chain 
            last_mv = self.point_index.find(points[mv_index]).value 
            a = None
            b = None
            d = 1 
            for i in range(l + 1): 
                idx = (mv_index + i + 1) % l

                point_index = self.point_index.find(points[idx]).value
                
                d += 1

                if a is None: 
                    a = point_index 

                if point_index in self.multivertices: 
                    
                    if d == 2:
                        a = point_index 
                        b = last_mv

                    chain = ((last_mv, point_index), (a, b))
                    self.polygon_edge_chains[polygon_id].append(chain)
                    last_mv = point_index
                    a = None 

                b = point_index


    def edge_chain(self, SE, AB):
        return self.edge_chains[SE][AB]

    def has_edge_chain(self, SE, AB):
        if SE in self.edge_chains: 
            if AB in self.edge_chains[SE]: 
                return True 
        return False  

    def polygon_vertices(self, polygon_id): 
        polygon_edge_chains = self.polygon_edge_chains[polygon_id]

        for edge_chain in polygon_edge_chains: 
            SE, AB = edge_chain 
            rSE, rAB = (SE[1], SE[0]), (AB[1], AB[0])

            if self.has_edge_chain(SE, AB): 
                edge_chain_obj = self.edge_chain(SE, AB)

                yield self.index_point[edge_chain_obj.start]

                for vertex_id in edge_chain_obj.track: 
                    yield self.index_point[vertex_id]

            elif self.has_edge_chain(rSE, rAB):
                edge_chain_obj = self.edge_chain(rSE, rAB)

                yield self.index_point[edge_chain_obj.end]

                for vertex_id in reversed(edge_chain_obj.track):
                    yield self.index_point[vertex_id]

            else:
                raise Exception(
                    f"Cannot find edge chain {SE} {AB} of {polygon_id}."
                )

    def all_edge_chains(self): 
        for edge_chain in self.edge_chains: 
            for adjacent in self.edge_chains[edge_chain]:
                edge_chain_obj = self.edge_chains[edge_chain][adjacent]
                yield edge_chain_obj  
    
    def patch_edge_chain(self, edge_chain, points):
    
        track = edge_chain.track

        # register points 
        for point in points: 
            self.point_index.insert(point, self.point_id)
            self.index_point[self.point_id] = point
            self.point_id += 1

        SE = (edge_chain.start, edge_chain.end)
        AB = edge_chain.ab
        rSE = (edge_chain.end, edge_chain.start)
        rAB = (AB[1], AB[0]) 

        a = self.point_index.find(points[0]).value
        b = self.point_index.find(points[-1]).value

        edge_chain.track = [
            self.point_index.find(point).value for point in points
        ]

        # delete points 
        for vertex_id in track:
            point = self.index_point[vertex_id]
            self.point_index.delete(point)  
            del self.index_point[vertex_id]

     
    def edge_chain_info(self): 
        for edge_chain in self.edge_chains: 
            for adjacent in self.edge_chains[edge_chain]:
                edge_chain_obj = self.edge_chains[edge_chain][adjacent]
                print(edge_chain, adjacent, list(edge_chain_obj.track), 
                      edge_chain_obj.polygon_id, edge_chain_obj.polygon_ids)

  
    def find_outer_edge_chains(self): 
        ei_detector = EI_Detector(self.polygons) 

        outer_edge_chains = set()

        for edge_chain in self.all_edge_chains(): 
            vertices = list(edge_chain.vertices())

            for i in range(len(vertices) - 1): 
                j = (i + 1) % len(vertices) 
                
                point_a = vertices[i]
                point_b = vertices[j] 
                
                e = None 

                a_id = ei_detector.vertex_id.find(point_a).value 
                b_id = ei_detector.vertex_id.find(point_b).value 

                if a_id < b_id: 
                    e = (a_id, b_id)
                else: 
                    e = (b_id, a_id)

                if e in ei_detector.outer_edges: 
                    outer_edge_chains.add(edge_chain) 

        return outer_edge_chains

    def find_inner_edge_chains(self): 
        outer_edge_chains = self.find_outer_edge_chains()
        inner_edge_chains = set()
        for edge_chain in self.all_edge_chains(): 
            if edge_chain not in outer_edge_chains: 
                inner_edge_chains.add(edge_chain)
        return inner_edge_chains