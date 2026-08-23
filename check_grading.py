import cards
import grading
from check_cards import helper_check

if __name__ == "__main__":

    # Required Equity Checks
    check_1 = grading.required_equity(4,1)
    check_2 = grading.required_equity(3,1)
    check_3 = grading.required_equity(7,3)
    check_4 = grading.required_equity(2,1)
    check_5 = grading.required_equity(12,4.5)

    # Ev of call checks
    check_6 = grading.ev_of_call(15,5,.4)
    check_7 = grading.ev_of_call(15,5,.25)
    check_8 = grading.ev_of_call(15,5,.1)

    # Grade Flop Checks
    check_10 = grading.grade_flop(.4,15,5,'call')
    check_11 = grading.grade_flop(.4,15,5,'fold')
    check_12 = grading.grade_flop(.1,15,5,'fold')
    check_13 = grading.grade_flop(.1,15,5,'call')

    # Grade Preflop Checks
    check_14 = grading.grade_preflop(('As','Ah'),'UTG','rfi','raise')
    check_15 = grading.grade_preflop(('Qs','9s'),'UTG','rfi','raise')
    check_16 = grading.grade_preflop(('As','Ah'),'SB','rfi','call')



    summary = []

    summary.append(helper_check(.2,check_1,"Required Equity Check 1"))
    summary.append(helper_check(.25,check_2,"Required Equity Check 2"))
    summary.append(helper_check(.3,check_3,"Required Equity Check 3"))
    summary.append(helper_check(.333,check_4,"Required Equity Check 4"))
    summary.append(helper_check(.273,check_5,"Required Equity Check 5"))
    
    summary.append(helper_check(3,check_6,"EV of call Check 1"))
    summary.append(helper_check(0,check_7,"EV of call Check 2"))
    summary.append(helper_check(-3,check_8,"EV of call Check 3"))

    summary.append(helper_check(('correct', .15),check_10,"Grade Flop Check 1"))
    summary.append(helper_check(('incorrect', .15),check_11,"Grade Flop Check 2"))
    summary.append(helper_check(('correct', -.15),check_12,"Grade Flop Check 3"))
    summary.append(helper_check(('incorrect', -.15),check_13,"Grade Flop Check 1"))

    summary.append(helper_check(('correct', {'raise'}),check_14,"Grade Preflop Check 1"))
    summary.append(helper_check(('incorrect', {'fold'}),check_15,"Grade Preflop Check 2"))
    summary.append(helper_check(('correct', {'raise','call'}),check_16,"Grade Preflop Check 3"))

    print(f'Equity Test: {sum(summary)} of {len(summary)} passed!')