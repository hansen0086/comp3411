con([],[]).
con([],X,X).
con(X,[],X).

con([X],[Y],[X,Y]).
con([H|T],Y,[H|Result]):-
    con(T,Y,Result).







rev([],[],[]).

rev(X,[],X).
rev(X,Y,Result):-
    con(Y,X,Result).
%Write a predicate merge(Sort1,Sort2,Sort) which takes two lists Sort1 and Sort2 that are already sorted in increasing order, and binds Sort to a new list which combines the elements from Sort1 and Sort2, and is sorted in increasing order.

max(A,B,A):-
    A>B.
max(A,B,B):-
    B>=A.
min(A,B,A):-
    A<B.
min(A,B,B):-
    B=<A.




merge(X,[],X).
merge([],X,X).
merge([H,T],[H2,T2],[H2|Result]):-
    H>H2,
    merge([H,T],T2,Result).


merge([H,T],[H2,T2],[H|Result]):-
    H=<H2,
    merge(T,[H2,T2],Result).

merge2(A,[],A).
merge2([],B,B).

% If first item of first list is smaller,
% it becomes first item of the merged list
merge2([A|R],[B|S],[A|T]) :-
   A =< B,
   merge2(R,[B|S],T).

% If fmerge([A|R],S,T).irst item of second list is smaller,
% it becomes first item of the merged list
merge2([A|R],[B|S],[B|T]) :-
   A > B,
   merge2([A|R],S,T).