from collections import Counter
df1['tf'] = df1.word_list.apply(lambda x: Counter(x))