my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]


# Divides a set on a specific column. Can handle numeric or nominal values
def divideset(rows, column, value):
    # Make a function that tells us if a row is in the first group (true) or the second group (false)
    split_function = None
    if isinstance(value, int) or isinstance(value, float):  # check if the value is a number i.e int or float
        split_function = lambda row: row[column] >= value
    else:
        split_function = lambda row: row[column] == value

    # Divide the rows into two sets and return them
    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return (set1, set2)
# Create counts of possible results (the last column of each row is the result)
def uniquecounts(rows):
   results={}
   for row in rows:
      # The result is the last column
      r=row[len(row)-1]
      if r not in results: results[r]=0
      results[r]+=1
   return results

# Entropy is the sum of p(x)log(p(x)) across all
# the different possible results
def entropy(rows):
   from math import log
   log2=lambda x:log(x)/log(2)
   results=uniquecounts(rows)
   # Now calculate the entropy
   ent=0.0
   for r in results.keys():
      p=float(results[r])/len(rows)
      ent=ent-p*log2(p)
   return ent

class decisionnode:
  def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
    self.col=col
    self.value=value
    self.results=results
    self.tb=tb
    self.fb=fb

def buildtree(rows, scoref=entropy):  # rows is the set, either whole dataset or part of it in the recursive call,

    # scoref is the method to measure heterogeneity. By default it's entropy.


    if len(rows) == 0: return decisionnode()  # len(rows) is the number of units in a set
    current_score = scoref(rows)

    # Set up some variables to track the best criteria
    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1  # count the # of attributes/columns.
    # It's -1 because the last one is the target attribute and it does not count.
    for col in range(0, column_count):
        # Generate the list of all possible different values in the considered column
        global column_values  # Added for debugging
        column_values = {}
        for row in rows:
            column_values[row[col]] = 1
            # Now try dividing the rows up for each value in this column
        for value in column_values.keys():  # the 'values' here are the keys of the dictionnary
            (set1, set2) = divideset(rows, col, value)  # define set1 and set2 as the 2 children set of a division

            # Information gain
            p = float(len(set1)) / len(rows)  # p is the size of a child set relative to its parent
            gain = current_score - p * scoref(set1) - (1 - p) * scoref(set2)  # cf. formula information gain
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:  # set must not be empty
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)

    # Create the sub branches
    if best_gain > 0:
        trueBranch = buildtree(best_sets[0])
        falseBranch = buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0], value=best_criteria[1],
                            tb=trueBranch, fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))

def printtree(tree,indent=''):
   # Is this a leaf node?
    if tree.results!=None:
        print(str(tree.results))
    else:
        print(str(tree.col)+':'+str(tree.value)+'? ')
        # Print the branches
        print(indent+'T->', end=" ")
        printtree(tree.tb,indent+'  ')
        print(indent+'F->', end=" ")
        printtree(tree.fb,indent+'  ')
tree=buildtree(my_data)
printtree(tree)