# Party Class #

## Class Initializer
Created a class Party to store each "member" of the party (m=4 so 4 members will be initialized). 
### Initializes with these arguments:
- name - Name of party member (ex. Alice, Bob, Charlie, Dave)
- start_index - Where party member starts using pads from
- direction - Whether party member goes left or right (+1 for right, -1 for left), and depends on start_index
- zone_min - Creates minimum range that party member can go (inclusive)
- zone_max - Creates maximum range that party member can go (exclusive)
### Initalized with variables but not arguments:
- current_index - defaults at start_index and increments/decrements based on direction to keep track of where party member is at all times
- has_sent - Keeps track of whether a party member has sent a message or not

## get_next_pad_index function
- Returns current_index of specific party member 