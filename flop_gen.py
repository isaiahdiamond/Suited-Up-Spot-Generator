'''Flop spot generation. Runs the preflop simulation forward to the flop,
puts in a bet, solves the decision hero faces, and stores the result.'''
from __future__ import annotations

import json
import os
import random

import cards
import ranges
import preflop_gen
import villian


# --- Constants ---
FLOP_ORDER = ['SB', 'BB', 'UTG', 'HJ', 'CO', 'BTN']
CBET_FREQ = 0.65          # how often the preflop aggressor c-bets
LIMPED_BET_FREQ = 0.30    # how often first-to-act bets a limped pot
BET_FRACTION = 0.67       # bet size as a fraction of the pot

def preflop_answer(hero_hand: tuple, hero_pos: str, action_faced: str) -> dict | None:
    '''The chart's verdict on hero's preflop decision. None if no chart covers it.'''
    chart = ranges.get_chart(hero_pos, action_faced)
    if not isinstance(chart, dict):
        return None

    label = cards.label_hand(hero_hand)

    if label in chart['mixed']:
        freq = chart['mixed'][label].get('raise', 0)
        return {'correct_actions': list(chart['mixed'][label]),
                'difficulty': 1 - abs(2 * freq - 1)}
    if label in ranges.parse_range(chart['raise']):
        return {'correct_actions': ['raise'], 'difficulty': 0}
    if label in ranges.parse_range(chart.get('call', '')):
        return {'correct_actions': ['call'], 'difficulty': 0}
    return {'correct_actions': ['fold'], 'difficulty': 0}

def villain_range_combos(position: str, action_faced: str,
                         known_cards: tuple) -> list:
    '''Every combo `position` continues with from its chart, minus dead cards.'''
    chart = ranges.get_chart(position, action_faced)
    if not isinstance(chart, dict):
        return []

    labels = set()
    labels |= ranges.parse_range(chart.get('raise', ''))
    labels |= ranges.parse_range(chart.get('call', ''))
    labels |= set(chart.get('mixed', {}))

    combos = ranges.labels_to_combos(labels)
    return cards.find_combos_left(combos, known_cards=known_cards)


def simulate_flop(spot: dict, resumed: dict, board: tuple) -> dict | None:
    '''Run the flop betting up to hero's turn. None if there's nothing to grade.'''
    hero_pos = spot['hero_pos']
    players = [p for p in FLOP_ORDER if p in resumed['players_in']]
    if hero_pos not in players or len(players) < 2:
        return None

    agro = resumed['last_agro']
    bettor = agro if agro in players else players[0]
    freq = CBET_FREQ if agro in players else LIMPED_BET_FREQ

    pot = resumed['pot']
    bet = round(pot * BET_FRACTION, 2)

    if random.random() >= freq:
        return {'board': board, 'players_in': players, 'pot': pot,
                'to_call': 0.0, 'bettor': None, 'hero_faces': 'check'}

    if bettor == hero_pos:
        return None    # hero would be the one betting; no decision to solve

    return {'board': board, 'players_in': players, 'pot': round(pot + bet, 2),
            'to_call': bet, 'bettor': bettor, 'hero_faces': 'bet'}


def flop_spot_generator(n: int, samples: int = 2000) -> list:
    '''Generate n fully-solved flop spots.'''
    saved = []
    attempts = 0

    while len(saved) < n and attempts < n * 30:
        attempts += 1

        table = preflop_gen.deal_table()
        hero_pos = random.choice(preflop_gen.POSITIONS)
        spot = preflop_gen.simulate_preflop(table, hero_pos)

        resumed = preflop_gen.resume_preflop(table, spot)
        if resumed is None:
            continue

        pre = preflop_answer(table[hero_pos], hero_pos, spot['action_faced'])
        if pre is None:
            continue

        board = table['Flop']
        flop = simulate_flop(spot, resumed, board)
        if flop is None:
            continue

        hero_hand = table[hero_pos]
        known = tuple(hero_hand) + tuple(board)

        combos = []
        for p in flop['players_in']:
            if p != hero_pos:
                combos.extend(
                    villain_range_combos(p, spot['action_faced'], known))
        if not combos:
            continue

        if flop['hero_faces'] == 'bet':
            solved = villian.best_action_facing_bet(
                hero_hand, board, combos, flop['pot'], flop['to_call'],
                samples=samples)
        else:
            solved = villian.best_action_unbet(
                hero_hand, board, combos, flop['pot'], samples=samples)

        row = {
            'spot_id': len(saved),
            'hero_pos': hero_pos,
            'hero_hand': list(hero_hand),
            'preflop_correct_actions': pre['correct_actions'],
            'preflop_difficulty': pre['difficulty'],
            'preflop_pot': spot['pot'],
            'preflop_to_call': spot['to_call'],
            'board': list(board),
            'preflop_actions': resumed['actions'],
            'players_in': flop['players_in'],
            'pot': flop['pot'],
            'to_call': flop['to_call'],
            'bettor': flop['bettor'],
            'hero_faces': flop['hero_faces'],
            'explanation': '',
        }
        row.update(solved)
        saved.append(row)

    return saved

