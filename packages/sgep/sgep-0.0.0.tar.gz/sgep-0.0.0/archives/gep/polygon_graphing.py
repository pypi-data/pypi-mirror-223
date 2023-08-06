#
# POLYGON GRAPHING MODULE
#


from gep.structs.point_bst import PointBST

class PolygonGraph: 
    def __init__(self, polygons): 
        self.polygons = polygons 
        self.tolerance = 0.0001

        self.index_point = {}
        self.vertex_polygons = {}

        self.point_index = PointBST()

        self.edge_polygons = {}
        self.neighbors = {}
        
        self.vertex_id = 1


    def register_points_and_vertices(self, ): 
        polygons = self.polygons

        # register polygons and vertices
        for polygon_id in polygons: 
            polygon = polygons[polygon_id] 
            for point in polygon:
                # register new point 
                vertex_id = self.vertex_id
                if self.point_index.find(point) is None: 
                    self.index_point[vertex_id] = point  
                    self.point_index.insert(point, vertex_id)
                    self.vertex_id += 1 
                else: 
                    vertex_id = self.point_index.find(point).value

                # record point presence in polygon 
                if vertex_id not in self.vertex_polygons:
                    self.vertex_polygons[vertex_id] = set() 
                self.vertex_polygons[vertex_id].add(polygon_id)

    def register_edges(self): 
        polygons = self.polygons 
        
        for polygon_id in polygons:
            polygon = polygons[polygon_id]

            for i in range(len(polygon)): 
                # identify edge
                j = (i + 1) % len(polygon) 
                point_i = polygon[i] 
                point_j = polygon[j] 
                a = self.point_index.find(point_i).value 
                b = self.point_index.find(point_j).value
                e = None 
                norm = False 

                
                # normalize edge
                if a < b: 
                    e = (a, b)
                else: 
                    e = (b, a)
                    norm = True 
                
                # register edge if needed
                if e not in self.edge_polygons: 
                    self.edge_polygons[e] = set() 

                # add polygon to edge
                self.edge_polygons[e].add(polygon_id)

    def make_point_adjacencies(self, **kwargs): 
        polygons = self.polygons 
        check = kwargs.get("check", None)

        # for each polygon, find the union 
        for polygon_id in polygons: 
            polygon = polygons[polygon_id] 

            self.neighbors[polygon_id] = {}

            for point in polygon: 
                vertex_id = self.point_index.find(point).value
                vertex_polygons = self.vertex_polygons[vertex_id] 
                for neighbor_id in vertex_polygons: 
                    if neighbor_id == polygon_id: 
                        continue 
                    if check and not check(self): 
                        continue
                    self.neighbors[polygon_id][neighbor_id] = 1

    def make_edge_adjacencies(self, constraint = 0.0001, **kwargs): 
        polygons = self.polygons 
        check = kwargs.get("check", None)

        self.register_points_and_vertices()
        self.register_edges()

        # for each polygon, find the union 
        for polygon_id in polygons: 
            polygon = polygons[polygon_id] 

            self.neighbors[polygon_id] = {}
            
            for i in range(len(polygon)): 
                # identify edge
                j = (i + 1) % len(polygon) 
                point_i = polygon[i] 
                point_j = polygon[j] 
                a = self.point_index.find(point_i).value
                b = self.point_index.find(point_j).value
                e = None 
                norm = False 
                
                # normalize edge
                if a < b: 
                    e = (a, b)
                else: 
                    e = (b, a)

          
                # find neighbors of edges 
                if e not in self.edge_polygons: 
                    continue

                for neighbor_id in self.edge_polygons[e]: 
                    if neighbor_id == polygon_id: 
                        continue
                    if check and not check(self): 
                        continue
                    self.neighbors[polygon_id][neighbor_id] = 1

