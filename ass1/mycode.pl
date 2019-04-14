%Hansen Liu 
%z5092212
%this is my code for assignment1 in COMP3411


%Q1

is_even(Number):-
    0 is Number mod 2. 



sumsq_even([],0).
sumsq_even([First| Rest], Sum) :-
    sumsq_even(Rest, SumOfRest),
    is_even(First),
    Sum is SumOfRest+ First* First.
    


sumsq_even([First| Rest], Sum) :-
    sumsq_even(Rest, SumOfRest),
    Sum is SumOfRest.


%Q2

parent(jim, brian).
parent(brian, jenny).
parent(pat, brian).
female(pat).
female(jenny).
male(jim).
male(brian).


descendant(Person, Descendant):-
  parent(Person,Descendant).

descendant(Person, Descendant):-
  parent(Person, Child),
  descendant(Child,Descendant).


same_name(Person1, Person2):-
  parent(Person1, Person2),
  male(Person1).

same_name(Person1, Person2):-
    








