'''
           DISPLAY.PY
=====================================
Contains data & functions for composing & displaying the data/GUI for the game. 

TABLE OF CONTENTS
    [0] IMPORTS & INITIALIZATIONS
    [1] DISPLAY FRAME: coords and loads the ASCII text file into runtime as a variable
    [2] GENERAL UTILITY FUNCTIONS: Used for more than one screen
    [3] SCREEN FUNCTIONS: Used for only one specific screen
    [X] JUNK CODE: Various bits and pieces and materials that were replaced/revised.


'''

############################################################################################

import os
from blessed import Terminal
from math import floor
from statistics import mean

term = Terminal()

############################################################################################

#declare constants for frame display position. X, Y refer to the .move_xy positions for terminal().  Width and height refers to the maximum character dimensions for the zone.
DISPLAY_COORDS = {
    'title':{'x':12, 'y':10},
    'title_max':{'width':55, 'height':1},
    'body':{'x':13, 'y':13},
    'body_max':{'width':53, 'height':20},
    'footnote':{'x':14, 'y':34},
    'footnote_max':{'width':53, 'height':1},
}


#load in display frame so that the file isn't continuously read
DISPLAY_FRAME = []
with open('display_frame_tall.txt', 'r') as f:
    for line in f.read().splitlines():
        DISPLAY_FRAME.append(line)            

############################################################################################
'''GENERAL UTILITY FUNCTIONS
These functions are used agnostic to any particular screen.
'''

def cleanify(string):
    '''
    Strips underscores and capitalizes for programatic name > display appropriate name
    '''
    return string.capitalize().replace('_', ' ')

def wrap_text(data, limits):
    '''
    Accepts a longer string and returns a wrapped string.
    Wrap text is mutually exclusive with v_just and h_just at the moment, and prints a single block of wrapped text in a frame that's slightly smaller than the maximum bounding limits.  Because of how print_pipeline by convention expects a list for data_group_n ['assembled'] but that this may not parse later with the specific assembly functions, this function will check to see if it is being passed a string or a list.  If it is a list, it expects a one-item list and grabs the first item from it.
    
    DANGER: if any word exceeds the limit of width and is not broken by a space, this function cannot work.
    '''
    if type(data) == list:
        data = data[0]
    
    #establishes function-specific variables for the wrap process
    height = limits['height']- 2
    width = limits['width'] - 2
    data = data.split()
    
    #Safety check: aborts function early if nonfunctional parameters are reached.
    for word in data:
        if len(word) >= width-1:
            return ['ERROR: WORD IN TEXT','EXCEEDS WIDTH LIMIT.']
    
    def line_assemble(data):
        #puts together each line for the wrapped text
        string = ''
        while len(string) <= width:
            #send empty strings home
            if data == []:
                return string, data
            
            #catches overflow and ensures end spaces aren't butting out words
            if len(string + data[0]) == width:
                string+= data.pop(0)
                return string, data
            if len(string + data[0]) > width:
                return string, data
            
            string += data.pop(0) + ' '
        return string, data
    
    refactored = []
    while data != []:
        newline, data = line_assemble(data)
        refactored.append(newline)

    
    #finally, h&v justify the new list to be properly set forward
    y_pad = [' ']
    refactored = [' '+line for line in refactored]
    
    #final safety check:
    if len(refactored) > height+2:
        return ['ERROR: HEIGHT OF','TEXT EXCEEDS LIMIT.']
    
    if len(refactored) > height:
        return refactored
    else:
        return y_pad + refactored

def v_justify(height, data):
    '''
    This function centers the display text vertically.
        height: max lines value
        data: the data printed in the frame
    Returns a list of strings with justified spacing.
    '''
    v_difference = height - len(data)
    front_pad = [' ' for i in range(floor(v_difference/2))]
    back_pad = [' ' for i in range(v_difference - len(front_pad))]
    
    return front_pad + data + back_pad

def h_justify(width, data):
    '''
    This function centers the display text horizontally.
        width: max character width of the display
        data: the data printed in the frame
    Returns a list of strings with justified spacing.
    '''
    autosetback = 3 #something of a magic constant - justifies further left for a more 'natural' centered look.  
    #average_width = floor(mean([len(line) for line in map(term.strip_seqs, data)]))
    average_width = floor(mean(map(len, map(term.strip_seqs, data))))

    
    front_pad = [' ' * (floor((width - average_width)/2)-autosetback) for i in range(width)]
    back_pad = []
    
    for line in map(term.strip_seqs, data):
        back_pad.append(' ' * (width - len(line) - len(front_pad[0])))
    
    return [a+b+c for a, b, c in zip(front_pad, data, back_pad)]

def tab_header(tabs, position):
    '''
    Constructs a header that is incorporated into the print pipeline for additional display. 
    Function returns an array of 3 strings each of length header_max; the keys are the position
    WARNING: This function assumes that the tabs display will always be 3 high.  Even if length or display frame changes, this dimension is unlikely to change.
    
    tabs: list of strings that will be displayed in header.
    position: integer that MUST be in the possible index range for tabs. Current position.
    '''
    
    header_max = DISPLAY_COORDS['title_max']['width']
    total_width = 1+sum([len(s) +1 for s in tabs]) #totals length of tabs and ║s
    spare_spaces = header_max-total_width
    header_array = ['╔', '║', '╚'] #print array
    
    #Catch case where total width exceed space limits.
    if header_max < total_width:
        raise Exception(f"Cannot print.  Width ({total_width}) exceeds maximum permissible ({header_max}).")
    
    def _get_shortest(lst):
        #Returns the index of the shortest length string from a list of strings.
        return lst.index(min(lst, key=len))
    
    def _outline(tabline, l_corner, middle_t, r_corner):
        '''
        This function requires the centre tabline to have already been constructed
        For top:     l_corner = '╔', middle_t = '╦', r_corner = '╗'
        For bottom:  l_corner = '╚', middle_t = '╩', r_corner = '╝'
        tabline = header['tabs'] /after/ it is complete
        '''
        bar_index = [i for i, c in enumerate(tabline) if c=='║']
        bar_index.pop(0) #remove index=0 (║ in first place) so the while loop works
        line = l_corner #initialize start of line
        
        while len(line) < (len(tabline)-1):
            
            if len(line) < bar_index[0]:
                line += '═'
            elif len(line) == bar_index[0]:
                line += middle_t
                bar_index.pop(0)
        line += r_corner
        
        return line
    
    #Initial 'even' space padding if there's lots of pads to be handed out:
    if spare_spaces >= 2*len(tabs):
        for i in range(len(tabs)):
            tabs[i] = ' ' + tabs[i] + ' '
        spare_spaces -= 2*len(tabs)
    
    #Thereafter, space pads the shortest item first:
    while spare_spaces >= 1:
        if spare_spaces == 1:
            tabs[_get_shortest(tabs)] = tabs[_get_shortest(tabs)] + ' '
            spare_spaces -= 1
        else:
            tabs[_get_shortest(tabs)] = ' ' + tabs[_get_shortest(tabs)] + ' '
            spare_spaces -= 2
    
    #finalize array structure
    for t in tabs:
        header_array[1] += t + '║' #Middle line of tabs (with text)
    header_array[0] = _outline(header_array[1], '╔', '╦', '╗') #Top (first) line
    header_array[2] = _outline(header_array[1], '╚', '╩', '╝') #Bottom (last) line
    
    #The unfortunate quality of having to construct the tabs line twice.  The first must be WITHOUT term.method, in order to have the proper index locations for top and bottom.  The second must be to add 'bold_black_on_white' method.  You can see this in that the ['tabs'] line will be len+20 compared to top and bottom *programmatically* but the difference NOT visually displayed to the monitor.
    header_array[1] = '║' 
    for t in tabs:
        if tabs[position]==t:
            header_array[1] += term.bold_black_on_white(t) + '║'
        else: header_array[1] += t + '║'
    
    #print the tab header in the correct location
    x = DISPLAY_COORDS['title']['x']
    y = DISPLAY_COORDS['title']['y']
    for i in header_array:
        print(term.move_xy(x, y) + i)
        y+=1

def footnote(text, coords):
    '''
    Thus function prints information in the footnote at the bottom of the display frame.  Text length to not exceed 53.
    '''
    print(term.move_xy(coords['x'], coords['y']) + term.bold(text))

def print_pipeline(data_group_1, data_group_2=None):
    '''
    This function aggregates data & print functions and return a list of strings that print out within the current display frame (as declared at the beginning of the file).  The data group variables are the data that is to be printed; it will automatically split into windows if group 2 != None.  The details of how data groups should be formatted is as below:
    group = {
        assembly_func: Unique function for each menu screen that assembles the pre-spaced and pre-justified data (such as REF, FOR, and the dots preceding them) and returns a list.
        v_just: Boolean; whether this group will be vertically justified.
        h_just: Boolean; whether this group will be horizontally justified.
        wrap: Boolean; whether this group is a long string that will need to wrap around.  Currently mutually exclusive with v/h justification
    }
    NOTE that this function, largely, currently does not check to see if the data will display past limit boundaries.  Validation occurs in data group assembly.
    NOTE that this function deals with neither the header nor the footnote.
    '''
    
    #Automatically defines limits based on whether there are two groups or not.
    limits = DISPLAY_COORDS['body_max'].copy()
    if data_group_2 != None:
        limits['width'] = floor(limits['width']/2)
    
    #apply print pipeline to each group
    for group in [data_group_1, data_group_2]:
        #initial check to see if there are two groups
        if group == None:
            break
        
        data = group['assembled']
        group['preprint'] = None
        
        #Returns a wrapped string
        if group['wrap']:
            group['preprint'] = wrap_text(data, limits)
            v_distance = limits['height'] - len(group['preprint'])
            for i in range(v_distance):
                group['preprint'].append(' ' * limits['width'])
            continue
        
        #vertically justifies; or appends appropriate number of lines
        if group['v_just']:
            data = v_justify(limits['height'], data)
        else:
            v_distance = limits['height'] - len(data)
            for i in range(v_distance):
                data.append(' ')
        
        #horizontally justifies; or pads spaces to the right
        if group['h_just']:
            data = h_justify(limits['width'], data)
        else:
            for i in range(len(data)):
                data[i] += (' ' * (limits['width']-len(data[i])))
        
        #Casts the refactored display data.
        group['preprint'] = data
    
    #Return a combined list if two sides; otherwise return a single list.
    if data_group_2 != None:
        return [i+'║'+j for i, j in zip(data_group_1['preprint'], data_group_2['preprint'])]
    else:
        return data_group_1['preprint']


############################################################################################
'''SCREEN FUNCTIONS
These functions are used for specific screens within the game.

TABLE OF CONTENTS:
    [0] Character generation displays
    [1] Inventory displays
    [2] Shop displays
    [3] Character improvement displays
    [4] Game data displays
    [5] Combat displays
'''

# ZONE [0] - CHARACTER GENERATION DISPLAYS ----------------

def box_logic(num):
    '''
    Returns filled or empty boxes for the attribute selection.  Arg must be an int in 1-4
    '''
    return ('●' * num) + ('○' * (4-num))

def attributes_display(cursor, options, points):
    '''
    Cursor is an integer IN the index of options.
    Options is the full list of attribute namedtuples.
    Points is the points remaining to spend and is only used in the footnote.
    '''
    #Clear screen and print current display frame + tabs.
    os.system('clear')
    for line in DISPLAY_FRAME:
        print(line)
    
    #Assemble left side display list from current cursor and options data.
    left_disp = []
    for i, opt in enumerate(options):
        if cursor != i:
            left_disp.append(f'{box_logic(opt.value)}  {opt.name}')
        else:
            left_disp.append(term.bold_black_on_white(f'{box_logic(opt.value)}  {opt.name}'))
    
    #Assemble right side display list from current cursor and options data.
    right_disp = options[cursor].desc
    
    #Construct display groups 1 and 2.
    group1 = {
        'assembled':left_disp,
        'v_just':True,
        'h_just':True,
        'wrap':False,
    }
    group2 = {
        'assembled':right_disp,
        'v_just':False,
        'h_just':False,
        'wrap':True,
    }
    
    #Use preprint for the finalized display.
    x = DISPLAY_COORDS['body']['x']
    y = DISPLAY_COORDS['body']['y']
    total_body = print_pipeline(group1, group2)
    
    for i in range(len(total_body)):
        print(term.move_xy(x, y+i) + total_body[i])
    
    footnote(f'Remaining Points:  {points}', DISPLAY_COORDS['footnote'])

def equipment_display(cursor, options, points):
    '''
    Cursor is an integer IN the index of options.
    Options is the full list of equipment namedtuples.
    Points is the points remaining to spend and is only used in the footnote.
    '''
    #Clear screen and print current display frame.
    os.system('clear')
    for line in DISPLAY_FRAME:
       print(line)
    
    #Assemble left side display list from current cursor and options data.
    left_disp = []
    for i, opt in enumerate(options):
        option_string = f'{cleanify(opt.name)}' + ' ' * (16-len(opt.name)) + f'{opt.value}'
        if opt.selected:
            option_string = f'[{term.bold(option_string)}]'
        else:
            option_string = f' {option_string} '
        if cursor == i:
            option_string = f'{term.bold_black_on_white(option_string)}'
        
        left_disp.append(option_string)
        
    #Assemble right side display list from current cursor and options data.
    right_disp = options[cursor].desc
    
    #Construct display groups 1 and 2.
    group1 = {
        'assembled':left_disp,
        'v_just':True,
        'h_just':True,
        'wrap':False,
    }
    group2 = {
        'assembled':right_disp,
        'v_just':False,
        'h_just':False,
        'wrap':True,
    }
    
    #Use preprint for the finalized display.
    x = DISPLAY_COORDS['body']['x']
    y = DISPLAY_COORDS['body']['y']
    total_body = print_pipeline(group1, group2)
    
    for i in range(len(total_body)):
        print(term.move_xy(x, y+i) + total_body[i])
    
    footnote(f'Remaining Points:  {points}', DISPLAY_COORDS['footnote'])

def skill_display(cursor, options, points):
    '''
    Cursor is an integer IN the index of options.
    Options is the full list of skill namedtuples.
    Points is the points remaining to spend, ==1 and is implicit.
    '''
    #Clear screen and print current display frame.
    os.system('clear')
    for line in DISPLAY_FRAME:
       print(line)
    
    #Assemble left side display list from current cursor and options data.
    left_disp = []
    for i, opt in enumerate(options):
        option_string = f'{cleanify(opt.name)}'
        if opt.selected:
            option_string = f'[{term.bold(option_string)}]'
        else:
            option_string = f' {option_string} '
        if cursor == i:
            option_string = f'{term.bold_black_on_white(option_string)}'
        
        left_disp.append(option_string)
        
    #Assemble right side display list from current cursor and options data.
    right_disp = options[cursor].desc
    
    #Construct display groups 1 and 2.
    group1 = {
        'assembled':left_disp,
        'v_just':True,
        'h_just':True,
        'wrap':False,
    }
    group2 = {
        'assembled':right_disp,
        'v_just':False,
        'h_just':False,
        'wrap':True,
    }
    
    #Use preprint for the finalized display.
    x = DISPLAY_COORDS['body']['x']
    y = DISPLAY_COORDS['body']['y']
    total_body = print_pipeline(group1, group2)
    
    for i in range(len(total_body)):
        print(term.move_xy(x, y+i) + total_body[i])



# ZONE [1] - INVENTORY DISPLAYS ---------------------------













