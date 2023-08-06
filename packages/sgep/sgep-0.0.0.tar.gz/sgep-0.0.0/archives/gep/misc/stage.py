#
# gep.misc.stage
# :: Helper class for drawing to SVG files. 
# 
import svgwrite

class Stage: 
    def __init__(self, *args, **kwargs):     
        self.layers = {
            "main" : {
                "index" : 0, 
                "items" : []
            }, 
            "background" : {
                "index" : float('-inf'), 
                "items" : []
            }
        }
        
        self.hidden_layers = set()
        self.size = kwargs.get("size", None)

        self.drawing = svgwrite.Drawing(*args, **kwargs)
        
    def set_background(self, color): 
        width = self.size[0]
        height = self.size[1] 

        polygon = [
            (0, 0), 
            (width, 0),
            (width, height),
            (0, height)
        ]

        self.draw_polygon(polygon, "background", fill=color)


    # ---- LAYER OPERATIONS ---- #
    def make_layer(self, layer, z_index, *args): 
        
        if layer in self.layers:
            raise Exception("Layer already exists.")

        self.layers[layer] = {
            "index" : 0, 
            "items" : []
        }   

    def remove_layer(self, layer): 
        del self.layers[layer] 

    def hide_all_layers(self): 
        self.hidden_layers = set(list(self.layers.keys())) 

    def show_all_layer(self): 
        self.hidden_layers = set() 

    def is_hidden(self, layer): 
        return layer in self.hidden_layers 

    def hide_layer(self, layer): 
        self.hidden_layers.add(layer) 

    def show_layer(self, layer): 
        if self.is_hidden(layer): 
            self.hidden_layers.remove(layer) 

    def move_to_top(self, layer): 
        self.layers[layer]["z_index"] = float("inf") 

    def has_layer(self, layer): 
        return layer in self.layers

    def draw_layer(self, layer): 
        layer = self.layers[layer]
        items = layer["items"]
        for item in items: 
            self.drawing.add(item)  

    # ---- MAIN OPERATIONS ---- #        
    def add(self, geom, layer = "main") :
        self.layers[layer]["items"].append(geom) 

    def save(self):   
        layers = self.layers
        sorted_layers = sorted(layers.items(), key=lambda x: x[1]["index"]) 

        for layer in sorted_layers: 
            self.draw_layer(layer[0])

        self.drawing.save()

    #  ---- DRAW SPECIFIC SHAPES ---- #

    def draw_point(self, coords, layer = "main", **kwargs):
        size = kwargs.get("size", 3) 
        color = kwargs.get("color", "grey") 
        point = self.drawing.circle(center=coords, r=size, fill=color)
        self.add(point)  
    
    def draw_polygon(self, polygon, layer = "main", **kwargs): 
        self.add(self.drawing.polygon(polygon, **kwargs))

    def draw_polygons(self, polygons, layer = "main", **kwargs): 
        for polygon in polygons: 
            self.draw_polygon(polygon, layer, **kwargs)

    def draw_points(self, points, layer = "main", **kwargs): 
        for point in points: 
            self.draw_point(point, layer, **kwargs)
 
    def draw_line(self, point_a, point_b, layer="main", **kwargs): 
        self.add(self.drawing.line(start=point_a, end=point_b, **kwargs))

    def draw_path(self, points, layer = "main", **kwargs): 
        for i in range(len(points) - 1): 
            j = (i + 1) % len(points) 
            
            a = points[i]
            b = points[j] 

            self.draw_line(a, b, layer, **kwargs)
            

        