# SuitedUp engine

This is the math engine behind SuitedUp, my mobile poker trainer. It deals random poker spots and works out the correct decision for each one, so the app can grade your play instantly.

I wrote the code myself. The math is checked by hand and against third-party tools.
[Check out the iOS app](https://suitedup.app)

<img width="1180" height="612" alt="Screenshot 2026-10-15 at 12 15 11 PM" src="https://github.com/user-attachments/assets/36dedd86-604a-4bd1-a8fb-276b25ddc335" />

## What it does

1. [Cards and combinations](docs/module-1-cards.md): builds the deck and counts hand combinations, including card removal.
2. [Hand evaluation](docs/module-2-evaluator.md): turns 7 cards into a poker hand like a flush or two pair.
3. [Equity](docs/module-3-equity.md): calculates how often your hand wins against an opponent's range on a given flop, exactly or by simulation.
4. [Ranges](docs/module-4-ranges.md): expands shorthand like `22+, ATs+, KQo` into real hands and looks up the right preflop chart for each position.
5. [Pot odds and grading](docs/module-5-grading.md): works out the equity a call needs, converts it to expected value in big blinds, and grades the decision. Preflop spots are graded from the charts, and some hands have two correct plays.
6. [Spot generation](docs/module-6-spot-generator.md): deals a table and plays each opponent from the same charts until the action reaches you. For flop spots it keeps going, deals the flop, and has someone bet. Spots the engine can't grade get thrown out.
7. [Opponent response](docs/module-7-villain-response.md): works out how often an opponent has to continue against a bet, which hands he continues with, and what betting or raising is worth. This lets the flop trainer grade bets and raises as well as calls and folds.

## Run it yourself

Clone the repo and install the dependencies:

```bash
git clone https://github.com/isaiahdiamond/Suited-Up-Spot-Generator.git
cd Suited-Up-Spot-Generator
pip install -r requirements.txt
```

Then pass the number of spots you want:

```bash
python preflop_gen.py 100
python flop_gen.py 100
```
