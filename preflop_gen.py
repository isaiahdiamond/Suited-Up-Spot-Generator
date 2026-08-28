'''This script deals with generating situations for preflop play that feeds that app.'''
import cards
import random
import ranges
import grading

random.seed(21)

POSITIONS = ['UTG','HJ','CO','BTN','SB','BB']

def deal_table() -> dict:
    '''This function deals out flop and 2 cards to each player depending on table size.'''
    draw = random.sample(cards.DECK, 15)
    scenario = {'Flop':tuple(draw[:3]), 'UTG': tuple(draw[3:5]),'HJ': tuple(draw[5:7]),'CO':tuple(draw[7:9]),'BTN':tuple(draw[9:11]),'SB':tuple(draw[11:13]),'BB':tuple(draw[13:15])}
    return scenario

def npc_decision(hand:tuple,position:str, facing:str)-> str:
    '''This function determines the decision our NPC will make preflop based on our charts.'''
    random_float = round(random.random(),4)
    
    chart = ranges.get_chart(position, facing)
    hand_label = cards.label_hand(hand)
    if not isinstance(chart, dict):
        return 'fold'
    
    if hand_label in chart['mixed']:
        total = 0
        options = chart['mixed'][hand_label]
        decision = 'fold'   
        for key, value in options.items():
            total = value + total
            if random_float <= total:
                decision = key
                break
    elif hand_label in ranges.parse_range(chart['raise']):
        decision = 'raise'
    elif hand_label in ranges.parse_range(chart.get('call','')):
        decision = 'call'
    else:
        decision = 'fold'
    
    return decision

def simulate_preflop(table:dict, hero_pos:str) -> dict:
    '''This function simulates preflop play with NPC's up to the users position'''
    hero_hand = table[hero_pos]
    hero_index = POSITIONS.index(hero_pos)
    earlier_positions = POSITIONS[:hero_index]

    pot = 1.5
    to_call = 1
    committed = {'UTG': 0, 'HJ': 0, 'CO': 0, 'BTN': 0, 'SB': 0.5, 'BB': 1}

    actions = []
    players_in = []
    raises = 0
    action_faced = 'rfi'
    last_agro = None
    for position in earlier_positions:
        npc_hand = table[position]
        
        if raises == 0:
            action_faced = 'rfi'
        elif raises == 1:
            action_faced = 'vs_rfi'
        else:
            action_faced = 'vs_3bet'
        
        npc_play = npc_decision(npc_hand,position,action_faced)
        if npc_play == 'raise':
            if raises == 0:
                to_call = 3
            else:
                to_call = 10
            owed = to_call - committed[position]
            pot += owed
            committed[position] = to_call
            raises += 1
            players_in.append(position)
            last_agro = position 
        elif npc_play == 'call':
            owed = to_call - committed[position]
            players_in.append(position)
            pot += owed
            committed[position] = to_call
        
        actions.append((position, npc_play))
    
    if raises == 0:
        action_faced = 'rfi'
    elif raises == 1:
        action_faced = 'vs_rfi'
    else:
        action_faced = 'vs_3bet'
    
    return {'hero_pos':hero_pos,'hero_hand':hero_hand, 'action_faced':action_faced, 'pot':pot,'to_call':to_call, 'players_in':players_in, 'actions':actions , 'committed':committed, 'raises':raises, 'last_agro': last_agro}

def preflop_spot_generator(n:int) -> list:
    '''This function loops over n and produces n amount of preflop spots'''
    saved = []
    for i in range(n):
        spot_id = i
        hero_pos = random.choice(POSITIONS)
        table = deal_table()
        situation = simulate_preflop(table,hero_pos)

        if situation['hero_pos'] == 'BB' and situation['action_faced'] == 'rfi':
            continue

        hand_label = cards.label_hand(table[hero_pos])    
        chart = ranges.get_chart(hero_pos, situation['action_faced'])
        if not isinstance(chart, dict):
            continue
        
        if hand_label in chart['mixed']:
            difficulty = 1 - abs((2 * chart['mixed'][hand_label].get('raise', 0)) - 1)
            correct_actions = list(chart['mixed'][hand_label])
        elif hand_label in ranges.parse_range(chart['raise']):
            difficulty = 0
            correct_actions = ['raise']
        elif hand_label in ranges.parse_range(chart.get('call', '')):
            difficulty = 0
            correct_actions = ['call']
        else:
            difficulty = 0
            correct_actions = ['fold']

        situation['correct_actions'] = correct_actions
        situation['hero_committed'] = {'SB': 0.5, 'BB': 1}.get(hero_pos, 0)
        situation['difficulty'] = difficulty
        situation['spot_id'] = spot_id
        
        saved.append(situation)

    return saved 

def resume_preflop(table:dict, spot:dict):
    hero_pos = spot['hero_pos']
    hero_faced = spot['action_faced']
    hero_hand = table[hero_pos]
    to_call = spot['to_call']
    pot = spot['pot']
    raises = spot['raises']
    last_agro = spot['last_agro']

    players_in = spot['players_in'].copy()
    actions = spot['actions'].copy()
    committed = spot['committed'].copy()

    later_positions = POSITIONS[POSITIONS.index(hero_pos) + 1:]

    hero_correct = npc_decision(hero_hand, hero_pos, hero_faced)

    if hero_correct == 'fold':
        actions.append((hero_pos, hero_correct))
        return None
    
    
    if hero_correct == 'raise':
        if raises == 0:
            to_call = 3
        else:
            to_call = 10
        owed = to_call - committed[hero_pos]
        pot += owed
        committed[hero_pos] = to_call
        raises += 1
        players_in.append(hero_pos)
        actions.append((hero_pos ,hero_correct))
        last_agro = hero_pos
    elif hero_correct == 'call':
        owed = to_call - committed[hero_pos]
        players_in.append(hero_pos)
        pot += owed
        committed[hero_pos] = to_call
        actions.append((hero_pos,hero_correct))
    
    for position in later_positions:
        npc_hand = table[position]
        
        if raises == 0:
            action_faced = 'rfi'
        elif raises == 1:
            action_faced = 'vs_rfi'
        else:
            action_faced = 'vs_3bet'
        
        npc_play = npc_decision(npc_hand,position,action_faced)
        if npc_play == 'raise':
            if raises == 0:
                to_call = 3
            else:
                to_call = 10
            owed = to_call - committed[position]
            pot += owed
            committed[position] = to_call
            raises += 1
            players_in.append(position)
            last_agro = position
        elif npc_play == 'call':
            owed = to_call - committed[position]
            players_in.append(position)
            pot += owed
            committed[position] = to_call
        
        actions.append((position, npc_play))

        
    return {'players_in': players_in, 'pot':pot, 'actions':actions, 'last_agro':last_agro}
