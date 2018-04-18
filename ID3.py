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
  # print examples
  list_of_attributes = getAttributes(examples)
  if not examples:
      leaf = Node()
      leaf.label = default
  elif same_classification(examples) != None or only_trivial(examples, list_of_attributes):
      # print(only_trivial(examples, list_of_attributes))
      leaf = Node()
      leaf.label = mode_attr(examples, 'Class')

  else:
      best = pick_best_attribute(examples, list_of_attributes)
      leaf = Node()
      leaf.name = best
      # print("Split at ", best)
      leaf.mode = mode_attr(examples, 'Class')
      split = getDict(examples, best)
      for key in split.keys():
        subtree = ID3(split[key], mode_attr(examples, 'Class'))
        leaf.children[key] = subtree
        leaf.children[key].parent = leaf

  # print(leaf.name, leaf.label)

  return leaf


def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''
  # leaves = bottom_seek(node)
  # leaflist = []
  # for i in leaves:
  #   leaflist.append(i.name)
  # print(leaflist)
  # return node
  # print("NO")
  bestacc = test(node,examples)
  # print("Original accuracy is ", bestacc)
  if bestacc == 1:
    # print("SEE YA")
    # print("Validation set is 1!")
    return bestacc

  bestnode = node
  # print("bestacc is ", bestacc)
  # print("Original Accuracy is ", bestacc)
  attempt = prune_helper(node, examples, bestacc)
  # if attempt != -100:
    # print("Attempted pruning acc is ", attempt[0])
  if attempt == -100:
    return bestnode
  else:
    if attempt[0] == 1:
      return attempt[1]
    return attempt[1]
    print("NO PASS")
    prune_helper(bestnode, examples, bestacc)

def prune_helper(node, examples, bestacc):
  leaves = bottom_seek(node)
  if leaves == None:
    # print("No more leaves")
    return -100
  leaflist = []
  for i in leaves:
    leaflist.append(i.name)
  # print("bottom seeked leaves are ", leaflist)
  # print("Going through leaves: ", leaflist)
  return gothroughleaves(leaves, node, examples, bestacc)

def gothroughleaves(lol, currnode, examples, bestacc):
  if lol == []:
    # print("Done going through leaves")
    return -100

  for leaf in lol:
    # print ("Popping ", leaf.name)
    storename = leaf.name
    storelabel = leaf.label
    leaf.name = None
    leaf.label = leaf.mode

    result = [test(currnode, examples), currnode]
    # print("Tested pruned accuracy is ", result[0])
    # print("---------")
    # print(result[0])
    # print(storename)
    # print("bestacc is ", bestacc)
    if result[0] <= bestacc:
      leaf.name = storename
      leaf.label = storelabel
      # print(leaf.name)
      del lol[0]
      return gothroughleaves(lol, currnode, examples, bestacc)
    else:
      # print ("Pruning was better, new acc is: ", result[0])
      return result


def bottom_seek(node):
  leaves = []
  seeker(node, leaves)
  # print("Leaves are ", leaves)
  # print(leaves)
  return leaves

def seeker(node, leaves):
  if node.label != None:
    return leaves
  if check_if_children_are_leafs(node) and node.label == None:
    leaves.append(node)
  else: 
    nextnodes = []
    for key in node.children.keys():
      if node.children[key].name != None:
        nextnodes.append(node.children[key])

    for node in nextnodes:
      seeker(node, leaves)

def pop_node(node):
  node.name = None
  node.children = {}
  node.label = node.mode
  node.mode = None
  return node

def check_if_children_are_leafs(node):
    all_children = len(node.children.keys())
    counter = 0;
    if node.children:
        for child in node.children.keys():
            if node.children[child].label != None:
                counter += 1
    return all_children == counter

def main():
  # prune(ID3([dict(x1=0, x2=0, x3=1, Class=0),
  #         dict(x1=0, x2=1, x3=1, Class=0),
  #         dict(x1=1, x2=0, x3=1, Class=1),
  #         dict(x1=1, x2=1, x3=1, Class=0)], 0), [dict(x1=1, x2=0, x3=1, Class=0)])

  # bottom_seek(ID3([dict(x1=1, x2=0, x3=0, Class=1),
  #         dict(x1=0, x2=1, x3=0, Class=0),
  #         dict(x1=1, x2=1, x3=0, Class=0),
  #         dict(x1=1, x2=0, x3=1, Class=1)], 0))
  # bottom_seek(ID3([dict(x1=1, x2=0, x3=0, Class=1),
  #         dict(x1=0, x2=1, x3=0, Class=0),
  #         dict(x1=1, x2=1, x3=0, Class=1),
  #         dict(x1=1, x2=0, x3=0, Class=1),
  #         dict(x1=0, x2=1, x3=1, Class=0),
  #         dict(x1=1, x2=0, x3=1, Class=0)], 0))
  # print(ID3([dict(x1=1, x2=0, x3=0, Class=1),
  #            dict(x1=0, x2=1, x3=0, Class=0),
  #            dict(x1=1, x2=1, x3=0, Class=1),
  #            dict(x1=1, x2=0, x3=0, Class=1)], 'default'))
  #print(getH([6,2]))
  # print(getEntropy([[0],[1],[1],[1],[0],[1],[1],[1]]))
  # print(getEntropy([[0],[0],[1],[1],[0],[1],[1],[0]]))
  # print(getEntropy([[0], [1]]))

  # tree = ID3([dict(x1=0, x2=1, x3=0, x4=? , Class=0),
  #         dict(x1=0, x2=1, x3=0, x4=? ,  Class=),
  #         dict(x1=0, x2=0, x3=1, x4=0 ,  Class=),
  #         dict(x1=0, x2=0, x3=0, x4=? ,  Class=),
  #         dict(x1=0, x2=0, x3=1, x4=1 ,  Class=),
  #         dict(x1=1, x2=0, x3=0, x4=0 ,  Class=),
  #         dict(x1=1, x2=1, x3=0, x4=? ,  Class=),
  #         dict(x1=1, x2=0, x3=0, x4=1 ,  Class=),
  #         dict(x1=1, x2=1, x3=1, x4=? ,  Class=)], 0)

  data = [dict(x1=0, x2=1, x3=0, x4=1 , Class=0),
          dict(x1=0, x2=1, x3=0, x4=0 ,  Class=0),
          dict(x1=0, x2=0, x3=1, x4=0 ,  Class=1),
          dict(x1=0, x2=0, x3=0, x4=1 ,  Class=1),
          dict(x1=0, x2=0, x3=1, x4=1 ,  Class=1),
          dict(x1=1, x2=0, x3=0, x4=0 ,  Class=0),
          dict(x1=1, x2=1, x3=0, x4=0 ,  Class=0),
          dict(x1=1, x2=0, x3=0, x4=1 ,  Class=0),
          dict(x1=1, x2=1, x3=1, x4=0 ,  Class=1)]

  tree = ID3(data, 0)
  # print("Testing tree with training examples: ", test(tree, data))
  leaves = bottom_seek(tree)
  leaflist = []
  for i in leaves:
    leaflist.append(i.name)
  # print(leaflist)
  validationData = [dict(x1=0, x2=1, x3=0, x4=0 ,  Class=1)]
  prune(tree, validationData)
  print("Testing pruned tree with validation data: ", test(tree, validationData))
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


def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  examples = preprocessing(examples) # preprocess the examples
  total_length = len(examples)
  amount_correct = float(0);
  for example in examples:
      correct_class = example['Class']
      del example['Class']
      if evaluate(node, example) == correct_class:
          amount_correct = amount_correct + 1
      example['Class'] = correct_class
  return amount_correct/total_length

def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  current_node = node
  while current_node.children != {} and current_node.label == None and current_node.name != "Class":
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
        value_list = each.values()
        if "?" in value_list:
            parsed_list = list(filter(lambda x: x !="?", value_list))
            if parsed_list:
                if len(parsed_list) == 1:
                    mode_value = "y"
                else:
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
    # print return_list
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

  vals = count_obj.values()

  # print(both)

  tot = float(tot)

  h = 0
  if 0 in vals: return 0 #is this right?
  else:
    for each in vals:
      h = h + (each/tot)*(math.log((each/tot), len(vals))) #is it still log2??? (CHECK LATER)
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

      # elif currdict.keys() == [0]:
      #   # print('Split on ', attribute, 'is trivial')
      #   continue

      # elif currdict.keys() == [1]:
      #   # print('Split on ', attribute, 'is trivial')
      #   continue

    # print('Splitting at ' + best)
    return best

def only_trivial(data_set, attribute_metadata):
  flag = True
  for attribute in attribute_metadata:
      # print('INSIDE ATTRIBUTE', attribute)
      currdict = getDict(data_set, attribute)
      if len(currdict.keys()) > 1:
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
