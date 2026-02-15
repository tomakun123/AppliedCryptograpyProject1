# Multi-Party OTP Protocol - Testing & Simulation Guide

**Project 1 Applied Cryptography**  
Thomas Motais De Narbonne, Raymond Lin, Kanthimathi Sundararajan

## Overview

This testing suite evaluates the Parallel Pairs protocol through statistical simulations across three scenarios (S.1, S.2, S.4) to measure pad waste and compare against the static partition baseline.

For protocol implementation details, see [README_PROTOCOL.md](README_PROTOCOL.md).

### What This Program Does

The simulation suite:
- Runs multiple protocol executions with random message patterns
- Measures pad usage and waste across different scenarios
- Provides statistical analysis (mean, std dev, min, max)
- Compares results against the 75% static partition baseline
- Validates perfect secrecy (no pad collisions)  

## Quick Start

Run the full simulation with default parameters (n=1000, d=10, 100 executions per scenario):

```bash
python main.py
```

**Expected output:**
- Configuration summary
- Progress indicators for each scenario
- Detailed results with statistics
- Summary comparison table
- Analysis vs. theoretical expectations

## Command-Line Options

The simulation supports extensive customization through CLI arguments:

```bash
# Custom pad count
python main.py --n 2000

# Custom gap parameter
python main.py --d 20

# Custom number of executions per scenario
python main.py --executions 200

# Custom message length range (random between min and max)
python main.py --min-msg-len 5 --max-msg-len 100

# Reproducible results with random seed
python main.py --seed 42

# Combine multiple parameters
python main.py --n 5000 --d 15 --executions 500 --seed 42

# Quick test with fewer executions
python main.py --executions 10
```

### Available Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--n` | 1000 | Total number of pads in sequence |
| `--d` | 10 | Gap parameter (max undelivered messages) |
| `--executions` | 100 | Number of times to run each scenario |
| `--min-msg-len` | 1 | Minimum message length (in pads) |
| `--max-msg-len` | 50 | Maximum message length (in pads) |
| `--seed` | None | Random seed for reproducibility |

### What Each File Does

**protocol.py** ([implementation guide](README_PROTOCOL.md))
- Implements `Party` and `Protocol` classes
- Handles safety conditions and pad consumption
- Enforces perfect secrecy with collision detection

**simulator.py**
- Implements `run_scenario_1()`, `run_scenario_2()`, `run_scenario_4()`
- Manages random party/message selection
- Handles consecutive failure detection
- Provides `run_multiple_executions()` helper

**main.py**
- CLI argument parsing
- Statistical analysis (`calculate_statistics()`)
- Formatted output and result tables
- Analysis and comparison functions

## Test Scenarios

The simulation evaluates three scenarios as specified in the project requirements:

### Scenario S.1: Single Active Party (x=1)

**Setup:**
- Randomly select 1 party at the start
- Only that party sends messages
- Messages continue until the party cannot send safely

**Expected Behavior:**
- One zone remains completely unused
- Theoretical waste: ~50%
- Actual waste: ~53% (gap parameter overhead)

**Purpose:** Tests worst-case scenario for protocol efficiency

### Scenario S.2: Two Active Parties (x=2)

**Setup:**
- Randomly select 2 parties at the start
- Each message round randomly chooses one of the 2 to send
- Continues until neither can send safely

**Expected Behavior:**
- **Same zone** (Alice & Bob OR Charlie & Dave): ~50% waste (other zone unused)
- **Different zones** (Alice & Charlie, etc.): ~0% waste (both zones utilized)
- Average across all combinations: ~25% waste

**Purpose:** Tests protocol with partial participation and zone utilization variance

### Scenario S.4: All Parties Active (x=4)

**Setup:**
- All 4 parties are active
- Each message round randomly selects any party to send
- Continues until no party can send safely

**Expected Behavior:**
- Both zones fully utilized
- Theoretical waste: Minimal (~2%)
- Highest efficiency scenario

**Purpose:** Tests protocol under optimal conditions with full participation

## Simulation Results

### Baseline: Static Partition

For comparison, a naive static partition approach gives each of the 4 parties exactly 25% of the pads:
- **Worst case waste**: 75% (when only 1 party sends, 3/4 of pads unused)
- This is the baseline our protocol must beat

### Measured Results (n=1000, d=10, 100 executions)

| Scenario | Avg Wasted | Std Dev | Min | Max | Waste % | vs Baseline |
|----------|-----------|---------|-----|-----|---------|-------------|
| S.1 (x=1) | 528.6 pads | 12.5 | 511 | 557 | **52.86%** | 22% better |
| S.2 (x=2) | 155.0 pads | 217.1 | 22 | 512 | **15.50%** | 59% better |
| S.4 (x=4) | 20.3 pads | 0.7 | 20 | 23 | **2.03%** | 73% better |
| **Baseline** | | | | | **75.00%** | - |

### Key Findings

**All scenarios significantly outperform the static partition baseline**

**S.1 Analysis:**
- Actual: 52.86% vs Expected: ~50%
- Small overhead from gap parameter `d` and message boundaries
- One zone completely wasted as expected

**S.2 Analysis:**
- Actual: 15.50% vs Expected: ~25%
- Better than expected due to favorable random party selections
- High variance shows dependency on which parties are chosen
- Range [22, 512] reflects same-zone vs different-zone pairings

**S.4 Analysis:**
- Actual: 2.03% vs Expected: ~2%
- Matches theoretical predictions closely
- Low variance (±0.7) shows consistent performance
- Waste primarily from gap constraints at zone boundaries

## Statistical Methodology

### Execution Process

1. **Initialization**: Create fresh protocol instance with specified `n` and `d`
2. **Party Selection**: Randomly choose active parties for scenario
3. **Message Loop**:
   - Randomly select message length from [min_msg_len, max_msg_len]
   - Randomly select sender from active parties
   - Attempt to send message
   - Continue until protocol terminates or max consecutive failures reached
4. **Data Collection**: Record pads used, wasted, messages sent
5. **Repeat**: Run scenario multiple times (default: 100)

### Statistical Measures

- **Mean**: Average waste across all executions
- **Std Dev**: Variance in waste (high variance indicates scenario-dependent behavior)
- **Min/Max**: Range of observed waste values
- **Waste %**: Percentage of total pads unused

### Reproducibility

Use `--seed` parameter to get consistent results:
```bash
python main.py --seed 42
```

This sets the random number generator seed, ensuring:
- Same party selections
- Same message lengths
- Same sender choices
- Identical results across runs

### Verify Perfect Secrecy

The protocol includes assertions that will raise an error if any pad is used twice. If you see `AssertionError: Pad collision detected!`, there's a bug in the implementation.

## For Protocol Implementation Details

See [README_PROTOCOL.md](README_PROTOCOL.md)