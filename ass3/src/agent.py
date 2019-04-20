#/usr/bin/python3
# Sample starter bot by Zac Partridge
# Contact me at z.partridge@unsw.edu.au
# 06/04/19
# Feel free to use this and modify it however you wish

import socket
import sys
import numpy as np

# a board cell can hold:
#   0 - Empty
#   1 - I played here X
#   2 - They played here O

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
s = [".","X","O"]
curr = 0 # this is the current board to play in


# print a row
# This is just ported from game.c
def print_boards_row(boards, a, b, c, i, j, k):
    print(" "+s[boards[a][i]]+" "+s[boards[a][j]]+" "+s[boards[a][k]]+" | " \
             +s[boards[b][i]]+" "+s[boards[b][j]]+" "+s[boards[b][k]]+" | " \
             +s[boards[c][i]]+" "+s[boards[c][j]]+" "+s[boards[c][k]])

# Print the entire board
# This is just ported from game.c
def print_boards(boards):
    print_boards_row(boards, 1,2,3,1,2,3)
    print_boards_row(boards, 1,2,3,4,5,6)
    print_boards_row(boards, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_boards_row(boards, 4,5,6,1,2,3)
    print_boards_row(boards, 4,5,6,4,5,6)
    print_boards_row(boards, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_boards_row(boards, 7,8,9,1,2,3)
    print_boards_row(boards, 7,8,9,4,5,6)
    print_boards_row(boards, 7,8,9,7,8,9)
    print()

# choose a move to play
def play():
    print_boards(boards)
    #start coding here

    alphabeta = AlphaBeta(boards)
    nextState = alphabeta.alpha_beta_search(boards)
    print(nextState)


    # just play a random move for now
    n = np.random.randint(1,9)
    while boards[curr][n] != 0:
        n = np.random.randint(1,9)

    # print("playing", n)
    place(curr, n, 1)
    return n

# place a move in the global boards
def place(board, num, player):
    global curr
    curr = num
    boards[board][num] = player

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []
   
    if command == "second_move":
        place(int(args[0]), int(args[1]), 2)
        return play()
    elif command == "third_move":
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), 1)
        # place their last move
        place(curr, int(args[2]), 2)
        return play()
    elif command == "next_move":
        place(curr, int(args[0]), 2)
        return play()
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()


##########################
###### MINI-MAX A-B ######
##########################
class GameState:
    def __init__(self, boards, depth):
        self.boards = boards
        self.depth = depth
        return




class AlphaBeta:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, boards):
        first_state = GameState(boards, 0)
        self.game_state = first_state
        self.game_tree = boards  # GameTree
        self.root = game_tree  # GameNode
        self.max_depth = 3
        return

    def alpha_beta_search(self, game_state):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity

        children = self.getChildren(game_state)
        best_state = None
        for state in children:
            value = self.min_value(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        print "AlphaBeta:  Utility Value of Root Node: = " + str(best_val)
        print "AlphaBeta:  Best State is: " + best_state.Name
        return best_state

    def max_value(self, node, alpha, beta):
        print "AlphaBeta-->MAX: Visited Node :: " + node.Name
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = -infinity

        children = self.getChildren(node)
        for state in children:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        print "AlphaBeta-->MIN: Visited Node :: " + node.Name
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity

        children = self.getChildren(node)
        for state in children:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value
    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def getChildren(self, game_state):
        global curr
        children = []
        board=curr
        boards = game_state.boards
        for i in range(1,9):
            if boards[board][i]==0:
                next_boards = boards.copy()
                next_boards[board][i] = 2
                children.append(next_boards)
        assert boards is not None
        return children

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0

    def getUtility(self, node):
        assert node is not None
        return node.value