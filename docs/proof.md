## Definitions ##

Pad Sequence:
    Let there be a shared ordered sequence of pads such that P = {p0,p1,...,p(n-1)} where each pad may be used once.

Parties & Positions
    Let there be 4 parties par1, par2, par3, par4 where each contains an index that they will start at and use pads as they move along.
    Initial Positions:
        Let n be the length of the message
        par1 --> starts at 0, moves right
        par2 --> starts at [(n//2)-1], moves left
        par3 --> starts at (n//2), moves right
        par4 --> starts at n-1, moves left

Used Pads:
    A pad is considered used at send time where U ⊆ {0,...,n-1} is the set of pad indices that have been used

Sending Conditions:
    A party member is allowed to use a pad and send messaages if and only if:
        pi ∈/ (not an element of) U
        Two parties cannot choose the same pad index, and their claimed pad regions never intersect  
    
**Invariants**

Used Pads:
    Every pad index enters U at most once
Party Index:
    At all times, par1[ind]​≤par2[ind]​<par3[ind]​≤par4[ind]​, where ind represents the index of that party member

# Proof of Invariants
## Claim

The following invariants hold at all times during protocol execution:
1. **Used Pads Invariant**  
   Every pad index enters U at most once.
2. **Pointer Ordering Invariant**  
   At all times:  
   par1_index ≤ par2_index < par3_index ≤ par4_index

## Proof
We prove both invariants by induction over protocol events.
Protocol events consist of:

- A **send event**, where one party uses its current pad index and moves its pointer.
- A **delivery event**, which does not modify pad indices or used pads.

## Base Case (Time 0)

At time 0:
- No pads have been used, so  
  U = {}  

Therefore, the Used Pads Invariant holds.

- By initial positions:
  - par1 starts at 0
  - par2 starts at (n//2) - 1
  - par3 starts at (n//2)
  - par4 starts at n - 1

Since (n//2) - 1 is strictly less than (n//2), we have:

par2_index < par3_index

Also, when n ≥ 2:

par1_index ≤ par2_index  
par3_index ≤ par4_index  

Thus:

par1_index ≤ par2_index < par3_index ≤ par4_index

So both invariants hold at time 0.

## Inductive Step

Assume both invariants hold immediately before some protocol event. We show they still hold immediately after the event.

### Case 1: Delivery Event
A delivery event does not modify:
- Any party index
- The set U

Therefore, both invariants remain unchanged.

### Case 2: Send Event
Suppose party pari sends using pad index: 
    
p = pari_index

By the sending conditions:
1. p is not in U.
2. The party is allowed to send only if advancing its pointer preserves the ordering constraint with its adjacent neighbor.

After sending:
- U becomes U union {p}
- The party index moves one step in its direction:
  - par1 and par3 move right (+1)
  - par2 and par4 move left (-1)

We now verify both invariants.

## Preservation of Used Pads Invariant

Since the protocol requires:

p is not in U before sending, the pad index being added is new.

Thus, no pad index can enter U twice.

Therefore, the Used Pads Invariant is preserved.

## Preservation of Pointer Ordering Invariant

Only one pointer changes during a send event.

We analyze each party.

### par1 Sends (moves right)

Before sending:

par1_index ≤ par2_index

After incrementing par1_index by 1, ordering would fail only if:

par1_index + 1 > par2_index

However, the protocol allows par1 to send only if:

par1_index + 1 ≤ par2_index

Therefore, ordering remains preserved.

### par2 Sends (moves left)

Before sending:

par1_index ≤ par2_index  
par2_index < par3_index  

After decrementing par2_index by 1, ordering would fail only if:

par2_index - 1 < par1_index

But the protocol allows par2 to send only if:

par2_index - 1 ≥ par1_index

Thus the left boundary ordering is preserved.

Since par2 moves left, the inequality par2_index < par3_index remains true automatically.

### par3 Sends (moves right)

Before sending:

par2_index < par3_index ≤ par4_index  

After incrementing par3_index by 1, ordering would fail only if:

par3_index + 1 > par4_index

But the protocol allows par3 to send only if:

par3_index + 1 ≤ par4_index

Thus the right boundary ordering is preserved.

Since par3 moves right, the inequality par2_index < par3_index remains true automatically.

### par4 Sends (moves left)

Before sending:

par3_index ≤ par4_index  

After decrementing par4_index by 1, ordering would fail only if:

par4_index - 1 < par3_index

But the protocol allows par4 to send only if:

par4_index - 1 ≥ par3_index

Thus ordering remains preserved.

## Conclusion

Both invariants:
- Used Pads uniqueness
- Pointer ordering

hold at time 0 and are preserved by every protocol event.

Therefore, by induction, both invariants hold throughout execution.
