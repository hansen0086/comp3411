is_tree(empty).

is_tree(tree(L,Num,R)):-
    number(Num),
    is_tree(L),
    is_tree(R).


%is_heap


is_heap(empty).
%left and right are empty
is_heap(tree(L,Node,R)):-
    L = empty,
    R = empty.

%left is not empty, right is empty
is_heap(tree(L,Node,R)):-
    is_tree(L),
    L = tree(Left, Number, Right),
    Number >= Node, 
    R = empty,
    is_heap(L).

%right is not empty, left is empty
is_heap(tree(L,Node,R)):-
    is_tree(L),
    R = tree(Left, Number, Right),
    Number >= Node, 
    L = empty,
    is_heap(R).

%left and right are both not empty.
is_heap(tree(L,Node,R)):-
    R = tree(Right_Child_Left, Right_Child_Number, Right_Child_Right),
    Right_Child_Number >= Node, 
    L = tree(Left_Child_Left, Left_Child_Number, Left_Child_Right),
    Left_Child_Number >= Node, 
    is_heap(L),
    is_heap(R).

