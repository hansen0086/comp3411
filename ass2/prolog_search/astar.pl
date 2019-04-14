% A-Star Search

% COMP3411/9414/9814 Artificial Intelligence, UNSW, Alan Blair

% solve(Start, Solution, G, N)
% Solution is a path (in reverse order) from start node to a goal state.
% G is the length of the path, N is the number of nodes expanded.

solve(Start, Solution, G, N)  :-
    consult(pathsearch), % insert_legs(), head_member(), build_path()
    h(Start,H),
    astar([[Start,Start,0,H]], [], Solution, G, 1, N).

% astar(Generated, Expanded, Solution, L, M, N)
%
% Generated = [[Node1,Prev1,G1,H1],[Node2,Prev2,G2,H2],...,[Start,Start,0,H0]]
%  Expanded = [[Node1,Prev1,G1],[Node2,Prev2,G2],...,[Start,Start,0]]
% Generated (but not yet expanded) Nodes are stored in increasing order of G+H.
% Each Node occurs at most once in the Expanded list (with mimimum value of G).

% If the next leg to be expanded begins with a goal node,
% stop searching, build the path and return it.
astar([[Node,Pred,G,_H]|_Generated], Expanded, Path, G, N, N)  :-
    goal(Node),
    build_path([[Node,Pred,G]|Expanded], Path).

% Extend leg at head of queue by generating successors of its destination node.
% Insert newly created legs into the Generated list (in increasing order of G+H).
% Transfer expanded leg to the Expanded list, and continue searching.
astar([[Node,Pred,G,_H]| Generated], Expanded, Solution, G1, L, N) :-
    extend(Node, G, Expanded, NewLegs),
    M is L + 1,
    insert_legs(Generated, NewLegs, Generated1),
    insert_expanded([Node,Pred,G], Expanded, Expanded1),
    astar(Generated1, Expanded1, Solution, G1, M, N).

% Find all successor nodes to this node, and check in each case
% that a shorter path to the new node has not already been expanded.
extend(Node, G, Expanded, NewLegs) :-
    % write(Node),nl,   % print nodes as they are expanded
    findall([NewNode, Node, G1, H], (s(Node, NewNode, C)
    , G1 is G + C
    , not(shorter_path(NewNode, G1, Expanded))
    , h(NewNode, H)
    ), NewLegs).

% Discard new leg if we already knew of a shorter path to the same Node.
insert_expanded([Node,_Prev,G], Expanded, Expanded) :-
    shorter_path(Node, G, Expanded), ! .

% Otherwise, add new leg to front of Expanded list.
insert_expanded(Leg, Expanded, [Leg|Expanded]).

% base case: first item in list is shorter path to same Node.
shorter_path(Node, G, [[Node,_Pred,G1]|_]) :-
    G >= G1, ! .

% Otherwise, keep searching rest of list.
shorter_path(Node, G, [_Leg|Expanded]) :-
    shorter_path(Node, G, Expanded).

% base case: insert one leg into an empty list.
insert_one_leg([], Leg, [Leg]).

% If we already knew a shorter path to the same node, discard the new one.
insert_one_leg([Leg1|Generated], Leg, [Leg1|Generated]) :-
    Leg  = [Node,_Pred, G, _H],
    Leg1 = [Node,_Pred1,G1,_H1],
    G >= G1, ! .

% Insert the new leg in its correct place in the list (ordered by G+H).
insert_one_leg([Leg1|Generated], Leg, [Leg,Leg1|Generated]) :-
    Leg  = [_Node, _Pred, G, H ],
    Leg1 = [_Node1,_Pred1,G1,H1],
    F1 is G1 + H1,
    F is G + H,
    F < F1, ! .

% Search recursively for the correct place to insert.
insert_one_leg([Leg1|Generated], Leg, [Leg1|Generated1]) :-
    insert_one_leg(Generated, Leg, Generated1).
