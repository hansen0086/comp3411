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
#   1 - I played here
#   2 - They played here

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