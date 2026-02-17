# Parallel Pairs Protocol - Implementation Guide

**Multi-Party One-Time Pad Communication Protocol (m=4)**

**Project 1 Applied Cryptography**  
Thomas Motais De Narbonne, Raymond Lin, Kanthimathi Sundararajan


## Overview

The Parallel Pairs protocol extends the 2-party one-time pad encryption to 4 parties while maintaining perfect secrecy and minimizing pad waste. This document describes the protocol implementation in `protocol.py`.

For testing details, see [README_TESTING.md](README_TESTING.md).

## Protocol Design

### Architecture

The protocol divides 4 parties into 2 independent teams, each operating in a separate zone:

- **Team 1 (Zone 1)**: Alice and Bob
  - Alice: starts at index 0, moves right
  - Bob: starts at index n/2-1, moves left
  
- **Team 2 (Zone 2)**: Charlie and Dave
  - Charlie: starts at index n/2, moves right
  - Dave: starts at index n-1, moves left

### Zone Division

Given a pad sequence of length `n`:
- **Zone 1**: Indices [0, n/2)
- **Zone 2**: Indices [n/2, n)

## Safety Conditions

To maintain perfect secrecy (no pad reuse), parties must maintain a gap of at least `d` pads from their partner, where `d` is the maximum number of undelivered messages in the network.

### For Rightward Parties (Alice, Charlie)

A rightward party can send a message of length L if:

```python
next_end < partner_last_index - d
```

Where:
- `next_end = current_index + L - 1`
- `partner_last_index` is the last pad used by their zone partner

### For Leftward Parties (Bob, Dave)

A leftward party can send a message of length L if:

```python
next_start > partner_last_index + d
```

Where:
- `next_start = current_index - L + 1`
- `partner_last_index` is the last pad used by their zone partner

## Perfect Secrecy Guarantee

The protocol ensures perfect secrecy through:

1. **Zone isolation**: Parties in different zones never use the same pads
2. **Gap enforcement**: Partners in the same zone maintain at least `d` pads separation
3. **Direction separation**: Partners move in opposite directions, naturally creating separation
4. **Assertion checks**: Every pad usage is verified to prevent collisions

## Implementation of Classes

### Party Class

```python
Party(name, start_index, direction, zone_min, zone_max)
```

**Attributes:**
- `name`: Party identifier (Alice, Bob, Charlie, Dave)
- `start_index`: Initial pad index
- `direction`: +1 for rightward, -1 for leftward movement
- `zone_min`, `zone_max`: Zone boundary constraints
- `current_index`: Current position in pad sequence

**Key Methods:**
- `can_send(message_length, partner_last_index, d, partner_has_sent)`: bool
  - Checks if message can be sent safely
  
- `consume_pads(message_length)`: list[int]
  - Consumes pads and returns indices used
  - Advances current position
  
- `get_last_used_index()`: int
  - Returns the last pad index this party used

### Protocol Class

```python
Protocol(n, d=10)
```

**Attributes:**
- `n`: Total number of pads in sequence
- `d`: Gap parameter (default: 10)
- `pad_usage`: Boolean array tracking which pads have been used
- `alice`, `bob`, `charlie`, `dave`: Party instances
- `parties`: Dictionary for party lookup
- `pairs`: Dictionary mapping parties to their zone partners

**Key Methods:**
- `attempt_send(party_name, message_length)`: bool
  - Attempts to send a message from specified party
  - Returns True if successful, False if safety check fails
  - Raises AssertionError if pad collision detected
  
- `is_terminated()`: bool
  - Checks if protocol has terminated
  - Returns True when no party can send even a minimal message
  
- `get_wasted_pads()`: int
  - Returns count of unused pads
  
- `get_statistics()`: dict
  - Returns comprehensive protocol statistics

## Usage Example

```python
from protocol import Protocol

# Create protocol with 1000 pads, gap d=10
protocol = Protocol(n=1000, d=10)

# Alice sends a message of length 25
success = protocol.attempt_send("Alice", 25)
if success:
    print(f"Message sent! Pads used: {protocol.get_used_pads()}")

# Charlie sends a message of length 30
success = protocol.attempt_send("Charlie", 30)

# Check if protocol can continue
if protocol.is_terminated():
    print("Protocol terminated - no party can send safely")
    
# Get statistics
stats = protocol.get_statistics()
print(f"Total messages sent: {stats['messages_sent']}")
print(f"Waste percentage: {stats['waste_percentage']:.2f}%")
```

## Termination Conditions

The protocol terminates when **at least one party** cannot send the next message securely. This occurs when:

1. A party reaches their zone boundary
2. The gap between partners becomes too small (≤ d)
3. All parties are blocked by their respective constraints
