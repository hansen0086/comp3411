sign_runs([],[]).
sign_runs(List,[List]).

same_sign(Num1, Num2):-
    0>Num1,
    0>Num2.
same_sign(Num1, Num2):-
    0=< Num1,
    0=< Num2.

%First and second are not the same
sign_runs([First|FirstTail], [[First]|Rest]):-
    FirstTail=[Second|SecondTail],
    not(same_sign(First, Second)),
    sign_runs(FirstTail, Rest).

%First and second are the same
sign_runs([First|FirstTail], [[First,Second]|Rest]):-
    FirstTail=[Second|SecondTail],
    same_sign(First, Second),
    append(First, Second,Result),

    sign_runs(FirstTail, Rest),
    append()SecondTail],
    same_sign(First, Second),
    append(First, Second,Result),

    a(FirstTail, Result, Rest),
    sign_runs(FirstTail, Rest),
    append()
    .

a(X, A, A).
a([F,S|T], A, R):-
    same_sign(F, S),
    append(S, A, Result),
    a(S|T, Result, R).









