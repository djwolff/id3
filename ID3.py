from node import Node
import math
from collections import Counter

N = [1,2,2,3,3,3,4,4,4,4,5,5,5,5,5]
C = Counter(N)

j = [ [k,]*v for k,v in C.items()]


def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''

  attributes = []
  for each in examples:
    attributes.extend(each.keys())

  attributes = list(set(attributes))

  best = 'x1'


  newnode = Node()
  newnode.label = best

  return getDict(examples, best)



def main():
  print(ID3([dict(x1=1, x2=0, x3=0, Class=1),
             dict(x1=0, x2=1, x3=0, Class=0),
             dict(x1=1, x2=1, x3=0, Class=1),
             dict(x1=1, x2=0, x3=0, Class=1)], 'default'))

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

def getH(example_array): # returns Entropy for examples
  tot = 0
  for each in example_array:    #get number of examples in split
    tot = tot + each 

  tot = float(tot)

  h = 0

  for each in example_array:
    if each == 0: continue
    else: h = h + (each/tot)*(math.log((each/tot), len(example_array)))
  return -h


def mode(list):
  return max(set(list), key=list.count)

def getAttributes(examples): # returns list of all the different attributes found in examples
  attributes = []
  for each in examples:
    attributes.extend(each.keys())

  attributes = list(set(attributes))
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

main()
