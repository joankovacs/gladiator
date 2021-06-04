'''
           RESOURCES.PY
=====================================
Contains data for the game. 

TABLE OF CONTENTS
    [0] DATA STRUCTURES: Equipment, skills, and attributes as lists of dictonaries
    [1] COMPOSITION FUNCTIONS: Renders read-only structures into runtime structures
    [2] Suspended/revision/test code

NOTE: If modifying data structures, certain properties for each type must be present for chargen.py to work.
    Attributes
        STRUCTURE: 'name', 'desc'
        COMP FUNCTION: 'value'
    Equipment
        STRUCTURE: 'name', 'desc', 'value'*
        COMP FUNCTION: 'value'*, 'selected'
    Skills
        STRUCTURE: 'name', 'desc'
        COMP FUNCTION: 'value', 'selected'
*See further notes about equipment about value property placement
'''

#########################################################################################
#[0] DATA STRUCTURES
'''
Contains lists of dictionaries that contain read-only information for the game.

TASK: Figure out what to do with 'value' in equipment_read_only - it's only used for chargen and possibly doesn't need to be in the main game data structures.  [Possible: in class_init?  stand-alone list or dict?]

NOTE: EQP & SKL will possess many more fields later.  Full properties don't need to exist until F1.
'''

attributes_read_only = [
    {'name':'REF', 'desc':'Reflex determines how hard it is to hit you, and also your hit chance with weapons of all kinds. Armor can negatively affect your reflex.  Reflex also affects characteristics such as parrying, counterattacks, or certain maneuvers.',},
    {'name':'FOR', 'desc':'Fortitude determines your resistance to pain & suffering.  A character with a high fortitude will find it easier to keep going despite grievous injuries.  Fortitude also affects your stamina and energy levels.',},
    {'name':'WIT', 'desc':'Wits affects the success of a broad range of maneuvers and really keeps your opponents on their toes.  It also has a (small) hand in many other characteristics and abilities and allows you to perceive enemy actions clearer.',},
    {'name':'MOX', 'desc':'Moxie allows you to execute maneuvers with grace and panache and to stick it to overwhelming odds.  Crowds love a gladiator with moxie!  This stat is essential to keeping you in the crowds\' good graces.',},
]

equipment_read_only = [
    {'name':'gladius', 'value':2, 
     'desc':'duhhhh a sword'},
    {'name':'hasta', 'value':2, 
     'desc':'stabby stabby boi'},
    {'name':'javelin', 'value':1, 
     'desc':'+1000 stab range'},
    {'name':'dagger', 'value':1, 
     'desc':'nothing says you\'re brutally unprepared for a deathfest like a 6" piece of cheap iron'},
    {'name':'mace', 'value':2, 
     'desc':'BONK! horny jail'},
    {'name':'recurve_bow', 'value':3, 
     'desc':'this bow makes laser gun noises'},
    {'name':'tunic', 'value':2, 
     'desc':'TOGA PARTY! TOGA PAAAAARTY!!!'},
    {'name':'leather_shield', 'value':1, 
     'desc':'It\'ll stop an arrow but it won\'t stop your father\'s disappointment.'},
    {'name':'leather_hood', 'value':2, 
     'desc':'look shady and cool.  I mean, edgy and lame'},
    {'name':'bronze_cap', 'value':3,
     'desc':'keeps HAARP mind control rays out'},
    {'name':'linen_leggings', 'value':2, 
     'desc':'the name lies.  they\'re actually fishnet leggings & heels.'},
]

skills_read_only = [
    {'name':'gimmick_lvl1', 
     'desc':'Unlocks a number of cheap tricks that spring up from time to time in combat.  The crowd loves fighting dirty!',},
    {'name':'levelheaded_lvl1', 
     'desc':'You\'re less likely to panic or succumb to pain in battle.',},
    {'name':'shield_bash', 
     'desc':'Unlocks a short-range offensive maneuver with your shield.  The harder and heavier the shield, the better it is.',},
    {'name':'pommel_strike', 
     'desc':'Unlocks a short-range blunt damage strike with one-handed weapons.',},
    {'name':'wrestler', 
     'desc':'Unlocks a lot of hand-to-hand grappling and fighting maneuvers.  Don\'t miss out on this if you\'re fighting barehanded!',},
    {'name':'sprinter', 
     'desc':'Allows you to cover much greater distances in less time in the arena.  Important for closing on ranged opponents.',},
    {'name':'surefooted', 
     'desc':'You\'re much less likely to stumble, be staggered, or be knocked down in combat.',},
    {'name':'snipe', 
     'desc':'Increases range and accuracy of ranged weapons.  But only candy-asses used ranged in the arena.',},
    {'name':'tosser', 
     'desc':'Increases range, accuracy, and power of thrown weapons.  Be sure to flex it up for the crowd before you throw!',},
    
]


#########################################################################################
#[1] COMPOSITION FUNCTIONS - CHARACTER GENERATION
'''
Contains functions that composes runtime data for chargen (and possibly later, the main game?)
Returns a list of classes composed from DATA STRUCTURES above.
'''

def class_init_ATT(struc):
    '''
    >This function composes & returns a class that is an initialized version of a data structure.  The data structure can be attributes, skills, or equipment.  The class that it returns is suitable for being passes to chargen, where it exists during runtime, and then writes the values to character.py.  The purpose of this function is to be able to create runtime values (e.i. value of an attribute, whether a piece of equipment is in your inventory) without modifying runtime values of resources.py (Previous iteration had .selected as an attribute of namedtuples in resources.py).
    CAUTION: this might not be the best solution to the problem.  Consult w/ Samantha.
    
    struc: the data structure associated with the function (att, eqp, or skl)
    '''
    class Attribute:
        def __init__(self, name, desc, value):
            self.name = name
            self.desc = desc
            self.value = value
    
    attributes = [Attribute(name=att['name'], desc=att['desc'], value=1) for att in struc]
    return attributes

def class_init_EQP(struc):
    '''
    >This function composes & returns a class that is an initialized version of a data structure.  The data structure can be attributes, skills, or equipment.  The class that it returns is suitable for being passes to chargen, where it exists during runtime, and then writes the values to character.py.  The purpose of this function is to be able to create runtime values (e.i. value of an attribute, whether a piece of equipment is in your inventory) without modifying runtime values of resources.py (Previous iteration had .selected as an attribute of namedtuples in resources.py).
    CAUTION: this might not be the best solution to the problem.  Consult w/ Samantha.
    
    struc: the data structure associated with the function (att, eqp, or skl)
    '''
    class Equipment:
        def __init__(self, name, desc, value, selected):
            self.name = name
            self.desc = desc
            self.value = value
            self.selected = selected
    
    equipment = [Equipment(name=eqp['name'], desc=eqp['desc'], value=eqp['value'], selected=False) for eqp in struc]
    return equipment

def class_init_SKL(struc):
    '''
    >This function composes & returns a class that is an initialized version of a data structure.  The data structure can be attributes, skills, or equipment.  The class that it returns is suitable for being passes to chargen, where it exists during runtime, and then writes the values to character.py.  The purpose of this function is to be able to create runtime values (e.i. value of an attribute, whether a piece of equipment is in your inventory) without modifying runtime values of resources.py (Previous iteration had .selected as an attribute of namedtuples in resources.py).
    CAUTION: this might not be the best solution to the problem.  Consult w/ Samantha.
    
    struc: the data structure associated with the function (att, eqp, or skl)
    '''
    class Skill:
        def __init__(self, name, desc, value, selected):
            self.name = name
            self.desc = desc
            self.value = value
            self.selected = selected
    
    skills = [Skill(name=skl['name'], desc=skl['desc'], value=1, selected=False) for skl in struc]
    return skills































#########################################################################################
#Suspended code (under revision or obsolete)

#from collections import OrderedDict, namedtuple

#(Temporarily suspended, under revision)
#composites
'''
basic_lst_att = [a.name for a in attributes]
basic_lst_eqp = [e.name for e in equipment]
basic_lst_skl = [s.name for s in skills]
'''

#Resource declarations
#Contains the namedtuple declarations for old att/eqp/skl stuff
'''
Attribute = namedtuple('Attribute',['name','value','desc'])  
attributes = [
    Attribute('REF', 1,
              'Reflex determines how hard it is to hit you, and also your hit chance with weapons of all kinds. Armor can negatively affect your reflex.  Reflex also affects characteristics such as parrying, counterattacks, or certain maneuvers.'),
    Attribute('FOR', 1, 
              'Fortitude determines your resistance to pain & suffering.  A character with a high fortitude will find it easier to keep going despite grievous injuries.  Fortitude also affects your stamina and energy levels.'),
    Attribute('WIT', 1, 
              'Wits affects the success of a broad range of maneuvers and really keeps your opponents on their toes.  It also has a (small) hand in many other characteristics and abilities and allows you to perceive enemy actions clearer.'),
    Attribute('MOX', 1, 
              'Moxie allows you to execute maneuvers with grace and panache and to stick it to overwhelming odds.  Crowds love a gladiator with moxie!  This stat is essential to keeping you in the crowds\' good graces.'),
]


Equipment = namedtuple('Equipment',['name','value','selected','desc'])
equipment = [
    Equipment('gladius', 2, False, 
              'duhhhh a sword'),
    Equipment('hasta', 2, False, 
              'stabby stabby boi'),
    Equipment('javelin', 1, False, 
              '+1000 stab range'),
    Equipment('dagger', 1, False, 
              'nothing says you\'re brutally unprepared for a deathfest like a 6" piece of cheap iron'),
    Equipment('mace', 2, False, 
              'BONK! horny jail'),
    Equipment('recurve_bow', 3, False, 
              'this bow makes laser gun noises'),
    Equipment('tunic', 2, False, 
              'shirt says bohemian chic, weapons say you\'re ready to kill a man.'),
    Equipment('leather_shield', 1, False, 
              'It\'ll stop an arrow but it won\'t stop your father\'s disappointment.'),
    Equipment('leather_hood', 2, False, 
              'look shady and cool.  I mean, edgy and lame'),
    Equipment('bronze_cap', 3, False, 
              'keeps HAARP mind control rays out'),
    Equipment('linen_leggings', 2, False, 
              'the name lies.  they\'re actually fishnet leggings & heels.'),
]


Skill = namedtuple('Skill',['name', 'value', 'selected', 'desc'])
skills = [
    Skill('gimmick_lvl1', 1, False,
          'Unlocks a number of cheap tricks that spring up from time to time in combat.  The crowd loves fighting dirty!'),
    Skill('levelheaded_lvl1', 1, False, 
          'You\'re less likely to panic or succumb to pain in battle.'),
    Skill('shield_bash', 1, False, 
          'Unlocks a short-range offensive maneuver with your shield.  The harder and heavier the shield, the better it is.'),
    Skill('pommel_strike', 1, False, 
          'Unlocks a short-range blunt damage strike with one-handed weapons.'),
    Skill('wrestler', 1, False, 
          'Unlocks a lot of hand-to-hand grappling and fighting maneuvers.  Don\'t miss out on this if you\'re fighting barehanded!'),
    Skill('sprinter', 1, False, 
          'Allows you to cover much greater distances in less time in the arena.  Important for closing on ranged opponents.'),
    Skill('surefooted', 1, False, 
          'You\'re much less likely to stumble, be staggered, or be knocked down in combat.'),
    Skill('snipe', 1, False, 
          'Increases range and accuracy of ranged weapons.  But only candy-asses used ranged in the arena.'),
    Skill('tosser', 1, False, 
          'Increases range, accuracy, and power of thrown weapons.  Be sure to flex it up for the crowd before you throw!'),
]

'''
