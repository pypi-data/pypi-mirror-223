from dsap.bsts.structs.rbt import RBT
from gep.misc.comparators import *

class PointBST(RBT):
    def __init__(self): 
        self.tolerance = DEFAULT_TOLERANCE    

        RBT.__init__(self)

    def equals(self, a, b): 
        return point_equals(a.key, b.key, self.tolerance)

    def comparator(self, a, b): 
        return point_comparator(a.key, b.key, self.tolerance)

    
    

         