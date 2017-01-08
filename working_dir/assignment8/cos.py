from math import sqrt
def euclidian_len(d1):
    return sqrt(sum([v*v for k,v in d1.items()]))

def scalar(d1, d2):
    suma = 0
    for k,v in d1.items():
        try:
            suma += v * d2[k]
        except KeyError:
            pass
    return suma

def calc_cosine_similarity(d1,d2):
    return (scalar(d1,d2)/(euclidian_len(d1)*euclidian_len(d2)))