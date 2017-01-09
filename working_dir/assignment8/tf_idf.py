words = df1.words.tolist()

all_words = [word for sets in words for word in sets]

doc_freq = Counter(all_words)


def tf_dict_to_tfidf(tf_dic):
    new_dic = {}
    for k,v in tf_dic.items():
        new_dic[k] = v / float(doc_freq[k])
    return new_dic
df1['tf_idf'] = df1.tf.apply(tf_dict_to_tfidf)