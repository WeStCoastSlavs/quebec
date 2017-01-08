import re 
df1["words"] = df1.text.apply(lambda x: set(re.findall("\w+",str(x))))
df1["word_list"] = df1.text.apply(lambda x: re.findall("\w+",str(x)))