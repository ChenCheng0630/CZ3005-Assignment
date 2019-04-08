/* setting up basic ask query to retrive on activity*/
ask(X, Y):-
  related(X, Y), \+ history(X).
ask(X, Y):-
  random(X), \+ related(X, Y), \+ history(X).

/* helper function to determine if an element is a member of a list*/
member(X,[X|_]).
member(X,[_|R]) :- member(X,R).

/* define the relationship between two related elements*/
related(X,Y) :-
	play(L), member(X, L), member(Y, L);
	eat(L), member(X, L), member(Y, L);
	see(L), member(X, L), member(Y, L);
	learn(L), member(X, L), member(Y, L).

/* Define one postive description of a particular element*/
followup_positive_description(X, Y):-
  play(L), member(X, L), play_positive_description(S), member(Y, S) ;
  eat(L), member(X, L), eat_positive_description(S), member(Y, S);
  see(L), member(X, L), see_positive_description(S), member(Y, S);
  learn(L), member(X, L), learn_positive_description(S), member(Y, S).

/* Define one negative description associated with a particular element */
followup_negative_description(X, Y):-
  play(L), member(X, L), play_negative_description(S), member(Y, S);
  eat(L), member(X, L), eat_negative_description(S), member(Y, S);
  see(L), member(X, L), see_negative_description(S), member(Y, S);
  learn(L), member(X, L), learn_negative_description(S), member(Y, S).

/* Define one action associated with a particular element */
followup_action(X, Y):-
  play(L), member(X, L), play_action(S), member(Y, S);
  eat(L), member(X, L), eat_action(S), member(Y, S);
  see(L), member(X, L), see_action(S), member(Y, S);
  learn(L), member(X, L), learn_action(S), member(Y, S).

/* helper function to find one random element from the list */
random(X) :-
	play(L), member(X, L);
	eat(L), member(X, L);
	see(L), member(X, L);
	learn(L), member(X, L).

/* the list of activities the kid could do in school */
play([slides, sandbox, toys, trains, cars, playmat, ball]).
eat([cake, toffee, candy, sandwich, pizza, cheerios, veggies, fries, hamburgers, chocolate]).
see([bird, flowers]).
learn([alphabet, numbers, mathematics, drawing]).

/* the list of possible positive feelings the kid could have */
play_positive_description([fun, enjoyable, exiciting]).
eat_positive_description([tasty, delicious, healthy]).
see_positive_description([colourful, fancy, nice]).
learn_positive_description([enjoyable, fun, interesting]).

/* the list of possible negative feelings the kid could have */
play_negative_description([tiring, exhausting, bad]).
eat_negative_description([awful, bitter, unsavory]).
see_negative_description([dull, ugly, bad-looking]).
learn_negative_description([difficult, frustraing]).

/* the list of possible actions the kid should have done */
play_action([wash_hand_after_that, drink_enough_water]).
eat_action([clean_the_plate, clean_the_table, wash_hands_before_that]).
see_action([try_to_take_photo, touch_it]).
learn_action([take_notes, pay_attention, ask_teacher_questions]).

history(nothing).
