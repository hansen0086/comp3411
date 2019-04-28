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
#include <assert.h>
#include <math.h>
#include "common.h"
#include "agent.h"
#include "game.h"


#define true 1
#define false 0

struct node
{
    struct node *children;
    int numOfCildren;
    //node * parent;
    int depth;
    int prev_move;
    int player;
    int** boards;
};

int possible_num_ways_win(int player, struct node* state);
int winState(int player);
int isTerminal(struct node* state);
double getHeuristic(struct node* state);
int play();
double min_value(struct node* state, double alpha, double beta);
double max_value(struct node* state, double alpha, double beta);
struct node** getChildren(struct node* game_state);
int** copyBoard(int** boards);

#define MAX_MOVE 81
#define MAX_DEPTH 6
int board[10][10];
int move[MAX_MOVE+1];
int player;
int m;

/* newNode() allocates a new node with the given data(new_boards) with default 9 children*/
struct node* newGameState(int** new_boards, int depth, int player, int prev_move)
{ 
    // Allocate memory for new node
    struct node* node = (struct node*)malloc(sizeof(struct node));
    //node child_array[9];
    // Assign data to this node
    node->boards = new_boards;
    node->depth = depth;
    node->player = player;
    node->prev_move = prev_move;
    //node->numOfCildren = 9;

    //node->children = child_array;
    // array of children
    //node->parent = parent;
    
    
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
  this_move = play();
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
  this_move = play();
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
 this_move = play();
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
int winState(int player)
{
  for (int i = 1 ;i < 10;i++){
      if ((player==board[i][1]&& player ==board[i][2]&& player==board[i][3]) ||
      (player==board[i][4]&& player==board[i][5]&& player==board[i][6])||
      (player==board[i][7]&& player==board[i][8]&& player==board[i][9])||
      (player==board[i][1]&& player==board[i][4]&& player==board[i][7])||
      (player==board[i][2]&& player==board[i][5]&& player==board[i][8])||
      (player==board[i][3]&& player==board[i][6]&& player==board[i][9])||
      (player==board[i][1]&& player==board[i][5]&& player==board[i][9])||
      (player==board[i][3]&& player==board[i][5]&& player==board[i][7]))
      return true;
  }
  return false ;
}                                                          
                                                                                      
/*********************************************************//*
*/
int possible_num_ways_win(int player, struct node* state)
{
  int** curr_boards = state->boards;
  int num = 0;
  int player2 = 0;
  if(player == 1)
      player2 =2;
  else
      player2 =1;

  for (int i=1; i<10; i++){
      if (curr_boards[i][1]==player || curr_boards[i][2]==player || curr_boards[i][3]==player){
          if (!(curr_boards[i][1]==player2 || curr_boards[i][2]==player2 || curr_boards[i][3]==player2))
              num = num+1;
      }
      if(curr_boards[i][4]==player || curr_boards[i][5]==player || curr_boards[i][6] == player){
          if (! (curr_boards[i][4]==player2 || curr_boards[i][5]==player2 || curr_boards[i][6] == player2))
              num = num+1;
      }
      if(curr_boards[i][7]==player || curr_boards[i][8]==player || curr_boards[i][9] == player){
          if (! (curr_boards[i][7]==player2 || curr_boards[i][8]==player2 || curr_boards[i][9] == player2))
              num = num+1;
      }
      if(curr_boards[i][1]==player || curr_boards[i][4]==player || curr_boards[i][7] == player){
          if (! (curr_boards[i][1]==player2 || curr_boards[i][4]==player2 || curr_boards[i][7] == player2))
              num = num+1;
      }
      if(curr_boards[i][2]==player || curr_boards[i][5]==player || curr_boards[i][8] == player){
          if (! (curr_boards[i][2]==player2 || curr_boards[i][5]==player2 || curr_boards[i][8] == player2))
              num = num+1;
      }
      if(curr_boards[i][3]==player || curr_boards[i][6]==player || curr_boards[i][9] == player){
          if (! (curr_boards[i][3]==player2 || curr_boards[i][6]==player2 || curr_boards[i][9] == player2))
              num = num+1;
      }
      if(curr_boards[i][1]==player || curr_boards[i][5]==player || curr_boards[i][9] ==player){
          if (! (curr_boards[i][1]==player2 || curr_boards[i][5]==player2 || curr_boards[i][9] == player2))
              num = num+1;
      }
      if(curr_boards[i][3]==player || curr_boards[i][5]==player || curr_boards[i][7] == player){
          if (! (curr_boards[i][3]==player2 || curr_boards[i][5]==player2 || curr_boards[i][7] == player2))
              num = num+1;
      }
  }
  return num;
}        
//TODO
int isTerminal(struct node* state){

  if(state->depth ==MAX_DEPTH)
    return true;

  return false;
}

// TODO 
double getHeuristic(struct node* state){
    return possible_num_ways_win(1, state) - possible_num_ways_win(2, state);
}

struct node * alphabeta(struct node* game_state){
    double best_val = -INFINITY;
    double beta = INFINITY;
    
    //MAYBE FAULSE
    //TODO
    struct node** children = getChildren(game_state);
    struct node* best_state = NULL;
    for(int i=1; i<10; i++){
        struct node* state = children[i];
        if(state==NULL) continue;
        
        int value = min_value(state, best_val, beta);
        if(value > best_val){
            best_val = value;
            best_state = state;
        }
    }
    return best_state;
}
int max(double A, double B){
  return A>B;
}

int min(double A, double B){
  return A<B;
}
double max_value(struct node* state, double alpha, double beta){
  if(isTerminal(state))
    return getHeuristic(state);

  double value = -INFINITY;
  double eval=0;

  if(getHeuristic(state)==INFINITY)
    return INFINITY;
  if (getHeuristic(state)==-INFINITY)
    return -INFINITY;

  struct node** children = getChildren(state);
  
  for(int i=1; i<10; i++){
    struct node* state = children[i];
    if(state==NULL)
      continue;
    
    
    eval = min_value(state, alpha, beta);
    value = max(value, eval);
    alpha = max(alpha, eval);
    if(beta <= alpha)
      break;
  }
  return value;
}

double min_value(struct node* state, double alpha, double beta){
  if(isTerminal(state))
    return getHeuristic(state);

  double value = INFINITY;
  double eval = 0;
  
  if(getHeuristic(state)==INFINITY)
    return INFINITY;
  if(getHeuristic(state)==-INFINITY)
    return -INFINITY;

  struct node** children = getChildren(state);

  for(int i=1; i<10; i++){
    struct node* state = children[i];
    if(state==NULL)
      continue;
    eval = max_value(state, alpha, beta);
    value = min(value, eval);
    alpha = min(alpha, eval);
    if(beta <= alpha)
      break;
  }
  return value;
}


int play(){
  int next_move = 0;
  //TODO
  int curr = move[m];
  int ** temp_board;
  temp_board = (int **) malloc(sizeof(int *)*10);
  for(int i=0;i<10;i++){
    temp_board[i] = (int *)malloc(sizeof(int)*10); 
  }
  for(int i=0;i<10;i++){
    for(int j=0;j<10;j++)
    temp_board[i][j]= board[i][j];
  }
  struct node* game_state = newGameState(temp_board, 0, 2, curr);
  struct node* nextState = alphabeta(game_state);
  if(nextState == NULL){
    printf("I LOSE");
    for(int i=1; i<10; i++){
      if(board[m][i]==0)
        return i;
    }
  }

  int** next_board = nextState->boards;
  
  for(int i=1; i<10; i++){
    for(int j=1; j<10; j++){
      if(board[i][j]!=next_board[i][j]){
        next_move = j;
        break;
      }

    }
  }

  return next_move;
}

struct node** getChildren(struct node* game_state){
    int curr_depth = game_state->depth;
    int next_depth = curr_depth + 1;
    int next_player = 0;
    if(game_state->player ==1)
        next_player = 2;
    else
        next_player=1;

    struct node* children[10];
    for(int i=1; i<10; i++)
        children[i] = malloc(sizeof(struct node));
    
    int board = game_state->prev_move;
    int** boards = game_state->boards;
    for(int i=1; i<10; i++){
        if(boards[board][i]==0){
            
            int **next_boards = copyBoard(boards);
            next_boards[board][i] = next_player;
            struct node* next_game_state = newGameState(next_boards, next_depth, next_player, i);
            children[i] = next_game_state;
            assert(boards!=NULL);
        }
    }

    return children;

}
    
int** copyBoard(int** boards){
  int** new_boards = malloc(100*sizeof(int));

  for(int i=1; i<10; i++){
    for(int j=1; j<10; j++){
      new_boards[i][j] = boards[i][j];
    }
  }
  return new_boards;
}


  
