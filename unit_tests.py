import ID3, parse, random
import matplotlib.pyplot as plt

def testID3AndEvaluate():
  data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]
  tree = ID3.ID3(data, 0)
  if tree != None:
    ans = ID3.evaluate(tree, dict(a=1, b=0))
    if ans != 1:
      print "ID3 test failed."
    else:
      print "ID3 test succeeded."
  else:
    print "ID3 test failed -- no tree returned"

def testPruning():
  data = [dict(a=1, b=1, c=1, Class=0), dict(a=1, b=0, c=0, Class=0), dict(a=0, b=1, c=0, Class=1), dict(a=0, b=0, c=0, Class=1), dict(a=0, b=0, c=1, Class=0)]
  validationData = [dict(a=0, b=0, c=1, Class=1)]
  tree = ID3.ID3(data, 0)
  ID3.prune(tree, validationData)
  if tree != None:
    ans = ID3.evaluate(tree, dict(a=0, b=1, c=1))
    print ans
    if ans != 1:
      print "pruning test failed."
    else:
      print "pruning test succeeded."
  else:
    print "pruning test failed -- no tree returned."


def testID3AndTest():
  trainData = [dict(a=1, b=0, c=0, Class=1), dict(a=1, b=1, c=0, Class=1),
  dict(a=0, b=0, c=0, Class=0), dict(a=0, b=1, c=0, Class=1)]
  testData = [dict(a=1, b=0, c=1, Class=1), dict(a=1, b=1, c=1, Class=1),
  dict(a=0, b=0, c=1, Class=0), dict(a=0, b=1, c=1, Class=0)]
  tree = ID3.ID3(trainData, 0)
  fails = 0
  if tree != None:
    acc = ID3.test(tree, trainData)
    if acc == 1.0:
      print "testing on train data succeeded."
    else:
      print "testing on train data failed."
      fails = fails + 1
    acc = ID3.test(tree, testData)
    if acc == 0.75:
      print "testing on test data succeeded."
    else:
      print "testing on test data failed."
      fails = fails + 1
    if fails > 0:
      print "Failures: ", fails
    else:
      print "testID3AndTest succeeded."
  else:
    print "testID3andTest failed -- no tree returned."

# inFile - string location of the house data file
def testPruningOnHouseData(inFile, size):
  withPruning = []
  withoutPruning = []
  data = parse.parse(inFile)
  data = data[:size]
  for i in range(100):
    random.shuffle(data)
    train = data[:len(data)/2]
    valid = data[len(data)/2:3*len(data)/4]
    test = data[3*len(data)/4:]

    tree = ID3.ID3(train, 'democrat')
    acc = ID3.test(tree, train)
    # print "training accuracy: ",acc
    acc = ID3.test(tree, valid)
    # print "validation accuracy: ",acc
    acc = ID3.test(tree, test)
    # print "test accuracy: ",acc

    ID3.prune(tree, valid)
    acc = ID3.test(tree, train)
    # print "pruned tree train accuracy: ",acc
    acc = ID3.test(tree, valid)
    # print "pruned tree validation accuracy: ",acc
    acc = ID3.test(tree, test)
    # print "pruned tree test accuracy: ",acc
    withPruning.append(acc)
    tree = ID3.ID3(train+valid, 'democrat')
    acc = ID3.test(tree, test)
    # print "no pruning test accuracy: ",acc
    withoutPruning.append(acc)
  # print withPruning
  # print withoutPruning
  print "average with pruning",sum(withPruning)/len(withPruning)," without: ",sum(withoutPruning)/len(withoutPruning)
  return [sum(withPruning)/len(withPruning), sum(withoutPruning)/len(withoutPruning)]

def plot():
    with_prune_list = []
    without_prune_list = []
    x_axis = []
    average_with = []
    average_without = []
    for x in range(10, 300):
        if x % 10 == 0:
            for y in range(100):
                result = testPruningOnHouseData("house_votes_84.data", x)
                average_with.append(result[0])
                average_without.append(result[1])
            x_axis.append(x)
            with_prune_list.append(sum(average_with)/len(average_with))
            without_prune_list.append(sum(average_without)/len(average_without))
    plt.plot(x_axis, average_with, 'ro-')
    plt.plot(x_axis, average_without, 'go-')
    plt.legend(['With Pruning', 'Without Pruning'], loc=4)
    plt.axis([0, 300, 0, 1])
    plt.ylabel('Accuracy')
    plt.xlabel('Data size')
    plt.title('Plot of Accuracy and Data size')
    plt.show()

if __name__ == "__main__":
    # testID3AndEvaluate()
    # testPruning()
    # testID3AndTest()
    # testPruningOnHouseData("house_votes_84.data") # replace infile with the data filepath
    plot()
