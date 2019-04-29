#!/usr/bin/python3
# Sample starter bot by Zac Partridge
# Contact me at z.partridge@unsw.edu.au
# 06/04/19
# Feel free to use this and modify it however you wish
'''
Usage: python3 agent.py -p portNum

Briefly describe how your program works, including any algorithms and data structures employed, 
and explain any design decisions you made along the way.

We are using alpha-beta tree search algorithm to implement the AI. The search stops when the tree reaches maximum depth (given by us). 
The node of the tree is instance of GameState which contains a expanded board, its depth, player (1 or 2) of previous move and previous move.
If the leaf node is not the end of the game, we try to evaluate the GameState by 2 heuristic functions: 
The first heuristic function is called possible_num_ways_win(player, i). This function returns an integer which is the possible number of ways to win (1 of 3 in a row) in i th (3*3)board.
The second heuristic function is called is_one_more_to_win(player, i). This function check if there is a potential win in a i th board (one more move on this board will lead to win)
We try to changes the values of maximum depth dynamically by checking how many moves are made already. 
We want to increase the deep gradually because the deeper node might have fewer children and will not timeout.
Alphabeta functions will find and return a GameState which have the largest value after recurrently iterating through minmax functions.
By comparing current board with a board returned by alphabeta search, we can extract our 'best' move to place on.
'''



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
num_move = 0

# print a row. | . O . | . . .

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

# GameState is the node of the tree
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
            return float('inf')
        #if this is a win state for O, return -infinity
        elif self.winState(2) == True :
            return -float('inf')
        else :
        #if it is not end state, we calculate the value heuristic for each node
            heurA = 0
            heurB = 0
            heuristic =0
            for i in range (1,10):
                heurA =  3* self.is_one_more_to_win(1, i)+ self.possible_num_ways_win(1, i) 
                heurB = -3*self.is_one_more_to_win(2, i) - self.possible_num_ways_win(2, i) 
                heuristic = heuristic + heurA + heurB 
            return heuristic

    #return if there is a potential win state
    def is_one_more_to_win(self, player1, i):
        curr_boards = self.boards
        if(curr_boards[i][1]==player1):
            for li in ([2,3],[4,7],[5,9]):
                if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                    return 1
        
        if(curr_boards[i][2] == player1):
            for li in ([1,3],[5,8]):
                if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                    return 1
        if(curr_boards[i][3] == player1):
            for li in ([1,2],[5,7],[6,9]):
                if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                    return 1

        if(curr_boards[i][4] == player1):
            for li in ([1,7],[5,6]):
                if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                    return 1

        if(curr_boards[i][5] == player1):
            for li in ([1,9],[2,8],[3,7],[4,6]):
                if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                    return 1

        if(curr_boards[i][6] == player1):
            for li in ([4,5],[3,9]):
                if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                    return 1
        
        if(curr_boards[i][7] == player1):
            for li in ([1,4],[3,5],[8,9]):
                if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                    return 1

        if(curr_boards[i][8] == player1):
            for li in ([2,5],[7,9]):
                if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                    return 1

        if(curr_boards[i][9] == player1):
            for li in ([1,5],[3,6],[7,8]):
                if ((curr_boards[i][li[0]]==player1 and curr_boards[i][li[1]]==0) or 
                (curr_boards[i][li[0]]==0 and curr_boards[i][li[1]]==player1)):
                    return 1
        return 0

    #return the possible number to win
    def possible_num_ways_win(self, player, i):
        curr_boards = self.boards
        num = 0
        if(player ==1):
            player2 =2
        else:
            player2 =1 

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

    #check if current state is a winning state for player
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


# alphabeta search
class AlphaBeta:

    def __init__(self, boards):
        global curr
        first_state = GameState(boards, 0,2, curr)
        self.game_state = first_state
        self.game_tree = boards 
        return

    def alpha_beta_search(self, game_state):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity
        result = []
        children = self.getChildren(game_state)
        best_state = None
        for state in children:
            value = self.min_value(state, best_val, beta)
            
            result.append(value)
            if value > best_val:
                best_val = value
                best_state = state

        return best_state
    # max for alphabeta search
    def max_value(self, state, alpha, beta):
        global max_depth
        # if it is terminal node get heuristic
        if state.depth==max_depth:
            return state.getHeuristic()

        infinity = float('inf')
        value = -infinity
        if state.winState(1)== True :
            return infinity
        if state.winState(2)== True :
            return -infinity

        children = self.getChildren(state)
        for state in children:
            eval = self.min_value(state, alpha, beta)
            value = max(value, eval)
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    # min for alphabeta search
    def min_value(self, state, alpha, beta):
        global max_depth

        # if it is terminal node get heuristic
        if state.depth==max_depth:
            return state.getHeuristic()
        infinity = float('inf')
        value = infinity

        if state.winState(1)== True :
            return infinity
        if state.winState(2)== True :
            return -infinity

        children = self.getChildren(state)
        for state in children:
            eval = self.max_value(state, alpha, beta)
            value = min(value, eval)
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    # get child notes for current game state
    def getChildren(self, game_state):
        global curr
        curr_depth = game_state.depth
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
                children.append(next_game_state)
        assert boards is not None
        
        return children

    # return true if the node has NO children
    # return false if the node has children 
    # def isTerminal(self, state):
    #     global max_depth
    #     if():
    #         return True
    #     return False

# choose a move to play, we are playing X (1)
def play():
    global curr
    global num_move
    global max_depth
    #print(max_depth)

    curr_board = boards

    next_move=0
    alphabeta = AlphaBeta(boards)
    nextState = alphabeta.alpha_beta_search(alphabeta.game_state)
    if (nextState == None):
        print("I LOSE")
        for i in range(1,10):
            if curr_board[curr][i]==0:
                return i
        
    
    next_board = nextState.boards

    for i in range(1,10):
        for j in range(1,10):
            if not (curr_board[i][j] == next_board[i][j]):
                next_move = j
                break
    
    if(num_move > 15):
        max_depth = 5
    if(num_move>20):
        max_depth = 6
    if(num_move > 35):
        max_depth = 8
    if(num_move >40):
        max_depth = 10
    place(curr, next_move, 1)
    return next_move

# place a move in the global boards
def place(board, num, player):
    global curr
    global num_move
    curr = num
    boards[board][num] = player
    num_move = num_move+1

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
