
#Primary module; contains chargen + core game logic.

###################################################################################################

import display as dsp

###################################################################################################
#CHARACTER GENERATION


###################################################################################################
#INITIAL DECLARATIONS

attributes = {
    'WIT':1,
    'FOR':1,
    'REF':1,
    'MOX':1,
}
remaining_att_points = 3

equipment_possibles = {
    'gladius':2,
    'hasta':2,
    'javelin':1,
    'dagger':1,
    'mace':2,
    'recurve_bow':3,
    'tunic':2,
    'leather_shield':1,
    'leather_hood':2,
    'bronze_cap':3,
    'linen_leggings':2,
}
remaining_equipment_points = 6


name = ''


print(dsp.intro1())

name = input("Enter your name here:  ")





###################################################################################################









###################################################################################################
