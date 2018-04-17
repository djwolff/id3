from node import Node
import math

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node)
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  list_of_attributes = all_attributes(examples)
  if not examples:
      leaf = Node()
      leaf.value = default
      return leaf
  elif same_classification(examples) != None:
      leaf = Node()
      leaf.label = mode(examples)
      return leaf
  else:
      best = pick_best_attribute(examples, list_of_attributes)

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

def all_attributes(example_list):
    attributes = []
  for each in examples:
    attributes.extend(each.keys())

  attributes = list(set(attributes))
  attributes.remove('Class')
  return attributes

def pick_best_attribute(example_list, all_attributes):
    max_gain = 0
    best_attr = 0
    for attr in all_attributes:
        gain_ratio




def same_classification(example_list):
    checker = example_list[0][Class]
    same = true
    for dictionary in example_list[1:]:
        if checker != dictionary['Class']
            same = false
            break
    if same:
        return None
    else:
        return checker


def entropy(data_set):
    tot = 0
    for each in data_set
        tot = tot + each
    tot = float(tot)
    h = 0
    for each in data_set:
        if each == 0: continue
        else: h = h + (each/tot)*(math.log((each/tot), len(data_set)))
    return -h

def mode(list):
    return max(set(list), key=list.count)
