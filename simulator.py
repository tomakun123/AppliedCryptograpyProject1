"""
Scenario simulation functions for the multi-party OTP protocol.
Implements S.1, S.2, and S.4 test scenarios.
"""

import random
from protocol import Protocol


def run_scenario_1(n, d, min_msg_length=1, max_msg_length=50):
    """
    Scenario S.1: Only 1 randomly chosen party sends messages.
    
    Args:
        n: Total number of pads
        d: Gap parameter
        min_msg_length: Minimum message length
        max_msg_length: Maximum message length
    
    Returns:
        Dictionary with simulation results
    """
    protocol = Protocol(n=n, d=d)
    
    # Randomly select 1 party to be active
    active_party = random.choice(["Alice", "Bob", "Charlie", "Dave"])
    
    messages_sent = 0
    
    # Send messages until protocol terminates
    while not protocol.is_terminated():
        # Random message length
        msg_length = random.randint(min_msg_length, max_msg_length)
        
        # Attempt to send from active party
        success = protocol.attempt_send(active_party, msg_length)
        
        if success:
            messages_sent += 1
        else:
            # If the active party can't send, protocol should terminate
            break
    
    return {
        'scenario': 'S.1',
        'active_party': active_party,
        'total_pads': n,
        'used_pads': protocol.get_used_pads(),
        'wasted_pads': protocol.get_wasted_pads(),
        'waste_percentage': protocol.get_waste_percentage(),
        'messages_sent': messages_sent,
        'messages_attempted': protocol.messages_attempted
    }


def run_scenario_2(n, d, min_msg_length=1, max_msg_length=50):
    """
    Scenario S.2: 2 randomly chosen parties send messages.
    Who sends each message is randomly selected.
    
    Args:
        n: Total number of pads
        d: Gap parameter
        min_msg_length: Minimum message length
        max_msg_length: Maximum message length
    
    Returns:
        Dictionary with simulation results
    """
    protocol = Protocol(n=n, d=d)
    
    # Randomly select 2 parties to be active
    all_parties = ["Alice", "Bob", "Charlie", "Dave"]
    active_parties = random.sample(all_parties, 2)
    
    messages_sent = 0
    consecutive_failures = 0
    max_consecutive_failures = 50  # Prevent infinite loops
    
    # Send messages until protocol terminates or active parties can't send
    while not protocol.is_terminated() and consecutive_failures < max_consecutive_failures:
        # Random message length
        msg_length = random.randint(min_msg_length, max_msg_length)
        
        # Randomly choose which of the 2 active parties sends
        sender = random.choice(active_parties)
        
        # Attempt to send
        success = protocol.attempt_send(sender, msg_length)
        
        if success:
            messages_sent += 1
            consecutive_failures = 0  # Reset counter on success
        else:
            consecutive_failures += 1
    
    return {
        'scenario': 'S.2',
        'active_parties': active_parties,
        'total_pads': n,
        'used_pads': protocol.get_used_pads(),
        'wasted_pads': protocol.get_wasted_pads(),
        'waste_percentage': protocol.get_waste_percentage(),
        'messages_sent': messages_sent,
        'messages_attempted': protocol.messages_attempted
    }


def run_scenario_4(n, d, min_msg_length=1, max_msg_length=50):
    """
    Scenario S.4: All 4 parties send messages.
    Who sends each message is randomly selected.
    
    Args:
        n: Total number of pads
        d: Gap parameter
        min_msg_length: Minimum message length
        max_msg_length: Maximum message length
    
    Returns:
        Dictionary with simulation results
    """
    protocol = Protocol(n=n, d=d)
    
    # All 4 parties are active
    active_parties = ["Alice", "Bob", "Charlie", "Dave"]
    
    messages_sent = 0
    consecutive_failures = 0
    max_consecutive_failures = 100  # Prevent infinite loops (4 parties, more attempts needed)
    
    # Send messages until protocol terminates or all active parties can't send
    while not protocol.is_terminated() and consecutive_failures < max_consecutive_failures:
        # Random message length
        msg_length = random.randint(min_msg_length, max_msg_length)
        
        # Randomly choose which party sends
        sender = random.choice(active_parties)
        
        # Attempt to send
        success = protocol.attempt_send(sender, msg_length)
        
        if success:
            messages_sent += 1
            consecutive_failures = 0  # Reset counter on success
        else:
            consecutive_failures += 1
    
    return {
        'scenario': 'S.4',
        'active_parties': active_parties,
        'total_pads': n,
        'used_pads': protocol.get_used_pads(),
        'wasted_pads': protocol.get_wasted_pads(),
        'waste_percentage': protocol.get_waste_percentage(),
        'messages_sent': messages_sent,
        'messages_attempted': protocol.messages_attempted
    }


def run_multiple_executions(scenario_func, num_executions, n, d, min_msg_length=1, max_msg_length=50):
    """
    Run a scenario multiple times and collect statistics.
    
    Args:
        scenario_func: The scenario function to run (run_scenario_1, run_scenario_2, or run_scenario_4)
        num_executions: Number of times to run the scenario
        n: Total number of pads
        d: Gap parameter
        min_msg_length: Minimum message length
        max_msg_length: Maximum message length
    
    Returns:
        List of results from each execution
    """
    results = []
    
    for i in range(num_executions):
        result = scenario_func(n=n, d=d, min_msg_length=min_msg_length, max_msg_length=max_msg_length)
        results.append(result)
    
    return results


if __name__ == "__main__":
    # Quick test of scenarios
    print("Testing Scenario Functions")
    print("=" * 60)
    
    # Test S.1
    print("\nScenario S.1 (1 active party):")
    result = run_scenario_1(n=1000, d=10)
    print(f"  Active: {result['active_party']}")
    print(f"  Used: {result['used_pads']}, Wasted: {result['wasted_pads']} ({result['waste_percentage']:.1f}%)")
    print(f"  Messages: {result['messages_sent']}")
    
    # Test S.2
    print("\nScenario S.2 (2 active parties):")
    result = run_scenario_2(n=1000, d=10)
    print(f"  Active: {result['active_parties']}")
    print(f"  Used: {result['used_pads']}, Wasted: {result['wasted_pads']} ({result['waste_percentage']:.1f}%)")
    print(f"  Messages: {result['messages_sent']}")
    
    # Test S.4
    print("\nScenario S.4 (4 active parties):")
    result = run_scenario_4(n=1000, d=10)
    print(f"  Active: {result['active_parties']}")
    print(f"  Used: {result['used_pads']}, Wasted: {result['wasted_pads']} ({result['waste_percentage']:.1f}%)")
    print(f"  Messages: {result['messages_sent']}")
    
    print("\n" + "=" * 60)
