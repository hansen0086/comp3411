/*********************************************************
 *  agent.c
 *  Nine-Board Tic-Tac-Toe Agent
 *  COMP3411/9414/9814 Artificial Intelligence
 *  Alan Blair, CSE, UNSW
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <stdbool.h>
#include <math.h>
#include "common.h"
#include "agent.h"
#include "game.h"

#define MAX_MOVE 81

int board[10][10];
int move[MAX_MOVE+1];
int player;
int m;

struct node
{
      node *children;
      int numOfCildren;
      node * parent;
      int *d;
}
  
/* newNode() allocates a new node with the given data(new_boards) with default 9 children*/
struct node* newNode(node parent, int* new_boards) 
{ 
  // Allocate memory for new node  
  struct node* node = (struct node*)malloc(sizeof(struct node)); 
  node child_array[9];
  // Assign data to this node 
  node->data = new_boards; 
  
  node->numOfCildren = 9;
  
  node->children = child_array;// array of children

  node->parent = parent;
  

  return(node); 
} 
/*********************************************************//*
   Print usage information and exit
*/
void usage( char argv0[] )
{
  printf("Usage: %s\n",argv0);
  printf("       [-p port]\n"); // tcp port
  printf("       [-h host]\n"); // tcp host
  exit(1);
}

/*********************************************************//*
   Parse command-line arguments
*/
void agent_parse_args( int argc, char *argv[] )
{
  int i=1;
  while( i < argc ) {
    if( strcmp( argv[i], "-p" ) == 0 ) {
      if( i+1 >= argc ) {
        usage( argv[0] );
      }
      port = atoi(argv[i+1]);
      i += 2;
    }
    else if( strcmp( argv[i], "-h" ) == 0 ) {
      if( i+1 >= argc ) {
        usage( argv[0] );
      }
      host = argv[i+1];
      i += 2;
    }
    else {
      usage( argv[0] );
    }
  }
}

/*********************************************************//*
   Called at the beginning of a series of games
*/
void agent_init()
{
  struct timeval tp;

  // generate a new random seed each time
  gettimeofday( &tp, NULL );
  srandom(( unsigned int )( tp.tv_usec ));
}

/*********************************************************//*
   Called at the beginning of each game
*/
void agent_start( int this_player )
{
  reset_board( board );
  m = 0;
  move[m] = 0;
  player = this_player;
}

/*********************************************************//*
   Choose second move and return it
*/
int agent_second_move( int board_num, int prev_move )
{
  int this_move;
  move[0] = board_num;
  move[1] = prev_move;
  board[board_num][prev_move] = !player;
  m = 2;
  do {
    this_move = 1 + random()% 9;
  } while( board[prev_move][this_move] != EMPTY );
  move[m] = this_move;
  board[prev_move][this_move] = player;
  return( this_move );
}

/*********************************************************//*
   Choose third move and return it
*/
int agent_third_move(
                     int board_num,
                     int first_move,
                     int prev_move
                    )
{
  int this_move;
  move[0] = board_num;
  move[1] = first_move;
  move[2] = prev_move;
  board[board_num][first_move] =  player;
  board[first_move][prev_move] = !player;
  m=3;
  do {
    this_move = 1 + random()% 9;
  } while( board[prev_move][this_move] != EMPTY );
  move[m] = this_move;
  board[move[m-1]][this_move] = player;
  return( this_move );
}

/*********************************************************//*
   Choose next move and return it
*/
int agent_next_move( int prev_move )
{
  int this_move;
  m++;
  move[m] = prev_move;
  board[move[m-1]][move[m]] = !player;
  m++;
  do {
    //TODO
    this_move = 1 + random()% 9;
  } while( board[prev_move][this_move] != EMPTY );
  move[m] = this_move;
  board[move[m-1]][this_move] = player;
  return( this_move );
}

/*********************************************************//*
   Receive last move and mark it on the board
*/
void agent_last_move( int prev_move )
{
  m++;
  move[m] = prev_move;
  board[move[m-1]][move[m]] = !player;
}

/*********************************************************//*
   Called after each game
*/
void agent_gameover(
                    int result,// WIN, LOSS or DRAW
                    int cause  // TRIPLE, ILLEGAL_MOVE, TIMEOUT or FULL_BOARD
                   )
{
  // nothing to do here
}

/*********************************************************//*
   Called after the series of games
*/
void agent_cleanup()
{
  // nothing to do here
}


/*********************************************************//*
*/
bool winState(int player)
{
  int curr_boards = board;
  for i in range(1,10):
      if ((player==curr_boards[i][1]&& player ==curr_boards[i][2]&& player==curr_boards[i][3]) ||
      (player==curr_boards[i][4]&& player==curr_boards[i][5]&& player==curr_boards[i][6])||
      (player==curr_boards[i][7]&& player==curr_boards[i][8]&& player==curr_boards[i][9])||
      (player==curr_boards[i][1]&& player==curr_boards[i][4]&& player==curr_boards[i][7])||
      (player==curr_boards[i][2]&& player==curr_boards[i][5]&& player==curr_boards[i][8])||
      (player==curr_boards[i][3]&& player==curr_boards[i][6]&& player==curr_boards[i][9])||
      (player==curr_boards[i][1]&& player==curr_boards[i][5]&& player==curr_boards[i][9])||
      (player==curr_boards[i][3]&& player==curr_boards[i][5]&& player==curr_boards[i][7])
      return true;
  return false ;
}                                                          
                                                                                      
/*********************************************************//*
*/
int possible_num_ways_win(int player)
{
  curr_boards = boards
  num = 0
  if(player == 1):
      player2 =2
  else:
      player2 =1 

  for i in range(1,10){
      if (curr_boards[i][1]==player || curr_boards[i][2]==player || curr_boards[i][3]==player){
          if not (curr_boards[i][1]==player2 || curr_boards[i][2]==player2 || curr_boards[i][3]==player2)
              num = num+1;
      }
      if(curr_boards[i][4]==player || curr_boards[i][5]==player || curr_boards[i][6] == player){
          if not (curr_boards[i][4]==player2 || curr_boards[i][5]==player2 || curr_boards[i][6] == player2)
              num = num+1;
      }
      if(curr_boards[i][7]==player || curr_boards[i][8]==player || curr_boards[i][9] == player){
          if not (curr_boards[i][7]==player2 || curr_boards[i][8]==player2 || curr_boards[i][9] == player2)
              num = num+1;
      }
      if(curr_boards[i][1]==player || curr_boards[i][4]==player || curr_boards[i][7] == player){
          if not (curr_boards[i][1]==player2 || curr_boards[i][4]==player2 || curr_boards[i][7] == player2)
              num = num+1;
      }
      if(curr_boards[i][2]==player || curr_boards[i][5]==player || curr_boards[i][8] == player){
          if not (curr_boards[i][2]==player2 || curr_boards[i][5]==player2 || curr_boards[i][8] == player2)
              num = num+1;
      }
      if(curr_boards[i][3]==player || curr_boards[i][6]==player || curr_boards[i][9] == player){
          if not (curr_boards[i][3]==player2 || curr_boards[i][6]==player2 || curr_boards[i][9] == player2)
              num = num+1;
      }
      if(curr_boards[i][1]==player || curr_boards[i][5]==player || curr_boards[i][9] ==player){
          if not (curr_boards[i][1]==player2 || curr_boards[i][5]==player2 || curr_boards[i][9] == player2)
              num = num+1;
      }
      if(curr_boards[i][3]==player || curr_boards[i][5]==player || curr_boards[i][7] == player){
          if not (curr_boards[i][3]==player2 || curr_boards[i][5]==player2 || curr_boards[i][7] == player2)
              num = num+1;
      }
  }
  return num;
}                                                     
/*********************************************************//*
peseudo code

function alphabeta(node, depth, α, β, maximizingPlayer) is
    if depth = 0 or node is a terminal node then
        return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
            α := max(α, value)
            if α ≥ β then
                break (* β cut-off *)
        return value
    else
        value := +∞
        for each child of node do
            value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
            β := min(β, value)
            if α ≥ β then
                break (* α cut-off *)
        return value
*/
// TODO 
int alphabeta(node curr_board, int depth, double alpha, double beta, bool maximising)
{
  if (depth = 0 || terminalNode(curr_board))
    return getHeuristic();
  
  if (maximising){
    int value =  -INFINITY;
    getChild(curr_board);

    for(int i=0; i++; curr_board->children[i]!=NULL){

      value = max(value, alphabeta(child, depth-1, alpha, beta, false));
      alpha = max(alpha, value);
      if(alpha >= beta){
        break;
      }
    }
    return value
  }
  else{
    int value = INFINITY;
    for(int i=0; i++; curr_board->children[i]!=NULL){
      value = min(value, alphabeta(child, depth-1, alpha, beta, true));
      beta = min(beta, value);
      if(alpha>=beta){
        break;
      }
    }
    return value
  }

bool terminalNode(node curr_board){
  if(getHeuristic(curr_board)== INFINITY || getHeuristic(curr_board)== -INFINITY)
    return true;
// TODO 
double getHeuristic(node curr_board){
  
}
// TODO 
void getChild(node curr_board){
  int temp_board[][] = copyBoard(curr_board.data);

  //TODO double check if move[m]==prev_move
  for(int i=0; i<=10; i++){
    temp_board[move[m]][i] = 
  }

}

int** copyBoard(int board[][]){
  int new_board[10][10];

  for(int i=0; i<=10; i++){
    for(int j=0; j<=10; j++){
      new_baord[i][j] = board[i][j];
    }
  }
  return new_board;
}
  
