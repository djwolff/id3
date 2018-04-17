from node import Node
import math
from collections import Counter
import copy
import random


def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node)
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  examples = preprocessing(examples)
  print examples
  list_of_attributes = getAttributes(examples)
  if not examples:
      leaf = Node()
      leaf.label = default
  elif same_classification(examples) != None or only_trivial(examples, list_of_attributes):
      leaf = Node()
      leaf.label = mode_attr(examples, 'Class')
  else:
      best = pick_best_attribute(examples, list_of_attributes)
      leaf = Node()
      leaf.name = best
      split = getDict(examples, best)
      for key in split.keys():
        subtree = ID3(split[key], mode_attr(examples, 'Class'))
        leaf.children[key] = subtree
  # print(leaf.name, leaf.label)

  return leaf





def main():
  # print(ID3([dict(x1=1, x2=0, x3=0, Class=1),
  #            dict(x1=0, x2=1, x3=0, Class=0),
  #            dict(x1=1, x2=1, x3=0, Class=1),
  #            dict(x1=1, x2=0, x3=0, Class=1)], 'default'))
  #print(getH([6,2]))
  # print(getEntropy([[0],[1],[1],[1],[0],[1],[1],[1]]))
  # print(getEntropy([[0],[0],[1],[1],[0],[1],[1],[0]]))
  # print(getEntropy([[0], [1]]))
  tree = ID3([dict(x1=1, x2=0, x3=0, Class=1),
          dict(x1=0, x2=1, x3=0, Class=0),
          dict(x1=1, x2=1, x3=0, Class=1),
          dict(x1=1, x2=0, x3=0, Class=1),
          dict(x1=0, x2=1, x3=1, Class=0),
          dict(x1=1, x2=0, x3=1, Class=0)], 0)
  # print(evaluate(tree, dict(x1=1, x2=1, x3=1)))

  # print(mode_attr([dict(x1=1, x2=0, x3=0, Class=1),
  #         dict(x1=0, x2=1, x3=0, Class=0),
  #         dict(x1=1, x2=1, x3=0, Class=1),
  #         dict(x1=1, x2=0, x3=0, Class=1),
  #         dict(x1=0, x2=1, x3=1, Class=0),
  #         dict(x1=1, x2=0, x3=0, Class=1)], 'x1'))

  # data = [dict(x1=1, x2=0, x3=0, Class=1),
  #         dict(x1=0, x2=1, x3=0, Class=0),
  #         dict(x1=1, x2=1, x3=0, Class=1),
  #         dict(x1=1, x2=0, x3=0, Class=1),
  #         dict(x1=0, x2=1, x3=1, Class=0)]

  # data1 = [dict(x1='?', x2=0, Class=0),
  #         dict(x1=1, x2='?',  Class=0),
  #         dict(x1='?', x2=1,  Class=0),
  #         dict(x1=0, x2='?',  Class=1),
  #         dict(x1=0, x2=1,  Class=1),
  #         dict(x1=0, x2=1,  Class=1),
  #         dict(x1=1, x2=1,  Class=1),
  #         dict(x1=1, x2=1,  Class=1),
  #         dict(x1=1, x2=0,  Class=1)]
  # attributes = getAttributes(data)

  # print(pick_best_attribute(data1, attributes))
  # print preprocessing(data1)

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
  total_length = len(examples)
  amount_correct = 0;
  for example in examples:
      correct_class = example['Class']
      del example['Class']
      if evaluate(node, example) == correct_class:
          amount_correct = amount_correct + 1
  return amount_correct/total_length

def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  current_node = node
  while current_node.label == None:
      decision = example[current_node.name]
      if current_node.children[decision]:
          current_node = current_node.children[decision]
      else:
          print("Something went wrong in the evaluate method oops -David")
          break
  return current_node.label

def preprocessing(example_list):
    return_list = example_list
    for z, each in enumerate(example_list):
        # Given a dictionary with missing values, return a dictionary of no missing valaues replaced by the mode of the dict.
        mode_value = 0
        return_dict = copy.deepcopy(each)
        class_value = return_dict.pop('Class', 0)
        return_dict = each
        value_list = each.values() # pop to take out the class value
        if '?' in value_list:
            parsed_list = list(filter(lambda x: x!="?", value_list))
            # print parsed_list
            if parsed_list:
                mode_value = mode(parsed_list) #if there is a split decision then it takes the first value.
                # find keys that need to replace the values
                for i, j in enumerate(value_list):
                    # print i
                    if j=="?":
                        return_dict[each.keys()[i]] = mode_value
            return_dict['Class'] = class_value
            return_list[z] = return_dict
        else:
            return_list[z] = each
    return return_list

def getEntropy(data, attr): # returns Entropy for examples
  count_obj = {}
  for each in attr:
      count_obj[each] = 0
  for each in data:
      for i, index in enumerate(attr):
          if each == attr[i]: count_obj[attr[i]] += 1
    # if each == 0: count0 += 1
    # elif each == 1: count1 += 1
    # else:
    #   print('Error, data is not either 0 or 1')
    #   return -1
  tot = float(len(data))

  all = count_obj.values()

  # print(both)

  tot = float(tot)

  h = 0
  if 0 in all: return 0
  else:
    for each in all:
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
    lowest_entropy = 999
    entropy = 0
    tot = float(len(data_set))
    # print('tot is', tot)

    for attribute in attribute_metadata:
      # print('INSIDE ATTRIBUTE', attribute)
      newobj = {}
      newlist = []
      currdict = getDict(data_set, attribute)
      if len(currdict.keys()) > 1:
        for i, key in enumerate(currdict.keys()):
            for each in currdict[key]:
                newlist.append(each['Class'])
            newobj[i] = newlist
            newlist = []

        # print newobj
        for key in newobj.keys():
            entropy = entropy + ((len(newobj[key])/tot) * getEntropy(newobj[key], currdict.keys()))
        # print('Entropy of ', attribute, 'is', entropy)
        if entropy < lowest_entropy:
          lowest_entropy = entropy
          best = attribute

      elif currdict.keys() == [0]:
        # print('Split on ', attribute, 'is trivial')
        continue

      elif currdict.keys() == [1]:
        # print('Split on ', attribute, 'is trivial')
        continue

    # print('Splitting at ' + best)
    return best

def only_trivial(data_set, attribute_metadata):
  flag = True
  for attribute in attribute_metadata:
      # print('INSIDE ATTRIBUTE', attribute)
      currdict = getDict(data_set, attribute)
      if currdict.keys() == [0, 1] or currdict.keys() == [1, 0]:
        flag = False
  # if flag == True: print("Only trivial splits")
  return flag


def same_classification(example_list):
    checker = example_list[0]['Class']
    same = True
    for dictionary in example_list[1:]:
        if checker != dictionary['Class']:
            same = False
            break
    if same:
        return checker
    else:
        return None

def mode_attr(examples, attr):
  l = []
  for each in examples:
    l.append(each[attr])
  return mode(l)


main()
