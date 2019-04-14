sign_runs([],[]).
sign_runs(List,[List]).

same_sign(Num1, Num2):-
    0>Num1,
    0>Num2.
same_sign(Num1, Num2):-
    0=< Num1,
    0=< Num2.

%First and second are not the same
sign_runs([Head1,Head2|Tail], List):-
    not(same_sign(Head1, Head2)),
    List = []

