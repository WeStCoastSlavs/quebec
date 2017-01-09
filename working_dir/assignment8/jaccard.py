def calc_jaccard_simmilarity(wordset1, wordset2):
    intersetion_cardinality = len(set.intersection(wordset1, wordset2))
    union_cardinality = len(set.union(wordset1, wordset2))
    return intersetion_cardinality/float(union_cardinality)