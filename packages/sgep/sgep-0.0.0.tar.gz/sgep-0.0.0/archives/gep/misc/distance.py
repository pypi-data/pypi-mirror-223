#
# geom.misc.distance
# :: Distance computations for manhattan and euclidean mode.
#

def euclidean_distance(a, b): 
    A = a[0] - b[0]
    B = a[1] - b[1] 
    AA = A ** 2 
    BB = B ** 2 
    return (AA + BB) ** (1/2)

def manhattan_distance(a, b): 
    A = a[0] - b[0]
    B = a[1] - b[1] 
    return abs(A) + abs(B)