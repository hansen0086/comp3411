member([],[]).
member(Item, Item).
member(Item, [First|Tail]):-
    Item is First.
member(Item, [First|Tail]):-
    member(Item,Tail).


remove_dup([],[]).

remove_dup([First|Rest], NewRest):-
    member(First, Rest),
    !,
    remove_dup(Rest,NewRest ).
remove_dup([First|Rest], [First|NewRest]):-
    not(member(First, Rest)),
    remove_dup(Rest, NewRest).
