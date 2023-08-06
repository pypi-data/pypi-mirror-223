#
# gep.misc.comparators 
# :: Comparator functions considering tolerance.
#

DEFAULT_TOLERANCE = 0.0001

# --- FLOAT COMPARISON --- # 
def float_equals(v1, v2, tolerance = DEFAULT_TOLERANCE): 
    return abs(v1 - v2) < tolerance

def float_gt(v1, v2, tolerance = DEFAULT_TOLERANCE): 
    return v2 - v1 > tolerance 

def float_lt(v1, v2, tolerance = DEFAULT_TOLERANCE): 
    return v1 - v2 < tolerance

# --- POINT COMPARISON --- #
def point_equals(a, b, tolerance = DEFAULT_TOLERANCE):
    return float_equals(a[0], b[0], tolerance) and \
           float_equals(a[1], b[1], tolerance)

def point_comparator(a, b, tolerance = DEFAULT_TOLERANCE):
    if float_equals(a[0], b[0], tolerance): 
        return float_lt(a[1], b[1], tolerance) 
    else: 
        return float_lt(a[0], b[0], tolerance)

# --- EDGE COMPARISON --- #
def edge_equals(A, B, tolerance = DEFAULT_TOLERANCE): 
    return (
        point_equals(A[0], B[0], tolerance) and \
        point_equals(A[1], B[1], tolerance)
    ) 

def edge_comparator(A, B, tolerance = DEFAULT_TOLERANCE): 
    if point_equals(A[0], B[0]): 
        return point_comparator(A[1], B[1], tolerance)
    else: 
        return point_comparator(A[0], B[0], tolerance)