## Definitions
### Pad Sequence
Let there be a shared ordered sequence of pads:

P = {p₀, p₁, …, pₙ₋₁}

where each pad may be used at most once.

### Parties & Zones
There are four parties:
- par1 (Alice)
- par2 (Bob)
- par3 (Charlie)
- par4 (Dave)

The pad space is partitioned into two disjoint zones:
- Zone 1 = {0, …, (n//2) − 1}
- Zone 2 (symmetric) = {(n//2), …, n − 1}

Zone₁ ∩ Zone₂ = ∅

Initial positions:
- par1 → starts at 0, moves right (+)
- par2 → starts at (n//2 − 1), moves left (−)
- par3 → starts at (n//2), moves right (+)
- par4 → starts at n − 1, moves left (−)

Each party consumes pads only within its assigned zone.

### Used Pads
A pad is considered used at send time. Let:

U ⊆ {0, …, n − 1}

denote the set of pad indices that have been used.

### Sending Conditions

Let d be the safety gap parameter.

Let Last(X) denote the last pad index written by party X.

A party may send a message of length L ≥ 1 only if:
1. Every pad in the proposed message segment is not in U.
2. The entire message segment lies within that party’s zone.
3. The safety gap condition holds.

Safety gap conditions:

In Zone 1:
- par1 may send only if  
  next_end(par1) < Last(par2) − d
- par2 may send only if  
  next_start(par2) > Last(par1) + d

In Zone 2:
- par3 may send only if  
  next_end(par3) < Last(par4) − d
- par4 may send only if  
  next_start(par4) > Last(par3) + d

# Invariants
We prove the following invariants hold at all times:

1. **Used Pads Invariant**  
   Every pad index enters U at most once.
2. **Zone Separation Invariant**  
   Each party only writes inside its assigned zone.
3. **Safety Gap Invariant (Zone₁)**  
   Last(par1) + d < Last(par2)
4. **Safety Gap Invariant (Zone₂)**  
   Last(par3) + d < Last(par4)

# Proof of Invariants
## Claim
All four invariants hold throughout protocol execution.

We prove this by induction over protocol events.

Protocol events consist of:
- A send event (a party consumes one or more pads).
- A delivery event (does not modify pad indices or U).

## Base Case (Time 0)
At time 0:
- U = ∅  
  Therefore, the Used Pads Invariant holds.

- By construction:
  - par1 ∈ Zone₁
  - par2 ∈ Zone₁
  - par3 ∈ Zone₂
  - par4 ∈ Zone₂  

Thus, Zone Separation holds.

Since par1 starts strictly left of par2 and par3 starts strictly left of par4, and d ≥ 0:

Last(par1) + d < Last(par2)  
Last(par3) + d < Last(par4)

Thus, all invariants hold at time 0.

## Inductive Step

Assume all invariants hold immediately before some protocol event.

We show they hold immediately after the event.

### Case 1: Delivery Event

A delivery event does not modify:
- U
- Any party index

Therefore, all invariants remain unchanged.

### Case 2: Send Event
Suppose party X sends a message of length L ≥ 1.

Let S denote the set of pad indices consumed.

After sending:
U := U ∪ S

The party’s index advances by L steps in its direction.

## Preservation of Used Pads Invariant
Before sending, the protocol verifies:

Every pad in S is not in U.

The implementation enforces this using:

assert not pad_usage[pad_idx]

Thus, no pad index can enter U more than once.

Therefore, the Used Pads Invariant is preserved.

## Preservation of Zone Separation
Before sending, the protocol checks:
- Right-moving party: next_end < zone_max  
- Left-moving party: next_start ≥ zone_min  

Thus, no party ever writes outside its assigned zone.

Zone Separation is preserved.

## Preservation of Safety Gap Invariant (Zone₁)
We analyze Zone 1 and Zone 2.

Assume before sending:

Last(par1) + d < Last(par2)

### Case: par1 Sends
Before sending, the protocol checks:

next_end(par1) < Last(par2) − d

After sending:

Last(par1)_new = next_end(par1)

Thus:

Last(par1)_new < Last(par2) − d

Adding d to both sides:

Last(par1)_new + d < Last(par2)

The invariant is preserved.

### Case: par2 Sends
Before sending, the protocol checks:

next_start(par2) > Last(par1) + d

After sending:

Last(par2)_new > Last(par1) + d

Thus:

Last(par1) + d < Last(par2)_new

The invariant is preserved.

The same applies to Zone 2.

# Conclusion
All invariants:
- Used pad uniqueness  
- Zone separation  
- Safety gap preservation in each zone  

hold at time 0 and are preserved by every protocol event.

Therefore, by induction, these invariants hold for the entire execution of the protocol.
Since:
- No pad may be used twice,
- Parties in different zones cannot overlap,
- Parties within a zone maintain a strict safety gap,

no two parties ever write to the same pad index.

The protocol therefore guarantees collision freedom and preserves the one-time pad requirement that each pad is used at most once.
