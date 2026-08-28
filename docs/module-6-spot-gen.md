# Module 6: Spot Generator. 🃏

**Status**: Completed ✅

### Dealing a Table
`deal_table()` draws fifteen cards in one go — three for the flop and two for
each of the six seats. One draw rather than several means a card can never
appear in two places, and the flop sits unused until the hand actually gets
there.

### Opponents That Play the Charts
`npc_decision()` gives one seat one action. It looks the hand up in that
position's chart and, for hands the chart plays more than one way, rolls a
random number against the frequencies to pick which. A hand raised 26% of the
time gets raised 26% of the time.

The charts do double duty here. Preflop they're the answer key; in the
generator they drive the opponents. That means the action sequences that come
out are realistically distributed for free — early positions open rarely, the
button opens often, and most pots end up heads-up or three-way.

### Walking the Action
`simulate_preflop()` starts at UTG and works around the table, tracking who's
still in, what's in the pot, and how many raises have gone in. That raise
count is what decides which chart the next seat gets asked for — nobody's
opened, someone has, or someone's three-bet.

It stops when the action reaches you. Whatever happened is the situation.

`resume_preflop()` picks up from there: you act according to the chart, the
seats behind you respond, and what comes out is the group of players who see
a flop and who among them showed the most strength.

### The Flop
`simulate_flop()` uses postflop order, which is not preflop order — the blinds
act first and the button acts last, no matter who raised. Whoever showed
strength preflop bets about two thirds of the pot most of the time and
everyone else checks; in a pot nobody raised, the first player to act does the
betting instead, less often.

### Throwing Spots Away
Not every hand produces a question. Hands where the correct play is to fold
never reach a flop, some positions have no chart for the situation they end up
in, and a hand where you'd be the one opening the betting needs Module 7 to
grade. All of those get discarded and the generator deals again.

### Verification
The generator was checked by running ten thousand hands and comparing how
often each seat opened against what the charts say it should — every position
landed within half a percent.

### How to run
`python -c "import preflop_gen; preflop_gen.preflop_spot_generator(20)"`, or
`flop_gen.flop_spot_generator(20)` for flop spots.