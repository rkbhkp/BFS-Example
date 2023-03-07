This puzzle implements a **Breath First Search**

- Uses Python 3

**Introducion**
The puzzle for this semester is "Happy Cows Farm", a piece placement game. The objective of the game is to place several cows in a field in a way that maximizes a score. 

**The Farm**
The farm is a square grid board where every cell location is either grass ".",  a haystack "@", or a water pond "#". Help Clayton the happy farmer place his cows "C" in the field while observing the following rules and preferences:
- There are as many cows as haystacks.
- Cows can only be placed in grass cells.
- Cows prefer to be adjacent to a haystack either horizontally or vertically.
- Cows are most happy if they are adjacent ( horizontally or vertically ) to both a haystack and a water pond.
- Cows dislike being next to another cow, horizontally, vertically and even diagonally.

**The Scoring**
Every cow placement has a corresponding score, which is the sum of the scores assigned to each cow. A cow's score is the sum of the following applicable rules :
- +1 : If a cow is horizontally or vertically adjacent to a haystack.
- +2 : If a cow is horizontally or vertically adjacent to both a haystack and a water pond.
- -3 : If a cow is next to another cow ( horizontally, vertically or diagonally )
Notice then that a cow surrounded by grass cells has a score of 0. If a cow is next to both a hay stack and a pond it will have a score of 3

Examples:

#..C

....

@.@.

C...
Placement 1: total score = 1.
The top cow has a score of 0. The bottom cow has a score of 1.

#...
....
@C@.
.C..
Placement 2: total score = -5.
The top cow has a score of -2 ( 1-3 ). The bottom cow has a score of -3.

#...
..C.
@.@.
C...
Placement 3: total score = 2.
The top cow has a score of 1. The bottom cow has a score of 1.

#...
C...
@.@.
..C.
Placement 4: total score = 4.
The top cow has a score of 3 ( 1+2 ). The bottom cow has a score of 1.

