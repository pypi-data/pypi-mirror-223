#
# gep.misc.indexify 
# :: indexifies items starting from 0

def indexify(items): 
    dic = {} 
    for i in range(0, len(items)):
        dic[i] = items[i - 1]
    return dic