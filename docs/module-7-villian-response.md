# Module 7: Villain Response & EV. 🃏

**Status**: Completed ✅

### Why This Exists
Pot odds answer one question: is calling profitable? They say nothing about
betting or raising, because there's no price to compare against until someone
has bet. Roughly half of all flop situations have you either first to act or
facing a check — this module is what makes those gradeable.

### How Often a Bet Gets Through
If someone folds too often against a bet, betting any two cards prints money.
The frequency where that stops being true is the **minimum defence frequency**,
and it falls straight out of the bet size: risking a bet to win the pot breaks
even when it works often enough to cover the times it doesn't.

A pot-sized bet needs to work half the time. A half-pot bet needs a third.

### Which Hands Keep Playing
`continuing_range()` assumes the opponent keeps his strongest hands and folds
the rest. Every hand in his range gets run through the hand evaluator on that
board, sorted, and the top slice kept.

Ranking by made-hand strength rather than equity is a deliberate trade — it's
one evaluation per hand instead of a full simulation, and the ordering comes
out nearly the same.

### What Betting Is Worth
`ev_of_bet()` splits on whether the opponent folds. When he does, you win the
pot. When he doesn't, you win a bigger pot when you're ahead and lose your bet
when you're not. Checking is worth your share of the pot as it stands, risking
nothing.

`best_action_unbet()` and `best_action_facing_bet()` compute the options for
each situation and return the best one along with how far ahead of the
second-best it is. That gap is the difficulty score — a large one means the
decision is obvious, a small one means it's genuinely close.

### Two Honest Simplifications
This model stops at the flop. It never charges a bet or raise for the hands
that go badly on later streets, which makes aggression look better than it is.
Two constants compensate:

**`DEFENSE_MULTIPLE`** makes the opponent continue more than the bare minimum,
since real players do. **`raise_edge`** requires a bet or raise to win by a
clear margin rather than by a hair.

Both are tuned so the resulting mix of actions resembles reasonable play. They
are calibrated numbers, not derived ones — this is a trainer that teaches
sound, slightly conservative flop play, and it is not a solver.

### Verification
Three hundred generated spots were checked for how often each action came out
best, and individually against how a competent player would play them.

### How to run
Import `villian` and call `best_action_facing_bet()` or `best_action_unbet()`
with a hand, a board, and an opponent's range.