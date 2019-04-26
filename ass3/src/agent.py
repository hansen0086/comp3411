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
max_depth = 4

# print a row. | . O . | . . .
'''
class Node(object):
    def __init__(self, state):
        self.state = state
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)
    
    def getChild(self,num):
        return self.children[num]
'''

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

##########################
###### MINI-MAX A-B ######
##########################
class GameState:
    def __init__(self, boards, depth,player,prev_move):
        self.boards = boards
        self.depth = depth
        self.player = player
        self.prev_move= prev_move
        return
    #return a integer to indicate the advantage
    def getHeuristic(self):
                #if this is a win state for X, return infinity
        if self.winState(1)== True :
            print_boards(self.boards)
            print("the board above has the heuristic of inf" )
            return float('inf')
        elif self.winState(2) == True :
            print_boards(self.boards)
            print("the board above has the heuristic of -inf" )
            return -float('inf')
        else :
            #TODO: calculate heuristic here
            heurA = self.possible_num_ways_win(1) - self.possible_num_ways_win(2)
            heurB = self.min_move_to_win(1)-self.min_move_to_win(2)
            heuristic =  heurA + heurB
            print_boards(self.boards)
            print("the board above has the heuristic of %d" % heuristic)
            #print("it is heuristic")
            #print(heuristic)
            return heuristic

        #return a bool to indicate whether this board is a winstate for a given player
        #
        #TODO

    def min_move_to_win(self, player1):
        curr_boards = self.boards
        score = 0
        total = 0
        
        for i in range(1,10):
            total = total + score
            score = 0
            if(curr_boards[i][1]==player1):
                for li in ([2,3],[4,7],[5,9]):
                    if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                    (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                        score = 1
                        continue
            
            if(curr_boards[i][2] == player1):
                for li in ([1,3],[5,8]):
                    if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                    (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                        score = 1
                        continue
            if(curr_boards[i][3] == player1):
                for li in ([1,2],[5,7],[6,9]):
                    if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                    (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                        score = 1
                        continue

            if(curr_boards[i][4] == player1):
                for li in ([1,7],[5,6]):
                    if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                    (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                       score = 1
                       continue

            if(curr_boards[i][5] == player1):
                for li in ([1,9],[2,8],[3,7],[4,6]):
                    if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                    (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                       score = 1
                       continue

            if(curr_boards[i][6] == player1):
                for li in ([4,5],[3,9]):
                    if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                    (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                       score = 1
                       continue
            
            if(curr_boards[i][7] == player1):
                for li in ([1,4],[3,5],[8,9]):
                    if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                    (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                       score = 1
                       continue
            if(curr_boards[i][8] == player1):
                for li in ([2,5],[7,9]):
                    if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                    (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                        score = 1
                        continue
            if(curr_boards[i][9] == player1):
                for li in ([1,5],[3,6],[7,8]):
                    if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                    (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                       score = 1
                       continue
        print(total)
        return total 

    def possible_num_ways_win(self, player):
        curr_boards = self.boards
        num = 0
        if(player ==1):
            player2 =2
        else:
            player2 =1 

        for i in range(1,10):
            if (curr_boards[i][1]==player or curr_boards[i][2]==player or curr_boards[i][3]==player):
                if not (curr_boards[i][1]==player2 or curr_boards[i][2]==player2 or curr_boards[i][3]==player2):
                    num = num+1
            if(curr_boards[i][4]==player or curr_boards[i][5]==player or curr_boards[i][6] == player):
                if not (curr_boards[i][4]==player2 or curr_boards[i][5]==player2 or curr_boards[i][6] == player2):
                    num = num+1
            if(curr_boards[i][7]==player or curr_boards[i][8]==player or curr_boards[i][9] == player):
                if not (curr_boards[i][7]==player2 or curr_boards[i][8]==player2 or curr_boards[i][9] == player2):
                    num = num+1
            if(curr_boards[i][1]==player or curr_boards[i][4]==player or curr_boards[i][7] == player):
                if not (curr_boards[i][1]==player2 or curr_boards[i][4]==player2 or curr_boards[i][7] == player2):
                    num = num+1
            if(curr_boards[i][2]==player or curr_boards[i][5]==player or curr_boards[i][8] == player):
                if not (curr_boards[i][2]==player2 or curr_boards[i][5]==player2 or curr_boards[i][8] == player2):
                    num = num+1
            if(curr_boards[i][3]==player or curr_boards[i][6]==player or curr_boards[i][9] == player):
                if not (curr_boards[i][3]==player2 or curr_boards[i][6]==player2 or curr_boards[i][9] == player2):
                    num = num+1
            if(curr_boards[i][1]==player or curr_boards[i][5]==player or curr_boards[i][9] ==player):
                if not (curr_boards[i][1]==player2 or curr_boards[i][5]==player2 or curr_boards[i][9] == player2):
                    num = num+1
            if(curr_boards[i][3]==player or curr_boards[i][5]==player or curr_boards[i][7] == player) :
                if not (curr_boards[i][3]==player2 or curr_boards[i][5]==player2 or curr_boards[i][7] == player2):
                    num = num+1
        return num
    
    #def min_move_to_win(self, player):
        #curr_boards = self.boards

    
    def winState(self, player):
        curr_boards = self.boards
        for i in range(1,10):
            if (player==curr_boards[i][1]==curr_boards[i][2]==curr_boards[i][3] or 
            player==curr_boards[i][4]==curr_boards[i][5]==curr_boards[i][6] or
            player==curr_boards[i][7]==curr_boards[i][8]==curr_boards[i][9] or
            player==curr_boards[i][1]==curr_boards[i][4]==curr_boards[i][7] or
            player==curr_boards[i][2]==curr_boards[i][5]==curr_boards[i][8] or
            player==curr_boards[i][3]==curr_boards[i][6]==curr_boards[i][9] or
            player==curr_boards[i][1]==curr_boards[i][5]==curr_boards[i][9] or
            player==curr_boards[i][3]==curr_boards[i][5]==curr_boards[i][7]) :
                return True
        return False



class AlphaBeta:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, boards):
        global curr
        first_state = GameState(boards, 0,2, curr)
        self.game_state = first_state
        self.game_tree = boards  # GameTree
        #self.root = game_tree  # GameNode
        #self.root = Node(first_state)
        return

    def alpha_beta_search(self, game_state):
        print("alpha_beta_search is called")
        infinity = float('inf')
        best_val = -infinity
        beta = infinity
        '''
        if self.getUtility(game_state)==float('inf'):
            return float('inf')
        if self.getUtility(game_state)==-float('inf') :
            return -float('inf')
        '''
        children = self.getChildren(game_state)
        best_state = None
        for state in children:
            #stateNode = Node(state)
            #self.root.add_child(stateNode)
            value = self.min_value(state, best_val, beta)
            print("printing value %f"% value)
            if value > best_val:
                best_val = value
                best_state = state
        #print "AlphaBeta:  Utility Value of Root Node: = " + str(best_val)
        #print "AlphaBeta:  Best State is: " + best_state.Name
        #assert best_state is not None
        return best_state

    def max_value(self, state, alpha, beta):
        #print "AlphaBeta-->MAX: Visited Node :: " + node.Name
        if self.isTerminal(state):
            return self.getUtility(state)
        infinity = float('inf')
        value = -infinity
        if self.getUtility(state)==float('inf'):
            return float('inf')
        if self.getUtility(state)==-float('inf') :
            return -float('inf')

        children = self.getChildren(state)
        for state in children:
            eval = self.min_value(state, alpha, beta)
            value = max(value, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
            #if value >= beta:
            #    return value
        return value

    def min_value(self, state, alpha, beta):
        #print "AlphaBeta-->MIN: Visited Node :: " + node.Name
        if self.isTerminal(state):
            return self.getUtility(state)
        infinity = float('inf')
        value = infinity
        if self.getUtility(state)==float('inf'):
            return float('inf')
        if self.getUtility(state)==-float('inf') :
            return -float('inf')

        children = self.getChildren(state)
        #i = 0
        for state in children:
            #self.getChildren(i).add_child(state)
            eval = self.max_value(state, alpha, beta)
            value = min(value, eval)
            #if value <= alpha:
            #   return value
            beta = min(beta, eval)
            if beta <= alpha:
                break

        return value
    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def getChildren(self, game_state):
        global curr
        curr_depth = game_state.depth
        #print(curr_depth)
        next_depth = curr_depth +1
        if(game_state.player==1):
            next_player=2
        else:
            next_player=1

        children = []
        board=game_state.prev_move
        boards = game_state.boards
        for i in range(1,10):
            if boards[board][i]==0:
                next_boards = boards.copy()
                next_boards[board][i] = next_player
                next_game_state = GameState(next_boards, next_depth,next_player, i)
                #print(next_game_state.depth)
                #print("this is a board in depth %d" % next_depth)
                #print_boards(next_game_state.boards)
                children.append(next_game_state)
        assert boards is not None
        
        return children

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, state):
        #assert node is not None
        #return len(node.children) == 0
        global max_depth
        
        if(state.depth==max_depth):
            return True
        return False

    def getUtility(self, state):
        #assert node is not None
        return state.getHeuristic()

# choose a move to play, we are playing X
def play():
    global curr
    #global max_depth
    #print_boards(boards)
    #start coding here
    curr_board = boards
    print ("the curr board is ")
    #print_boards(curr_board)
    next_move=0
    alphabeta = AlphaBeta(boards)
    nextState = alphabeta.alpha_beta_search(alphabeta.game_state)
    if (nextState == None):
        print("I LOSE")
        for i in range(1,10):
            if curr_board[curr][i]==0:
                return i
        
    
    next_board = nextState.boards
    print("trying to play")
    #print_boards(next_board)
    for i in range(1,10):
        for j in range(1,10):
            #print("\n")
            #print(i,j)
            #print(curr_board[i][j])
            #print(next_board[i][j])
            if not (curr_board[i][j] == next_board[i][j]):
                next_move = j
                break
    print_boards(curr_board)
    print ("we are playing move %d\n" % (next_move))
    print_boards(next_board)

    place(curr, next_move, 1)
    return next_move

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
        print("This is Hansen, We win!! :)")
        return -1
    elif command == "loss":
        print("This is Hansen,We lost :(")
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
