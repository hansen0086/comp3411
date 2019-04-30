insert(Num,[],[Num]).

insert(Num,[Head|Tail], [Num, Head|Tail]):-
    num<= Head.
insert()

isort([Head|Tail],NumList):-
    isort(Tail, sorted_tail),
    insert(Head, sorted_tail, NewList).



