mylength([], 0).
mylength([First | Rest], Length) :-
	mylength(Rest, LengthOfRest),
	Length is LengthOfRest + 1.

% concat(List1, List2, Concat_List1_List2)
% Concat_List1_List2 is the concatenation of List1 & List2

    
concat([],List2, List2).
concat([Item | Tail1], List2,[Item | Concat_List1_List2]) :-
    concat(Tail1, List2, Concat_List1_List2).








sum_items([],0).
sum_items([Item| Rest],Sum) :-
    sum_items(Rest,SumOfRest),
    Sum is SumOfRest + Item.



cost(cornflakes, 230).
cost(cocacola, 210).
cost(chocolate, 250).
cost(crisps, 190).

total_cost([],0).
total_cost([Item|Rest], Cost):-
    cost(Item, ItemCost),
    total_cost(Rest, CostOfRest),
    Cost is CostOfRest + ItemCost.


%remove_dups(+List, -NewList):
%New List isbound to List, but with duplicate items removed.


remove_dups([],[]).
remove_dups([First|Rest], NewRest):-
    member(First, NewRest),
    remove_dups(Rest, NewRest).

remove_dups([First|Rest], [First|NewRest]):-
    not(member(First, NewRest)),
    remove_dups(Rest, NewRest).