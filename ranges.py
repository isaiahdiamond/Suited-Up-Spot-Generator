'''This file is about finding ranges from player hands and getting the correct chart depending on the hero's position'''
import cards
import charts
# ------------- Builder Functions --------------
def build_combo_map():
    '''This function builds a map from each label to each card combo.'''
    combo_map = {}

    for combo in cards.ALL_COMBOS:
        label = cards.label_hand(combo)
        combo_map[combo] = label
    
    master_map = {}
    
    for combo, label in combo_map.items():
        if label not in master_map:
            master_map[label] = []
        master_map[label].append(combo)

    return master_map

# ----- constants ------- 
COMBO_MAP = build_combo_map()
VALUE_TO_RANK = {v: k for k, v in cards.CARD_VALUE.items()}
CHARTS = {
    'rfi':     charts.RFI_6MAX,
    'vs_rfi':  charts.VS_RFI_6MAX,
    'vs_3bet': charts.VS_3BET_6MAX,
}

# ------ Main functions ------------ 
def parse_range(string:str) -> set:
    '''This functiont takes in a string like "22+" and returns the set of ranges that the string describes '''
    final = []
    range_list = string.split(',')
    
    for item in range_list:
        item = item.strip()
        
        if item.endswith('+'):
            clean_text = item.replace('+','')
            
            if clean_text[0] == clean_text[1]:
                start_rank = clean_text[0]
                start_value = cards.CARD_VALUE[start_rank]

                for rank_label, num_value in cards.CARD_VALUE.items():
                    if num_value >= start_value:
                        pocker_pair = rank_label + rank_label
                        final.append(pocker_pair)         
            
            elif len(clean_text) >= 2:
                high_card = clean_text[0] 
                low_card = clean_text[1]  
                
                suit_modifier = clean_text[2:] if len(clean_text) > 2 else ""
                
                if high_card in cards.CARD_VALUE and low_card in cards.CARD_VALUE:
                    high_val = cards.CARD_VALUE[high_card]
                    low_val = cards.CARD_VALUE[low_card]
                    
                    for val in range(low_val, high_val):
                        low_rank_label = VALUE_TO_RANK[val]
                        
                        label = high_card + low_rank_label + suit_modifier
                        final.append(label)
        else:
            if item:
                final.append(item)
    
    final_labels = set(final) 
    return final_labels

def labels_to_combos(labels:set) -> list:
    '''This function takes in the output from parse_range() and returns the hand combos from that range'''
    combos = []
    for label in labels:
        combos.append(COMBO_MAP[label])
    
    master = []
    for sublist in combos:
        for combo in sublist:
            master.append(combo)

    return master

def get_chart(position:str, action:str):
    '''This function takes a position and action and returns the approiate chart.'''
    position = position.upper()
    if position == 'UTG' and action == 'vs_rfi':
        return 'No UTG chart for this action.'
    
    if position == 'BB' and action == 'rfi':
        return 'No BB chart for this action.'
    return CHARTS[action].get(position)

