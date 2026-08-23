'''This file stores the functions that calculate pot odds, ev for calling, and grades preflop and flop decisions'''
import cards
import ranges

def required_equity(pot:float, call:float):
    '''This function calculates the required equity to call a spot. The pot includes the villians bet'''
    req_eq = call / (pot + call)
    return round(req_eq, 3)

def ev_of_call(pot:float,call:float,eq:float):
    '''This function calculates the expected value of a call and returns the value in BB's'''
    ev = (eq * pot) - ((1 - eq) * call)
    return ev

def grade_flop(equity:float,pot:float,call:float, action:str):
    '''This function grades a flop decision based on equity and pot odds'''
    required_eq = required_equity(pot,call)
    margin = equity - required_eq
    tolerence = .02
    
    if abs(margin) < tolerence:
        right_action = {'call','fold'}
    elif margin > 0:
        right_action = {'call'}
    else:
        right_action = {'fold'}
    
    if action in right_action:
        return ('correct', round(margin,3), required_eq, equity)
    else:
        return ('incorrect', round(margin,3), required_eq, equity)
    
def grade_preflop(hand:tuple, position:str, action_faced:str, user_action):
    '''This function grades preflop decisions from users agaisnt our charts. Returning either correct or incorrect.'''
    hand_label = cards.label_hand(hand)
    chart = ranges.get_chart(position, action_faced)

    if hand_label in chart['mixed']:
        correct_action = set(chart['mixed'][hand_label])
    elif hand_label in ranges.parse_range(chart['raise']):
        correct_action = {'raise'}
    elif hand_label in ranges.parse_range(chart.get('call','')):
        correct_action = {'call'}
    else:
        correct_action = {'fold'}
    
    if user_action in correct_action:
        return ('correct', correct_action)
    else:
        return ('incorrect', correct_action)
    