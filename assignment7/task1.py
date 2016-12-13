
d1 = "this is a text about web science".split(" ")
d2 = "web science is covering the analysis of text corpora".split(" ")
d3 = "scientific methods are used to analyze webpages".split(" ")

# Get all the words in a corpus
sve = d1.copy()
sve.extend(d2)
sve.extend(d3)
sve = set(sve)


len(sve)


# Counting words in documents
def brojac(d1):
    d1_dic = {}
    for elem in sve:
#         print(elem)
        if elem in d1:
#             print(d1)
            d1_dic[elem] = 1
        else:
            d1_dic[elem] = 0
    return d1_dic
d1_dict = brojac(d1)
d2_dict = brojac(d2)
d3_dict = brojac(d3)

# Scalar product
def scalar(d1, d2):
    suma = 0
    for k,v in d1.items():
        suma += v * d2[k]
    return suma




from math import sqrt
def euclidian_len(d1):
    return sqrt(sum([v*v for k,v in d1.items()]))
def cosine(d1, d2):
    return (scalar(d1,d2)/(euclidian_len(d1)*euclidian_len(d2)))

print(cosine(d1_dict, d2_dict))
print(cosine(d1_dict, d3_dict))
print(cosine(d3_dict, d2_dict))