#Generate program
file = open('program.py', 'w')
import Node
#open input file
data = [[]]
"""
IMPORTANT: Change this file path to change testing data 
"""
#gather data
for line in f:  
    line = line.strip(\"\\r\   
data.append(line.split(',')
data.remove([]
#input dictionary tree
tree = "%s" % str(tree))

attributes = "%s" % str(attributes)
count = 0
for entry in data:
    count += 1
#copy dictionary
    tempDict = tree.copy()

#generate actual tree
while(isinstance(tempDict, dict)):
    root = Node.Node(tempDict.keys()[0], tempDict[tempDict.keys()[0]]
    tempDict = tempDict[tempDict.keys()[0]
#this must be attribute
    index = attributes.index(root.value
    value = entry[index
#ensure that key exists
    if(value in tempDict.keys())
    child = Node.Node(value, tempDict[value]
    result = tempDict[value
    tempDict = tempDict[value
#otherwise, break
    else
    print "can't process input %s"
    result = 
    brea
#print solutions 
    print (\"entry%s = %s\" % (count, result)
print "written program"
