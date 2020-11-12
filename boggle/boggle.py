#!/usr/bin/env python3
"""
Created on 4 Jan 2011

@author: Wei
"""

import click
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class Node:
    """
    class representing a single node in a boggle board
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.letter = ''
        self.neighbours = []
        
    def set_letter(self, letter):
        self.letter = letter
        
    def add_neighbour(self, a_node):
        self.neighbours.append(a_node)
        
    def __del__(self):
        pass
    

# solve boggle game
class Boggle:    
    # constructor, converts a two dimensional char-string board representation to nodes list
    def __init__(self, boardstr):
        if not self.is_square_board(boardstr):
            raise SystemExit("Not a square board given!")
        self.totalrows = len(boardstr)
        self.dict = []
        self.nodes = []
        self.boardLetterSet = set([])
        # maintain a list of visited nodes when searching
        # use a list instead of a O(1) hash/dict here for easier route trace,
        # since a word wouldn't be very long, O(nlogn) is not bad
        self.visited = []
        
        for row in range(0, self.totalrows):
            a_row = boardstr[row]
            row_nodes = []
            for col in range(0,self.totalrows):
                a_node = Node(row, col)
                a_node.set_letter(a_row[col])
                row_nodes.append(a_node)
                self.boardLetterSet.add(a_node.letter)
            self.nodes.append(row_nodes)

        # add each nodes neighbour nodes
        for row in range(0,self.totalrows):
            for col in range(0,self.totalrows):   
                for i in range(row-1, row+1+1):
                    for j in range(col-1, col+1+1):
                        # print(row,col,i,j)
                        if((0 <= i < self.totalrows) and (0 <= j < self.totalrows)
                           and ((not i == row) or (not j == col)) ):
                            self.nodes[row][col].add_neighbour(self.nodes[i][j])
    
    #  checks whether the given boardstr list is a square two dimensional list/array
    def is_square_board(self,boardstr):
        rows = len(boardstr)
        for row in boardstr:
            if not len(row)== rows:
                return False
        return True

    #  recursively search neighbours
    def find(self, node, word):
        if len(word) == 0:
            return True
        if len(word) == 1 and word == node.letter:
            self.visited.append(node)
            return True
        
        if node.letter == word[0]:
            neighbor_nodes = node.neighbours
            self.visited.append(node)
            word = word[1:]
            for n in neighbor_nodes:
                if n.letter == word[0] and (n not in self.visited):  #  and not visited
                    if self.find(n, word):
                        return True
                else:
                    pass
            del(self.visited[-1])    
            # del(self.visited[node])
        else:
            return False
        
    def contains(self, word):
        for row in range(0, self.totalrows):
            for col in range(0, self.totalrows):
                n = self.nodes[row][col]
                del(self.visited[0:])
                if self.find(n, word):
                    return self.visited
                    
        return None
    
    def load_dict(self, dict_file, min_len=1):
        with open(dict_file, 'r') as f:
            for line in f:
                w = line.lower().rstrip()
                ds = set(w)
                # we only add dictionary words with a minimum len AND
                # all of its characters are covered in this board
                if len(w) >= min_len and len(ds - self.boardLetterSet) == 0:
                    self.dict.append(w)

        # sort by word length 
        self.dict.sort(key=lambda x: len(x), reverse=True)
        logging.debug("%d words added to dict" % (len(self.dict)))


@click.command()
@click.option('-i', '--input_file', type=str, help='input file representing a boggle board', required=True)
@click.option('-d', '--dictionary_file', help='dictionary file to search against', required=True)
@click.option('-l', '--minimum_length', type=int, default=1, help='only return words longer than this')
def search(input_file, dictionary_file, minimum_length):
    board = []
    with open(input_file, 'r') as f:
        for line in f:
            row = list(line.strip().lower())
            board.append(row)

    b = Boggle(board)
    b.load_dict(dictionary_file, minimum_length)

    i = 0
    for word in b.dict:
        results = b.contains(word)
        if results:
            i += 1
            print(f'{i}:{word} path=', end='')
            for n in results:
                print(f"({n.x},{n.y})", sep='', end='')
            print()

    print(f'{i} words can be found in the boggle board')


if __name__ == '__main__':
    search()
