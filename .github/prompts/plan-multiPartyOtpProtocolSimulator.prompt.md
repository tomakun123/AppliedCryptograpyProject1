# Plan: Multi-Party OTP Protocol Simulator

This implements the "Parallel Pairs" protocol for 4-party one-time pad communication with variable-length messages. The program will simulate message sending under safety constraints, track pad usage, and measure waste across three test scenarios (S.1, S.2, S.4) over 100 executions each. Key decisions: `d=10` for gap parameter, configurable `n` (pad count), and messages of length L consume L consecutive pads.

## Steps

### 1. Create Party class (`protocol.py`)
- Attributes: `name`, `start_index`, `direction` (±1), `zone_min`, `zone_max`, `current_index`
- Method: `can_send(message_length, other_party_last_index, d)` → checks safety condition based on direction
- Method: `consume_pads(message_length)` → advances `current_index` by L in the party's direction
- Method: `get_next_pad_index()` → returns the next pad this party would use

### 2. Create Protocol class (`protocol.py`)
- Initialize 4 parties with zones (Alice/Bob: [0, n/2), Charlie/Dave: [n/2, n))
- Track `pad_usage` array (boolean array of length n)
- Method: `attempt_send(party, message_length)` → checks safety for both parties in the pair, consumes pads if valid, returns success/failure
- Method: `is_terminated()` → checks if any party cannot send their next message (termination condition)
- Method: `get_wasted_pads()` → returns count of unused pads

### 3. Implement safety condition logic (`protocol.py`)
- For rightward parties (Alice, Charlie): `next_index + L - 1 < partner_last_index - d`
- For leftward parties (Bob, Dave): `next_index - L + 1 > partner_last_index + d`
- Ensure parties stay within zone boundaries
- Handle initial state (first message from each party always allowed if within zone+gap)

### 4. Create scenario simulation functions (`simulator.py`)
- `run_scenario_1(n, d, active_parties=1)` → randomly select 1 party at start, only that party sends until termination
- `run_scenario_2(n, d, active_parties=2)` → randomly select 2 parties at start, randomly alternate between them
- `run_scenario_4(n, d, active_parties=4)` → all 4 parties active, randomly select sender each iteration
- Each function: randomly chooses message length L (need to define range), attempts send, repeats until protocol terminates
- Returns: total pads used, wasted pads, message count

### 5. Create statistics and testing harness (`main.py`)
- Configuration: `n` (configurable via CLI or default 1000), `d=10`, executions=100
- Message length: random uniform in range [1, 50] (clarify if different range needed)
- Run each scenario 100 times, collect wasted pad counts
- Calculate: mean, std deviation, min, max wasted pads per scenario
- Calculate waste percentage vs. static partition baseline (75% for worst case)

### 6. Add output and visualization (`main.py`)
- Print summary table: Scenario | Avg Wasted | Std Dev | Min | Max | Waste %
- Compare against static partition (75% worst case)

## Verification

- Run `python main.py --n 1000` to execute all scenarios with default parameters
- Verify S.1 waste ≈ 50% (one zone unused)
- Verify S.2 waste varies based on which pairs are active (0-50%)
- Verify S.4 uses most pads (lowest waste)
- Check that no pad is ever used twice (assertion in `Protocol.attempt_send`)
- Test edge cases: n=100, n=10000, d=1, d=100

## Decisions

- **Message length distribution**: Using uniform random [1, 50] bytes (can be adjusted)
- **Initial state**: Parties start at zone boundaries; `Last()` for each party is their start position before first message
- **Random seed**: Not fixed initially to get true distribution; can add `--seed` flag for reproducibility
- **Zone boundary**: Dave starts at index `n-1` (not `n`, since indices are 0-based)
- **Termination check**: Performed after each message attempt with a hypothetical next message of length 1

## Configuration Parameters

- **d (gap parameter)**: 10 (max undelivered messages)
- **n (total pads)**: Configurable via CLI (default 1000)
- **Executions per scenario**: 100
- **Message length**: Variable (L bytes = L pads consumed)

## Expected Outcomes

- **Scenario S.1** (1 active party): ~50% waste (one zone completely unused)
- **Scenario S.2** (2 active parties): 
  - Same zone (e.g., Alice & Bob): ~50% waste
  - Different zones (e.g., Alice & Charlie): ~0% waste
  - Average: ~25% waste
- **Scenario S.4** (4 active parties): Lowest waste (optimal zone utilization)
- All scenarios should beat the 75% worst-case waste of static partition
