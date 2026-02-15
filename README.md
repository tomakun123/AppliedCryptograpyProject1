# Multi-Party One-Time Pad Protocol Simulator

**Project 1 Applied Cryptography**  
Thomas Motais De Narbonne, Raymond Lin, Kanthimathi Sundararajan

## Overview

This project implements and evaluates a multi-party protocol that extends the classic 2-party one-time pad encryption to 4 parties while maintaining perfect secrecy and minimizing pad waste.

### The Protocol

**Parallel Pairs Protocol (m=4)**
- Divides 4 parties into 2 teams operating in separate zones
- **Team 1 (Zone 1)**: Alice (moves right →) and Bob (moves left ←)
- **Team 2 (Zone 2)**: Charlie (moves right →) and Dave (moves left ←)
- Each party maintains a safety gap of `d` pads from their partner
- Messages of length L consume L consecutive pads

### Key Features

✓ **Perfect Secrecy**: No pad is ever used twice (verified by assertions)  
✓ **Low Waste**: Significantly better than static partitioning (75% worst case)  
✓ **Configurable**: Adjustable pad count, gap parameter, and message lengths  
✓ **Statistical Analysis**: 100+ executions per scenario with comprehensive metrics  

## Installation

No external dependencies required! Uses Python 3.11+ standard library only.

```bash
cd "c:\Users\Raymond\Documents\NYU College Work\Spring 2026\Applied Security\AppliedCryptograpyProject1"
```

## Usage

### Run Full Simulation (Default: 100 executions per scenario)

```bash
python main.py
```

**Output:**
- Detailed results for scenarios S.1, S.2, and S.4
- Statistical metrics (mean, std dev, min, max)
- Comparison against 75% static partition baseline
- Analysis and conclusions

### Custom Parameters

```bash
# Custom pad count
python main.py --n 2000

# Custom gap parameter
python main.py --d 20

# Custom number of executions
python main.py --executions 200

# Custom message length range
python main.py --min-msg-len 5 --max-msg-len 100

# Reproducible results with seed
python main.py --seed 42

# Combine parameters
python main.py --n 5000 --d 15 --executions 500 --seed 42
```

## File Structure

```
AppliedCryptograpyProject1/
├── protocol.py          # Core protocol implementation (Party & Protocol classes)
├── simulator.py         # Scenario simulation functions (S.1, S.2, S.4)
├── main.py             # Main driver with CLI and statistics
├── problem.md          # Project specification
└── README.md           # This file
```

## Scenarios

### S.1: Single Active Party (x=1)
- Randomly select 1 party
- Only that party sends until it can't
- **Expected waste**: ~50% (one zone unused)

### S.2: Two Active Parties (x=2)
- Randomly select 2 parties
- Random sender each round
- **Expected waste**: ~25% average
  - Same zone: ~50%
  - Different zones: ~0%

### S.4: All Parties Active (x=4)
- All 4 parties active
- Random sender each round
- **Expected waste**: Minimal (~2%)

## Results (n=1000, d=10, 100 executions)

| Scenario | Avg Wasted | Std Dev | Min | Max | Waste % |
|----------|-----------|---------|-----|-----|---------|
| S.1 (x=1) | 528.6 pads | 12.5 | 511 | 557 | **52.86%** |
| S.2 (x=2) | 155.0 pads | 217.1 | 22 | 512 | **15.50%** |
| S.4 (x=4) | 20.3 pads | 0.7 | 20 | 23 | **2.03%** |
| **Baseline** | | | | | **75.00%** |

✅ **All scenarios beat the 75% static partition baseline!**

## Implementation Details

### Safety Conditions

**Rightward parties** (Alice, Charlie):
```python
next_end < partner_last - d
```

**Leftward parties** (Bob, Dave):
```python
next_start > partner_last + d
```

### Termination

Protocol terminates when at least one party cannot send the next message securely.

### Collision Prevention

Every pad usage is verified with an assertion to ensure perfect secrecy:
```python
assert not self.pad_usage[pad_idx], "Pad collision detected!"
```

## Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n` | 1000 | Total number of pads |
| `d` | 10 | Gap parameter (max undelivered messages) |
| `executions` | 100 | Runs per scenario for averaging |
| `min-msg-len` | 1 | Minimum message length |
| `max-msg-len` | 50 | Maximum message length |
| `seed` | None | Random seed for reproducibility |

## Theory vs Practice

### S.1 Results
- **Theory**: 50% waste (one zone unused)
- **Practice**: 52.86% waste
- **Reason**: Gap parameter `d` and message boundaries create ~3% overhead

### S.2 Results
- **Theory**: 25% average (50% same zone, 0% different zones)
- **Practice**: 15.50% waste
- **Reason**: Random selection favored different-zone pairs in this run

### S.4 Results
- **Theory**: Minimal waste
- **Practice**: 2.03% waste
- **Reason**: Gap constraints at zone boundaries prevent using last ~20 pads

---

**NYU Applied Cryptography - Spring 2026**  
**Project 1: Multi-Party One-Time Pad Protocol Design**