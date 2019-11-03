'''
Created on 4 Jan 2011

@author: Wei
'''
import math
import sys

class Node:
    '''
    class representing a single node in a boggle board
    '''

    def __init__(self,x,y):
        '''
        Constructor
        '''
        self.x = x
        self.y = y
        self.letter = ''
        self.neighbours = []
        
    def setLetter(self, letter):
        self.letter = letter
        
    def addNeighbour(self, aNode):
        self.neighbours.append(aNode)
        
    def __del__(self):
        pass
    

#solve boggle game
class Boggle:    
    #constructor, converts a two dimensional char-string board representation to nodes list
    def __init__(self, boardstr):
        if(not self.isSquareBoard(boardstr)):
            raise SystemExit("Not a square board given!")
        self.totalrows = len(boardstr)
        
        self.nodes = []
        self.boardLetterSet = set([])
        #maintain a list of visited nodes when searching
        #use a list instead of a O(1) hash/dict here for easier route trace,
        #since a word wouldn't be very long, O(nlogn) is not bad  
        self.visited = []
        
        for row in range(0,self.totalrows):
            aRow = boardstr[row]
            rowNodes = []
            for col in range(0,self.totalrows):
                aNode = Node(row,col)
                aNode.setLetter(aRow[col])
                rowNodes.append(aNode)
                self.boardLetterSet.add(aNode.letter)
            self.nodes.append(rowNodes)

        #add each nodes neighbour nodes
        for row in range(0,self.totalrows):
            for col in range(0,self.totalrows):   
                for i in range(row-1, row+1+1):
                    for j in range(col-1, col+1+1):
                        #print(row,col,i,j)
                        if((i >=0 and i< self.totalrows) and (j>=0 and j < self.totalrows) 
                           and ((not i == row) or (not j == col)) ):
                            self.nodes[row][col].addNeighbour(self.nodes[i][j])
                            
        
#        nList = self.nodes[2][1].neighbours
#        for n in nList:
#            print (n.letter)   
    
    #checks whether the given boardstr list is a square two dimensional list/array
    def isSquareBoard(self,boardstr):
        rows = len(boardstr)
        for row in boardstr:
            if(not len(row)== rows):
                return False
        return True
    
    
    #recursively search neighbours   
    def find(self, node, str):
        if(len(str)==0):
            return True
        if(len(str)==1 and str == node.letter):
            self.visited.append(node)
            return True
        
        if(node.letter == str[0]):
            neighborNodes = node.neighbours
            self.visited.append(node)
            str = str[1:]
            for n in neighborNodes:
                
                if(n.letter == str[0] and (n not in self.visited)):  # and not visited
                    if(self.find(n,str)):
                        return True
                else:
                    pass
            del(self.visited[-1])    
            #del(self.visited[node])
        else:
            return False
        
    def contains(self, word):
        for row in range(0,self.totalrows):
            for col in range(0,self.totalrows):
                n = self.nodes[row][col]
                del(self.visited[0:])
                if(self.find(n,word)):
                    return self.visited
                    
        return None
    
    def loadDict(self,dictFile,minLen=3):
        f = open(dictFile)
        self.dict = []
        
        for line in f:
            w = line.lower().rstrip();
            ds = set(w)
            #we only add dictionary words with a minimum len AND
            #all of its characters are covered in this board
            if(len(w)>=minLen and len(ds - self.boardLetterSet) == 0):
                self.dict.append(w)        
                #sort by length
        
        #sort by word length 
        self.dict.sort(key=lambda x: len(x),reverse=True)        
        #print(len(self.dict)," words added to dict")
            
input = sys.argv[1]

n = len(input)

sqrt = int(math.sqrt(n))

print ("n=", n)
board=[]

for i in range(0,sqrt):
    list = []
    for j in range(0,sqrt):
        list.append( input[i*sqrt+j] )
    board.append(list)
            
#board = [['d','a','t','e'],
#         ['a','r','r','i'],
#         ['u','f','o','e'],
#         ['l','e','t','s']]

b = Boggle(board)

dictFile = r"sowpods.txt"
b.loadDict(dictFile)

i=0  
for word in b.dict:        
        list = b.contains(word)
        if(not list == None):
            i+=1
            print(i,":",word," -> ",end='')   
            for n in list:
                print("(",n.x,",",n.y,")", sep='', end='')
            print()     
#print(b.contains2("armiger"))       
