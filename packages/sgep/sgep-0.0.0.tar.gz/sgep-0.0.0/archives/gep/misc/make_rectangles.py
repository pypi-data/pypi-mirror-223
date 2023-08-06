

def make_rectangle(x, y, width, height): 
    return [
        (x, y),
        (x + width, y),
        (x + width, y + height), 
        (x, width + height)
    ]

def make_square(x, y, size):
    return make_rectangle(x, y, size, size)