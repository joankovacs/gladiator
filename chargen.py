'''
           CHARGEN.PY
=====================================
Contains the code for character generation.

TABLE OF CONTENTS
    (finished):
    [0] IMPORTS & INITIALIZATIONS
    [1] GENERAL UTILITY FUNCTIONS
    [2] SCREEN CLASS DECLARATIONS
    [3] MAIN
    
    (unfinished):
    [4] NAME SELECTION: Final user chargen choice, type name.
    [5] CONFIRMATION: Asks user to confirm all their choices, while confronting them with it.
    [6] FINALIZATION: Exports data to character.py (used by main.py in final)
    [X] TEST CODE: Code that won't exist in the final version but exists here for testing. 



TO DO:
    *Goes to name selection once ATT/EQP/SKL selection is complete
    *Need a 'finish' key (spacebar?) to exit out of ATT/EQP/SKL selection
    *Give summary & (option to confirm OR go back) once finished with ATT/EQP/SKL selection
'''

###############################################################################
#[0] IMPORTS & INITIALIZATIONS

import os
from blessed import Terminal

import display as dsp
import resources as rs
import character as ch

term = Terminal()


###############################################################################
#[1] GENERAL UTILITY FUNCTIONS - used in character generation screen logic.

def vertical_cursor_logic(position, all_positions, attempt):
    '''
    Determines how to move the selection cursor on accepted keyboard input.
        *position: int /in/ all_positions that represents current position
        *all_positions: list of possible positions 
        *attempt: recorded key press
    '''
    if attempt == 'KEY_UP':
        if position == min(all_positions):
            return max(all_positions)
        else:
            return position-1
    if attempt == 'KEY_DOWN':
        if position == max(all_positions):
            return min(all_positions)
        else:
            return position+1

def select_logic(item, remaining_points):
    '''
    Logic for selecting equipment & skills with the space bar
        *item: The current cursor selection
        *selected: boolean value for if the item is already selected or not
        *value: The 'cost' of the item (in the case of skills, ==1)
        *remaining_points: Remaining spend value for skills and equipment
    '''
    
    selected = item.selected
    value = item.value
    
    
    if selected:
        return False, remaining_points+value
    else:
        if remaining_points >= value:
            return True, remaining_points-value
        else:
            return False, remaining_points

def list_to_range(lst):
    #Make some code cleaner by compiling this functionality into a func
    return list(range(len(lst)))


###############################################################################
#[2] SCREEN CLASS DECLARATIONS
'''Description:
Each instantiation represents one of the three mechanics that requires user input during character generation - Attributes, Equipment, and Skills.
'''


class AttributeScreen:
    def __init__(self, remaining_points):
        self.remaining_points = remaining_points
        
        self.title = 'ATTRIBUTES'
        self.res_list = rs.class_init_ATT(rs.attributes_read_only)
        self.vertical_input = ['KEY_UP', 'KEY_DOWN']
        self.att_input = ['KEY_LEFT', 'KEY_RIGHT']
        self.accepted_input = self.vertical_input + self.att_input
        self.cursor = 0
        self.cursor_range = list_to_range(self.res_list)
    def selection(self, inp):
        '''
        Method for attribute selection screen.
        CALL: 
            1. At main_chargen() initial
            2. When the input 'KEY_TAB' cycles to correct tab position in screens list
            3. When the input is not TAB and tab position is correct
        PARAMETERS:
            *inp: either type==None OR term class object: passed in as an interpretation of user input.
        '''
        def attribute_logic(attribute, remaining_points, attempt):
            '''
            Logic for increasing or decreasing base attributes at game start.
                *attribute: Expects a class object defined in resources.py
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
        
        #If the method is called via pressing the TAB key, inp=None.  This resets cursor.
        if inp==None:
            self.cursor=0
        
        #If the method is called via pressing input in accepted_input, cursor state is saved.
        elif inp.name in self.vertical_input:
            self.cursor = vertical_cursor_logic(self.cursor, self.cursor_range, inp.name)
        elif inp.name in self.att_input:
            self.res_list[self.cursor].value, self.remaining_points =attribute_logic(self.res_list[self.cursor], self.remaining_points, inp.name)

        #Display the attributes screen after changes are interpreted.
        dsp.attributes_display(self.cursor, self.res_list, self.remaining_points)

class EquipmentScreen:
    def __init__(self, remaining_points):
        self.remaining_points = remaining_points 
        
        self.title = 'EQUIPMENT'
        self.res_list = rs.class_init_EQP(rs.equipment_read_only)
        self.vertical_input = ['KEY_UP', 'KEY_DOWN']
        self.accepted_input = self.vertical_input + ['KEY_ENTER']
        self.cursor = 0
        self.cursor_range = list_to_range(self.res_list)
    def selection(self, inp):
        '''
        Method for equipment selection screen.
        CALL: 
            1. When the input 'KEY_TAB' cycles to correct tab position in screens list
            2. When the input is not TAB and tab position is correct
        PARAMETERS:
            *inp: either type==None OR term class object: passed in as an interpretation of user input.
        '''
        #If the method is called via pressing the TAB key, inp=None.  This resets cursor.
        if inp==None:
            self.cursor=0
        
        #If the method is called via pressing input in accepted_input, cursor state is saved.
        elif inp.name in self.vertical_input:
            self.cursor = vertical_cursor_logic(self.cursor, self.cursor_range, inp.name)
        elif inp.name == 'KEY_ENTER':
            self.res_list[self.cursor].selected, self.remaining_points = select_logic(self.res_list[self.cursor], self.remaining_points)
        
        #Display the equipment screen after changes are interpreted.
        dsp.equipment_display(self.cursor, self.res_list, self.remaining_points)

class SkillScreen:
    def __init__(self, remaining_points):
        self.remaining_points = remaining_points
        
        self.title = 'SKILLS'
        self.res_list = rs.class_init_SKL(rs.skills_read_only)
        self.vertical_input = ['KEY_UP', 'KEY_DOWN']
        self.accepted_input = self.vertical_input + ['KEY_ENTER']
        self.cursor = 0
        self.cursor_range = list_to_range(self.res_list)
    def selection(self, inp):
        '''
        Method for skill selection screen.
        CALL: 
            1. When the input 'KEY_TAB' cycles to correct tab position in screens list
            2. When the input is not TAB and tab position is correct
        PARAMETERS:
            *inp: either type==None OR term class object: passed in as an interpretation of user input.
        '''
        #If the method is called via pressing the TAB key, inp=None.  This resets cursor.
        if inp==None:
            self.cursor=0
        
        #If the method is called via pressing input in accepted_input, cursor state is saved.
        elif inp.name in self.vertical_input:
            self.cursor = vertical_cursor_logic(self.cursor, self.cursor_range, inp.name)
        elif inp.name == 'KEY_ENTER':
            self.res_list[self.cursor].selected, self.remaining_points = select_logic(self.res_list[self.cursor], self.remaining_points)
        
        #Display the equipment screen after changes are interpreted.
        dsp.skill_display(self.cursor, self.res_list, self.remaining_points)

#Instatiate classes and compile them into a list for main()
screen_ATT = AttributeScreen(remaining_points = 5)
screen_EQP = EquipmentScreen(remaining_points=7)
screen_SKL = SkillScreen(remaining_points=1)

screens = [screen_ATT, screen_EQP, screen_SKL]


###############################################################################
#[3] MAIN
'''Description:
Primary function uses class methods & attributes for the 3 character generation tabs.  Loops between user inputs (tab > new screen; class.accepted_input > updated screen) until mechanics selection is finished.  Finally, prompts the user to input a name, and then asks them one more time to confirm all choices.
'''

def main(screens):
    '''
    This function uses a list of classes - each one representing a different mechanic - for character generation.  
    
    *screens: A list of classes representing the core mechanics of character generation that requires user input.
    '''
    tab = 0
    tabs = [s.title for s in screens]
    tab_range = list_to_range(tabs)
    
    def tab_logic(position, all_positions):
        #Simple func to cycle position, an integer in all_positions. Returns new position. 
        if position==all_positions[-1]:
            return 0
        return position+1
    
    with term.cbreak(), term.hidden_cursor():
        #Call chargen screen in tab position 0, with no value for input key.
        screens[tab].selection(None)
        dsp.tab_header(tabs, tab)
        inp = term.inkey()
        
        while inp != 'q':
            #interpret first input: cycle tabs if inp==TAB, else call screen logic
            if inp.name in screens[tab].accepted_input:
                screens[tab].selection(inp)
            if inp.name == 'KEY_TAB':
                tab = tab_logic(tab, tab_range)
                screens[tab].selection(None)
            dsp.tab_header(tabs, tab)
            inp = term.inkey()
    
    
    os.system('clear')
    print('\n\n\n        Thanks for playing GLADIATOR!  I hope you had a good time.')
    print('             [game by Joan Kovacs]\n\n\n')
    

###############################################################################
#[4] NAME SELECTION


























###############################################################################
#[5] FINALIZATION
'''Description:
This is for passing the values set during runtime in the lists of classes into character.py.
'''

def cast_values(ATT, EQP, SKL):
    '''
    Casts program values from chargen into character.py for runtime.
    ATT: List of attribute dictionaries
    EQP: List of equipment dictionaries
    SKL: List of skill dictionaries
    
    Returns three values.  NOTE: Proper way to call function is:
    ch.attributes, ch.inventory, ch.skills = cast_values(screen_ATT.res_list, screen_EQP.res_list, screen_SKL.res_list)
    '''
    attributes = {a.name:a.value for a in ATT}
    inventory = {i.name:False for i in EQP if i.selected==True }
    skills = [s.name for s in SKL if s.selected==True]
    
    return attributes, inventory, skills

###############################################################################
#[X] TEST CODE


main(screens)


#Finalization tests
ch.attributes, ch.inventory, ch.skills = cast_values(screen_ATT.res_list, screen_EQP.res_list, screen_SKL.res_list)

print(f'Final attributes: {ch.attributes}')
print(f'Final inventory:  {ch.inventory}')
print(f'Final skills learned:  {ch.skills}')


