# Party Class #

## Class Initializer
Created a class Party to store each "member" of the party (m=4 so 4 members will be initialized). 
### Initializes with these argument(s):
- name - Name of party member (ex. Alice, Bob, Charlie, Dave)
- start_index - Where party member starts using pads from
- direction - Whether party member goes left or right (+1 for right, -1 for left), and depends on start_index
- zone_min - Creates minimum range that party member can go (inclusive)
- zone_max - Creates maximum range that party member can go (exclusive)
### Initalized with variable(s) but not argument(s):
- current_index - defaults at start_index and increments/decrements based on direction to keep track of where party member is at all times
- has_sent - Keeps track of whether a party member has sent a message or not

## get_next_pad_index function
- Returns current_index of specific party member 
- Represents next pad index to be used if a message were to be sent

## get_last_used_index function
- Goal of this function is to return the last index used by the party member
- We first check whether a message has been sent by the party member, and if not, we simply return their default index which we set as start_index
- Depending on the direction the party member moves, we either return current_index - 1 (if member moving right) or current_index + 1 (if member moving left)
- This ensures boundary of already used pads is always known

## can_send function
- Goal of this function is to ensure the party member can properly send a message without violating any rules
### Argument(s)
- message_length - Number of pads needed for message
- partner_last_index - Last pad index used by partner in same zone
- d - Safety gap parameter (buffer of unused pads)
- partner_has_sent - Whether party members corresponding partner has sent at least one message
### Function
- The direction of the party member helps figure out which branch in the if statement to go (moving right is a positive direction, left is a negative direction)
#### Right Direction (Positive)
- Store the next start_index (by using current_index) and where the index would end by adding the current_index and the length of the message (subtracted by 1 since its an index)
- Check if next_end is greater than or equal to zone_max, if it is return False since there aren't enough pads for the message
- Check if party member's partner has sent a message, and check whether there is enough pads between party member and partner. Regardless of whether the partner has sent, enforce next_end < partner_last_index - d; when partner hasn’t sent, partner_last_index equals their start_index.
#### Left Direction (Negative)
- Store the next start_index (by using current_index minus message_length and plus one cause its an index) and where the index would end by simply setting it to current_index
- Check if next_start is less than zone_min, if it is, return False since there aren't enough pads for the message   
- Check if party member's partner has sent a message, and if he has, check whether there is enough pads between party member and partner. Regardless of whether the partner has sent, enforce next_start > partner_last_index + d; when partner hasn’t sent, partner_last_index equals their start_index.

## consume_pads function
- Goal of this function is to consume pad indices for a message once it has been determined safe to send and move the index of talking party member
- Returns a list of pad indices that were consumed
### Argument(s)
- message_length - Number of pads needed for message
### Function
- The direction of the party member helps figure out which branch in the if statement to go (moving right is a positive direction, left is a negative direction)
- Since the function represents the consumption of pads, the has_sent value is changed to True
#### Right Direction (Positive)
- Creates a list of the pad indexes that were used to send the message
- Increments the current_index of the party member by the message_length 
#### Left Direction (Negative)
- Creates a list of the pad indexes that were used to send the message
- Decrements the current_index of the party member by the message_length

## repr function
- Returns readable string showing:
  - Party member's name
  - Current position
  - Direction (in arrows: --> for right direction and <-- for left direction)

# Protocol Class #

## Class Initializer
Created a class Protocol to coordinate the full Parallel Pairs system.

### Initializes with these argument(s)
- n - Total number of pads in sequence
- d - Gap parameter (max undelivered messages), defaults to 10

### Initializes with variabler(s) but not argument(s)
- pad_usage - List of length n, filled with booleans to track which pads have been used
- zone_split - n//2 to divide the pad space into two equal zones
- parties - Dictionary to easily access party members
- pairs - Dictionary to easily access party members' partners
- messages_sent - Counts successful sends
- messages_attempted - Counts all send attempts

### Partner Making
#### Zone 1 [0, zone_split):
- Creation of alice using Party class:
  - name - Alice
  - start_index - 0
  - direction - Moving right (+1)
  - zone_min - 0
  - zone_max - zone_split (half of the space)
- Creation of bob using Party class:
  - name - Bob
  - start_index - zone_split-1 
  - direction - Moving left (-1)
  - zone_min - 0
  - zone_max - zone_split (half of the space)
#### Zone 2 [zone_split, n):
- Creation of charlie using Party class:
  - name - Charlie
  - start_index - zone_split
  - direction - Moving right (+1)
  - zone_min - zone_split
  - zone_max - n
- Creation of dave using Party class:
  - name - Dave
  - start_index - n-1
  - direction - Moving left (-1)
  - zone_min - zone_split
  - zone_max - n

## attempt_send function
- Simulates a party attempting to send a message of a given length
### Arguments
- party_name - Name of party attempting to send
- message_length - Length of message in pads
### Function
- Increment messages_attempted
- Retrieve party member and their partner
- Check if party member is able to send the message properly using can_send function in party class 
  - If False, return False as message will not be able to be sent without breaking a rule
- call consume_pads which the message_length as the parameter, returning a list of the indexes of used pads
- For each pad index used:
  - Assert pad has not already been used
  - Mark pad as used in pad_usage
- Increment messages_sent
- Return True, ensuring that no pad is ever reused, preserving perfect secrecy
- Note: The assert not pad_usage[pad_idx] enforces each pad index is used at most once, which is the necessary condition for OTP perfect secrecy.

## is_terminated function
- Goal of this function is to check if the protocol has terminated (when no party can send even a minimal message)
- Returns True if protocol is terminated
### Function
- For each party member in parties dictionary:
  - Set party and partner for each member and check if they can send a minimal message (length 1) using the can_send function (party class).
  - If any party can send a length-1 message, return False (NOT terminated yet).  
- If no party can send a length-1 message, return True (terminated).  

## get_wasted_pads function
- Return count of unused pads
- Computed as: n - sum(pad_usage) (since sum(pad_usage) counts used pads).

## get_used_pads function
- Return total count in pad_usage (using sum() function), or the number of used pads

## get_waste_percentage function
- Returns (wasted_pads/n)*100 (used get_wasted_pads function for wasted_pads)

## get_statistics function
- Returns a dictionary with various statistics about how the protocol went:
  - Total pads
  - Used pads
  - Wasted pads
  - Waste percentage
  - Messages sent
  - Messages attempted
  - Termination status

## repr function
- Returns compact summary of:
  - n
  - d
  - Used pads
  - Wasted pads
  - Messages sent
