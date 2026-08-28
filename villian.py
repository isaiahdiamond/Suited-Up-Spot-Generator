'''Villain response modelling: how often a bet gets through, what continues
against it, and the EV of betting versus checking.'''
from __future__ import annotations

import cards
import evaluator
import ranges
import equity

DEFENSE_MULTIPLE = 1.6


def min_def_freq(pot: float, bet_size: float) -> float:
    '''Fraction of his range villain must continue with to stop a bet
    profiting with any two cards. `pot` EXCLUDES the bet.'''
    fold_equity = bet_size / (pot + bet_size)
    return 1 - fold_equity


def fold_frequency(pot: float, bet_size: float) -> float:
    '''How often villain folds to a bet of `bet_size` into `pot`.'''
    return bet_size / (pot + bet_size)


def defence(pot: float, bet_size: float) -> tuple[float, float]:
    '''Returns (defended_fraction, fold_frequency) after applying
    DEFENSE_MULTIPLE to the minimum defence frequency.'''
    defended = min(1.0, min_def_freq(pot, bet_size) * DEFENSE_MULTIPLE)
    return defended, 1 - defended


def continuing_range(board: tuple, villain_combos: list,
                     defended: float) -> list:
    '''Villain continues with his strongest `defended` fraction. Ranked by
    made-hand strength on the flop rather than equity — far cheaper, and
    near-identical ordering.'''
    if not villain_combos:
        return []

    ranked = []
    for combo in villain_combos:
        five = tuple(combo) + tuple(board)
        ranked.append((evaluator.evaluate_hand(five), combo))

    ranked.sort(key=lambda pair: pair[0], reverse=True)

    keep = max(1, round(len(ranked) * defended))
    return [combo for _, combo in ranked[:keep]]


def ev_of_bet(pot: float, bet: float, eq_vs_continuing: float,
              fold_freq: float) -> float:
    '''EV in bb of betting `bet` into `pot`. Villain folds `fold_freq` of the
    time; when he continues you win pot+bet with `eq_vs_continuing`.'''
    win_when_called = eq_vs_continuing * (pot + bet)
    lose_when_called = (1 - eq_vs_continuing) * bet
    return fold_freq * pot + (1 - fold_freq) * (win_when_called - lose_when_called)


def ev_of_check(pot: float, equity_vs_range: float) -> float:
    '''EV in bb of checking — your share of the existing pot, risking nothing.'''
    return equity_vs_range * pot


def best_action_unbet(hero_hand: tuple, board: tuple, villain_combos: list,
                      pot: float, bet_fraction: float = 0.67,
                      samples: int = 2000) -> dict:
    '''Hero is first to act or facing a check: bet or check?'''
    bet = round(pot * bet_fraction, 2)
    defended, f = defence(pot, bet)
    cont = continuing_range(board, villain_combos, defended)

    eq_full = equity.estimate_equity(board, hero_hand, villain_combos, samples)
    eq_cont = equity.estimate_equity(board, hero_hand, cont, samples)

    evs = {
        'bet':   ev_of_bet(pot, bet, eq_cont, f),
        'check': ev_of_check(pot, eq_full),
    }
    return _verdict(evs, {'bet_size': bet, 'fold_freq': f,
                          'equity': eq_full, 'equity_vs_continuing': eq_cont},
                    raise_edge=0.75)


def best_action_facing_bet(hero_hand: tuple, board: tuple, villain_combos: list,
                           pot: float, to_call: float,
                           raise_multiple: float = 3.0,
                           samples: int = 2000) -> dict:
    '''Hero faces a bet: fold, call, or raise? `pot` INCLUDES villain's bet.'''
    eq_full = equity.estimate_equity(board, hero_hand, villain_combos, samples)

    raise_to = round(to_call * raise_multiple, 2)
    extra = raise_to - to_call
    defended, f = defence(pot, extra)
    cont = continuing_range(board, villain_combos, defended)
    eq_cont = equity.estimate_equity(board, hero_hand, cont, samples)

    evs = {
        'fold':  0.0,
        'call':  eq_full * pot - (1 - eq_full) * to_call,
        'raise': ev_of_bet(pot, raise_to, eq_cont, f),
    }
    return _verdict(evs, {'raise_to': raise_to, 'fold_freq': f,
                          'equity': eq_full, 'equity_vs_continuing': eq_cont,
                          'required_equity': to_call / (pot + to_call)})


def _verdict(evs: dict, extras: dict, raise_edge: float = 5.0) -> dict:
    ordered = sorted(evs.items(), key=lambda pair: pair[1], reverse=True)
    best, best_ev = ordered[0]
    second, second_ev = ordered[1] if len(ordered) > 1 else (best, best_ev)

    if best in ('raise', 'bet') and (best_ev - second_ev) < raise_edge:
        best, best_ev, second_ev = second, second_ev, best_ev

    result = {
        'best_action': best,
        'evs': {k: round(v, 3) for k, v in evs.items()},
        'margin': round(best_ev - second_ev, 3),
    }
    result.update({k: (round(v, 4) if isinstance(v, float) else v)
                   for k, v in extras.items()})
    return result