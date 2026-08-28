# The Poker Trainer Engine 🃏
This is the math engine behind my mobile app, Poker Trainer - SuitedUp. It generates random poker scenarios and grades the mathematically optimal decision a player should take.

This code and repo is not AI generated, and all math is verified by hand and 3rd party checks.

### Module 1:
Covers generating a deck, all possible hand combinations, card removal, and combinatorics.

Check it out [here](docs/module-1-cards.md).

### Module 2:
Covers turning random cards into the game of poker. It turns 7 random cards into poker ranks ie: Flush, Two-Pair, etc.

Check it out [here](docs/module-2-evaluator.md).

### Module 3:
Covers calculating exact and estimated equity in a specific poker hand. It takes a flop, the hero's cards, and the villain's range to calculate the hero's equity.
It serves as the foundational piece for grading mathematically optimal decisions in the game.

Check it out [here](docs/module-3-equity.md).

### Module 4:
Covers preflop ranges. It expands poker shorthand like `"22+, ATs+, KQo"` into the actual hands it describes, converts those into card combinations, and looks up the right preflop chart for a given position and action. This is what feeds villain's range into the equity engine, and what the preflop trainer grades against.

Check it out [here](docs/module-4-ranges.md).

### Module 5:
Covers pot odds and decision grading. It works out how much equity a call needs to break even, converts that into expected value in big blinds, and grades a decision against it. Preflop decisions are graded straight off the charts instead — including hands that are played more than one way, where two actions are both correct.

Check it out [here](docs/module-5-grading.md).

### Module 6:
Covers spot generation. It deals a table, walks the preflop action seat by
seat with each opponent's decision coming from the same charts the trainer
grades against, and stops when the action reaches you — that's a spot. It
then carries on past your turn, deals the flop, and lets someone bet, which
gives the flop trainer its situations. Anything the engine can't grade gets
thrown away rather than stored.

Check it out [here](docs/module-6-spot-generator.md).


### Module 7:
Covers what happens after you bet. It works out how often an opponent has to
keep playing to stop a bet from printing money, which of his hands those are,
and what betting or raising is worth against them. That's what lets the flop
trainer grade aggression instead of only call-or-fold.

Check it out [here](docs/module-7-villain-response.md).


### How to run"
python check_cards.py
python check_evaluator.py
python check_equity.py
python check_ranges.py
python check_grading.py

### Modules:
1. Cards, Combinations, & Removal ✅
2. Rules of the game (Hand Evaluation) ✅
3. Equity ✅
4. Ranges ✅
5. Pot Odds & Grading ✅
6. Spot Generator ✅
7. Villian Response & EV ✅