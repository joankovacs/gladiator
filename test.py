from collections import OrderedDict, namedtuple
from math import floor
from statistics import mean
import os
from blessed import Terminal
import resources as rs

term = Terminal()
#########################################################################################
#TEST ZONE

































#OLD TESTS
#########################################################################################
from display import tab_header

l1 = ['ATTRIBUTES', 'EQUIPMENT', 'SKILLS'] #chargen menu
l2 = ['FIGHT!', 'INVENTORY'] #main menu before first fight
l3 = ['FIGHT!', 'INVENTORY', 'SHOP', 'IMPROVEMENT', 'GAME DATA'] #main menu
l_4 = ['MAIN MENU', 'SKILLS', 'ABILITIES', 'CHARACTER INFO'] #Character improvement. implement?
l_5 = ['MAIN MENU', 'INVENTORY', 'EQUIPMENT', 'CHARACTER INFO'] #Inventory.  implement?


lists = [l1, l2, l3, l_4, l_5]

#---------------------------------------------

def tab_cursor_logic(position, all_positions):
    if position==all_positions[-1]:
        return 0
    return position+1

def functional_tabs(tab_list):
    tab_cursor = 0
    tab_all_positions = [i for i in range(len(tab_list))]

    with term.cbreak(), term.hidden_cursor():
        tab_header(tab_list, tab_cursor)
        inp = term.inkey()

        while inp != 'q':
            # interpret first input
            if inp.name=='KEY_TAB':
                tab_cursor = tab_cursor_logic(tab_cursor, tab_all_positions)
                tab_header(tab_list, tab_cursor)
                
            #cycle input indefinitely
            inp = None
            inp = term.inkey()


#functional_tabs(l3)


'''
#load in display frame so that the file isn't continuously read
DISPLAY_FRAME = []
with open('display_frame_tall.txt', 'r') as f:
    for line in f.read().splitlines():
        DISPLAY_FRAME.append(line)
DISPLAY_COORDS = {
    'title':{'x':12, 'y':10},
    'title_max':{'width':55, 'height':1},
    'body':{'x':13, 'y':13},
    'body_max':{'width':53, 'height':13},
    'footnote':{'x':13, 'y':29},
    'footnote_max':{'width':53, 'height':1},
}

#Dumped code
###############################################################################
#[1] DATA STRUCTURES - all current structures obsolete via CLASS process

#key input limits.  Nontab is for all keys that are used within a screen.
nontab_program_keys = ['KEY_UP', 'KEY_DOWN', 'KEY_LEFT', 'KEY_RIGHT', 'KEY_ENTER']
vertical_input = ['KEY_UP', 'KEY_DOWN']
attribute_input = ['KEY_LEFT', 'KEY_RIGHT']

#read-in from resources
attributes = rs.class_init_ATT(rs.attributes_read_only)
equipment = rs.class_init_EQP(rs.equipment_read_only)
skills = rs.class_init_SKL(rs.skills_read_only)

#chargen limits for initial selections
remaining_points = {
    'attributes':5,
    'equipment':7,
    'skills':1,
}
'''
###############################################################################
#[3] ATTRIBUTE, EQUIPMENT, SKILL SELECTION
#Currently obsolete via CLASS process

def attribute_horizontal_logic(attribute, remaining_points, attempt):
    '''
    Logic for increasing or decreasing base attributes at game start.
        *attribute: Expects the named tuple specific to the attribute
        *remaining_points: Points left to spend on attributes
        *attempt: increase or decrease (KEY_RIGHT or KEY_LEFT respectively)
    NOTE: 'all_positions' is the same for all attributes. The range an attri-
    bute can be at game start is 1 through 4 (int).  This is hardcoded.
    NOTE: This returns a tuple for tuple assignment of 
        (attribute's value, remaining_points) because both values are changed.
    '''
    att_val = attribute.value
    no_change = (att_val, remaining_points)
    
    if attempt == 'KEY_LEFT':
        if attribute.value == 1:
            return no_change
        else:
            return (att_val-1, remaining_points+1)
    if attempt == 'KEY_RIGHT':
        if attribute.value == 4:
            return no_change
        elif remaining_points == 0:
            return no_change
        else:
            return (att_val+1, remaining_points-1)

def attribute_selection(remaining_points):
    '''
    Loop for attribute selection logic.
    '''
    cursor = 0
    all_positions = [i for i in range(len(attributes))]
    
    with term.cbreak(), term.hidden_cursor():
        dsp.attributes_display(cursor, attributes, remaining_points)
        inp = term.inkey()

        while inp != 'q':
            # interpret first input
            if inp.name in vertical_input:
                cursor = vertical_cursor_logic(cursor, all_positions, inp.name)
            if inp.name in attribute_input:
                attributes[cursor].value, remaining_points = attribute_horizontal_logic(attributes[cursor], remaining_points, inp.name)

            #cycle input indefinitely
            dsp.attributes_display(cursor, attributes, remaining_points)
            inp = term.inkey()

def equipment_selection(remaining_points):
    '''
    Loop for equipment selection logic.
    '''
    cursor = 0
    all_positions = [i for i in range(len(equipment))]
    
    with term.cbreak(), term.hidden_cursor():
        dsp.equipment_display(cursor, equipment, remaining_points)
        inp = term.inkey()

        while inp != 'q':
            # interpret first input
            if inp.name in vertical_input:
                cursor = vertical_cursor_logic(cursor, all_positions, inp.name)
            if inp.name == 'KEY_ENTER':
                equipment[cursor].selected, remaining_points = select_logic(equipment[cursor], remaining_points)

            #cycle input indefinitely
            dsp.equipment_display(cursor, equipment, remaining_points)
            inp = term.inkey()

def skill_selection(remaining_points):
    '''
    Loop for skill selection logic.
    '''
    cursor = 0
    all_positions = [i for i in range(len(skills))]
    
    with term.cbreak(), term.hidden_cursor():
        dsp.skill_display(cursor, skills, remaining_points)
        inp = term.inkey()

        while inp != 'q':
            # interpret first input
            if inp.name in vertical_input:
                cursor = vertical_cursor_logic(cursor, all_positions, inp.name)
            if inp.name == 'KEY_ENTER':
                skills[cursor].selected, remaining_points = select_logic(skills[cursor], remaining_points)

            #cycle input indefinitely
            dsp.skill_display(cursor, skills, remaining_points)
            inp = term.inkey()












