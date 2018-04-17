from node import Node
import math
from collections import Counter



def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''

  best = 'x1'

  newnode = Node()
  newnode.label = best

  return getDict(examples, best)



def main():
  # print(ID3([dict(x1=1, x2=0, x3=0, Class=1),
  #            dict(x1=0, x2=1, x3=0, Class=0),
  #            dict(x1=1, x2=1, x3=0, Class=1),
  #            dict(x1=1, x2=0, x3=0, Class=1)], 'default'))
  #print(getH([6,2]))
  # print(getEntropy([[0],[1],[1],[1],[0],[1],[1],[1]]))
  # print(getEntropy([[0],[0],[1],[1],[0],[1],[1],[0]]))
  # print(getEntropy([[0], [1]]))
  
  data = [dict(x1=1, x2=0, x3=0, Class=1),
          dict(x1=0, x2=1, x3=0, Class=0),
          dict(x1=1, x2=1, x3=0, Class=1),
          dict(x1=1, x2=0, x3=0, Class=1),
          dict(x1=0, x2=1, x3=1, Class=0)]

  data1 = [dict(x1=0, x2=0, Class=0),
          dict(x1=0, x2=0,  Class=0),
          dict(x1=0, x2=0,  Class=0),
          dict(x1=0, x2=1,  Class=1),
          dict(x1=0, x2=1,  Class=1),
          dict(x1=0, x2=1,  Class=1),
          dict(x1=1, x2=1,  Class=1),
          dict(x1=1, x2=1,  Class=1),
          dict(x1=1, x2=0,  Class=1)]
  attributes = getAttributes(data1)

  print(pick_best_attribute(data1, attributes))

def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''

# def getH(example_array): # returns Entropy for examples
#   tot = 0
#   for each in example_array:    #get number of examples in split
#     tot = tot + each 

#   tot = float(tot)

#   h = 0

#   for each in example_array:
#     if each == 0: continue
#     else: h = h + (each/tot)*(math.log((each/tot), len(example_array)))
#   return -h

def getEntropy(data): # returns Entropy for examples
  count0 = 0
  count1 = 0
  for each in data:
    if each[0] == 0: count0 += 1
    elif each[0] == 1: count1 += 1
    else:
      print('Error, data is not either 0 or 1')
      return -1
  tot = float(len(data))

  both = [count0, count1]
  # print(both)

  tot = float(tot)

  h = 0
  if count0 == 0 or count1 == 0: return 0
  else:
    for each in both:
      h = h + (each/tot)*(math.log((each/tot), 2))
  return -h


def mode(list):
  return max(set(list), key=list.count)

def getAttributes(examples): # returns list of all the different attributes found in examples
  attributes = []
  for each in examples:
    attributes.extend(each.keys())

  attributes = list(set(attributes))
  attributes.remove('Class')
  return attributes

def getValues(examples, attribute): # returns list of all the different values for attribute in examples
  vals = []
  for each in examples:
    vals.append(each[attribute])
  vals = list(set(vals))
  return vals

def getDict(examples, attribute): # returns dictionary {attr_value: list_of_examples}
  vals = getValues(examples, attribute)
  newdict = {}

  for val in vals:
    newdict[val] = []
  for each in examples:
    newdict[each[attribute]].append(each)

  return newdict

def pick_best_attribute(data_set, attribute_metadata):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    # Your code here
    best = None
    split0 = []
    split1 = []
    entropy = 0
    lowest_entropy = 999
    tot = float(len(data_set))
    # print('tot is', tot)


    for attribute in attribute_metadata:
      print('INSIDE ATTRIBUTE', attribute)
      newlist0 = []
      newlist1 = []
      currdict = getDict(data_set, attribute)
      if currdict.keys() == [0, 1] or currdict.keys() == [1, 0]:
        split0 = currdict[0]
        split1 = currdict[1]
        # print('We have 2 dicts')

        for each in split0:
          newlist0.append([each['Class']])

        for each in split1:
          newlist1.append([each['Class']])

        print('newlist0 is', newlist0, 'newlist1 is', newlist1)
        entropy = (len(newlist0)/tot) * getEntropy(newlist0) + (len(newlist1)/tot)*getEntropy(newlist1)
        print('Entropy of ', attribute, 'is', entropy)
        if entropy < lowest_entropy:
          lowest_entropy = entropy
          best = attribute

      elif currdict.keys() == [0]:
        print('Split on ', attribute, 'is trivial')
        continue

      elif currdict.keys() == [1]:
        print('Split on ', attribute, 'is trivial')
        continue

      else:
        print('ERROR NO CURRDICT')
        return -1

    return best



def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the output value (index 0) is the same for all examples in the the data_set, if so return that output value, otherwise return None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
     '''
    # Your code here
    pass
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

main()
