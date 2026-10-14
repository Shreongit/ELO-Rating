 ELO-Rating

It is an excellent method for calculating relative skill levels of players represented as numeric values.

## Understanding ELO

- Consider a PvP match b/w two players, player A and player B.
- Player A has ELO rating $R_a$ and player B has ELO rating $R_b$.
- ELO ratings of individual players reflect their relative skill levels based on performance in past matches.
- Now, a player defeating a much weaker player is not the same as defeating a much more stronger player. ELO rating takes this into account and is reflected in updated ratings of both players.
- After each match, ELO rating of both players is updated based on a formula.
- Originally, it only considers the outcome of a match.

## Formula to calculate New Rating of a Player

$$
R^{'}_a = R_a + K \times (S_a - E_a)
$$

where,
<br>
$R^{'}_a: \text{New Rating of player A}$
<br>
$R_a: \text{Original Rating of player A}$
<br>
$K\ : \text{Scaling factor}$
<br>
$S_a: \text{Actual score or outcome of the match}$
<br>
$E_a: \text{Expected score or outcome of the match}$

### Scaling Factor: $K$

- It determines how much influence each match can have on the ELO ratings of the players.
- It can be varied according to matches, leagues, competitions, player rating levels, etc.
- Generally, can be set to $32$.

### Actual score: $S_a$

- Represents whether a player won or lost or drawn the match.
- Generally, it takes one of the three values:
  - $1$ for a win
  - $0$ for a loss
  - $0.5$ for a draw
  - i.e. $S_{a} \in [0, 1]$

### Expected score: $E_a$

- This is where magic of ELO ratings happen.
- It represents the probability that the player will win a match.
- It is calculated based on ELO ratings of two players.
- Formula:

$$
E_a = \frac{Q_a}{Q_a + Q_b}
\text{, where}
\begin{cases}
    Q_a = 10 ^ {R_a / c} \\
    Q_b = 10 ^ {R_b / c} \\
    c = 400 \text{ (generally)}
\end{cases}
$$

On solving  by substituting values of $Q_a$ and $Q_b$,

$$
E_a = \frac{1}{1 + 10 ^ {\frac{R_b - R_a}{c}}} \text{, where } c = 400
$$

$\therefore E_a \in [0, 1]$

- As $0 \leq S_a \leq 1$ and $0 \leq E_a \leq 1$, maximum change in a player's rating can be $K$.

### Initial ELO Rating

- It is the rating that a new player has when he starts playing the game.
- It must be significantly larger than $K$ factor, to allow a player to play, and lose enough matches before eventually winning matches, so that his ELO rating would finally start rising up.
- Generally, can be set to $1000$.

## Considering Points scored by players

### But, why?

- Consider a game, where the only thing which matters is not just the outcome of game, i.e. win or loss.
- Let's say:
  - In 1st game, player A won over player B by 5-1 score.
  - In second game player C won over player B by 2-1 score.
- In this scenario, player A had a much more dominant win than player C.
- Thus, player A much have a better rating inrease than player C.

### Method 0

- In this, we are considering the effect of points scored by individual players on the change in rating.
- We only consider the fact whether the player has won or lost or drawn the match.
- This is same as original ELO Rating.

### Method 1

- We replace $S_a$ with the fraction of points scored by player A divided by total score.
- i.e.,

$$
S_a = \frac{P_a}{P_a + P_b}
$$

where,
<br>
$P_a: \text{Points scored by player A}$
<br>
$P_b: \text{Points scored by player B}$

- This is more intuitive and we don't need to update the main rating change formula.
- But, it gives less control and predictability on the rating change.

### Method 2

- In this, we keep $S_a$ same as outcome of match, i.e., $S_a \in$ { $0, 0.5, 1$ }.
- And we extend rating update formula with another scaling factor to which acts as a bonus for the amount of scored points.
- New Formula:

$$
R^{'}_a = R_a + K \times (S_a - E_a) + p \times L \times \left( \frac{P_a}{P_a + P_b} \right)
$$

where,
<br>
$L: \text{Second scaling factor}$
<br>

$$
p =
\begin{cases}
  1 & \quad \text{if } S_a - E_a \gt 0 \\
  -1 & \quad \text{if } S_a - E_a \lt 0 \\
  0 & \quad \text{otherwise}
\end{cases}$$

$$p = \frac{S_a - E_a}{|S_a - E_a|}$$

- $L$ can be set to 16, and can be varied as well.
- This method is less intuitive, but gives much more control and predictability of the ratings.
- Using this, maximal change that a rating can have is $K + L$.

## Implementation

- I have implemented all of the above formulas in ELO class in Python and Java.

### Class ELO

- It has a constructor and two public methods.
  - constructor(): To create an instance of class ELO
  - elo(): It can be called after a match with ratings of both players and match result. It returns the updated ratings of the players.
  - elo_with_points(): It is similar to elo(), but this is with consideration of points scored by the two players.

#### Constructor

- It takes 3 arguments:
  1. k_factor: Value of $K$ factor. (int, default $32$)
  2. c_value: Value of $c$ number. (int, default $400$)
  3. l_factor: Value of $L$ factor. (int, default $16$)
- Constructor instantiates an object of ELO class with given parameters.
- In practice, it can be called multiple times for different leagues, arenas, matches, championships, competitions, etc.

#### elo() method

-  This is the rating update function which only considers the outcome of a match.
- It takes 4 arguments:
  1. rating_a: Current rating of player A. (float)
  2. rating_b: Current rating of player B. (float)
  3. outcome: Outcome of a match. (int)
- outcome must $\in$ {0, 1, 2} where,
  - outcome = 0 $\implies$ Match is drawn
  - outcome = 1 $\implies$ Player A won the match
  - outcome = 2 $\implies$ Player B won the match
- It returns the new ratings of the players in the form of tuple/array of float point numbers. e.g. (1400.0, 1550.0)
- It must be called after a match with the required parameters to get the new ratings of the players.

#### elo_with_points() method

- This is the rating update formula which takes into consideration the individual points scored by the players.
- It takes 5 arguments:
  1. rating_a: Current rating of player A. (float)
  2. rating_b: Current rating of player B. (float)
  3. points_a: Points scored by player A. (float)
  4. points_b: Points scored by player B. (float)
  5. method: Method to use for consideration of points scored. (int, default 2)
- method must $\in$ {0, 1, 2} where,
  - method = 0 $\implies$ Just consider the outcome of a match.
  - method = 1 $\implies$ Consider fraction of points at the place of $S_a$.
  - method = 2 $\implies$ Uses the L factor for consideration of points.
- It returns the new ratings of the players in the form of tuple/array of float point numbers. e.g. (1400.0, 1550.0)
- It must be called after a match with the required parameters to get the new ratings of the players.

### Dependencies

- Python: No extra libraries used.
- Java: No extra libraries used.
