# Module 5: Pot Odds & Grading. 🃏

**Status**: Completed ✅

### Pot Odds
`required_equity()` answers one question: how often do you need to win for calling to
break even? You're risking your call to win the pot plus your own call, so the answer is
`call / (pot + call)`. The pot here includes the bet you're facing — the same number a
player sees on screen.

A half-pot bet needs 25% equity to call. A pot-sized bet needs 33%. Those are the numbers
players memorize, and this function reproduces them.

`ev_of_call()` puts it in big blinds instead of percentages. You win the pot when you're
ahead and lose your call when you're not, so it's
`(equity × pot) - ((1 - equity) × call)`. At exactly the required equity it returns 0,
which is the same break-even point the pot odds formula gives.

### Grading a Flop Decision
`grade_flop()` compares your equity against what you need. The difference is the **margin**:
positive means calling is profitable, negative means folding is.

Margins very close to zero mean both actions are basically break-even, so there's a
tolerance band (default ±2%) where calling and folding are both graded correct.

The function returns the verdict, the margin, the required equity, and your actual equity —
everything the explanation needs, so the numbers come from the math rather than being
re-derived later.

### Grading a Preflop Decision
Preflop needs no equity calculation at all. `grade_preflop()` labels your two cards using
the hand evaluator, looks up the chart for your position and the action you're facing, and
finds where your hand sits: raise, call, mixed, or absent (fold).

Mixed cells matter here. A hand played two ways — raise 26% of the time, limp 74% — has
two correct answers, so the function returns a set of acceptable actions rather than one.

### Verification
`check_grading.py` checks the pot odds formula against standard bet sizes, confirms the
EV formula agrees with the pot odds break-even point, tests the tolerance band from both
sides, and checks preflop grading across all three chart types.

### How to run
Simply run `python check_grading.py`.