import argparse
import statistics
from simulator import run_scenario_1, run_scenario_2, run_scenario_4, run_multiple_executions


def calculate_statistics(results):
    """
    Calculate statistical metrics from multiple execution results.
    
    Args:
        results: List of result dictionaries from scenario executions
    
    Returns:
        Dictionary with statistical metrics
    """
    wasted_pads = [r['wasted_pads'] for r in results]
    waste_percentages = [r['waste_percentage'] for r in results]
    messages_sent = [r['messages_sent'] for r in results]
    used_pads = [r['used_pads'] for r in results]
    
    return {
        'avg_wasted': statistics.mean(wasted_pads),
        'std_wasted': statistics.stdev(wasted_pads) if len(wasted_pads) > 1 else 0,
        'min_wasted': min(wasted_pads),
        'max_wasted': max(wasted_pads),
        'avg_waste_pct': statistics.mean(waste_percentages),
        'std_waste_pct': statistics.stdev(waste_percentages) if len(waste_percentages) > 1 else 0,
        'avg_messages': statistics.mean(messages_sent),
        'avg_used': statistics.mean(used_pads),
        'executions': len(results)
    }


def print_header():
    """Print the header for the simulation."""
    print("\n" + "=" * 80)
    print("Multi-Party One-Time Pad Protocol Simulation")
    print("Protocol: Parallel Pairs (m=4)")
    print("=" * 80)


def print_configuration(n, d, executions, min_msg_len, max_msg_len):
    """Print the simulation configuration."""
    print("\nConfiguration:")
    print(f"  Total pads (n): {n}")
    print(f"  Gap parameter (d): {d}")
    print(f"  Executions per scenario: {executions}")
    print(f"  Message length range: [{min_msg_len}, {max_msg_len}]")
    print(f"  Static partition baseline (worst case): 75.0%")


def print_scenario_results(scenario_name, stats, n):
    """Print results for a single scenario."""
    print(f"\n{scenario_name}:")
    print(f"  Executions: {stats['executions']}")
    print(f"  Average pads used: {stats['avg_used']:.1f} / {n}")
    print(f"  Average pads wasted: {stats['avg_wasted']:.1f} ± {stats['std_wasted']:.1f}")
    print(f"  Wasted pads range: [{stats['min_wasted']}, {stats['max_wasted']}]")
    print(f"  Average waste percentage: {stats['avg_waste_pct']:.2f}% ± {stats['std_waste_pct']:.2f}%")
    print(f"  Average messages sent: {stats['avg_messages']:.1f}")


def print_summary_table(s1_stats, s2_stats, s4_stats):
    """Print a summary table comparing all scenarios."""
    print("\n" + "=" * 80)
    print("Summary Table")
    print("=" * 80)
    print(f"{'Scenario':<12} {'Avg Wasted':<15} {'Std Dev':<12} {'Min':<8} {'Max':<8} {'Waste %':<12}")
    print("-" * 80)
    
    # S.1
    print(f"{'S.1 (x=1)':<12} "
          f"{s1_stats['avg_wasted']:>8.1f} pads   "
          f"{s1_stats['std_wasted']:>8.1f}    "
          f"{s1_stats['min_wasted']:>6}  "
          f"{s1_stats['max_wasted']:>6}  "
          f"{s1_stats['avg_waste_pct']:>6.2f}%")
    
    # S.2
    print(f"{'S.2 (x=2)':<12} "
          f"{s2_stats['avg_wasted']:>8.1f} pads   "
          f"{s2_stats['std_wasted']:>8.1f}    "
          f"{s2_stats['min_wasted']:>6}  "
          f"{s2_stats['max_wasted']:>6}  "
          f"{s2_stats['avg_waste_pct']:>6.2f}%")
    
    # S.4
    print(f"{'S.4 (x=4)':<12} "
          f"{s4_stats['avg_wasted']:>8.1f} pads   "
          f"{s4_stats['std_wasted']:>8.1f}    "
          f"{s4_stats['min_wasted']:>6}  "
          f"{s4_stats['max_wasted']:>6}  "
          f"{s4_stats['avg_waste_pct']:>6.2f}%")
    
    print("-" * 80)
    print(f"{'Baseline':<12} {'(static partition worst case)':>45} {'75.00%':>12}")
    print("=" * 80)

def main():
    """Main function to run the simulation."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Multi-Party OTP Protocol Simulator')
    parser.add_argument('--n', type=int, default=1000, 
                       help='Total number of pads (default: 1000)')
    parser.add_argument('--d', type=int, default=10,
                       help='Gap parameter (default: 10)')
    parser.add_argument('--executions', type=int, default=100,
                       help='Number of executions per scenario (default: 100)')
    parser.add_argument('--min-msg-len', type=int, default=1,
                       help='Minimum message length (default: 1)')
    parser.add_argument('--max-msg-len', type=int, default=50,
                       help='Maximum message length (default: 50)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility (default: None)')
    
    args = parser.parse_args()
    
    # Set random seed if provided
    if args.seed is not None:
        import random
        random.seed(args.seed)
        print(f"Random seed set to: {args.seed}")
    
    # Print header and configuration
    print_header()
    print_configuration(args.n, args.d, args.executions, args.min_msg_len, args.max_msg_len)
    
    print("\n" + "=" * 80)
    print("Running simulations...")
    print("=" * 80)
    
    # Run Scenario S.1
    print("\nRunning Scenario S.1 (1 active party)...", end=" ", flush=True)
    s1_results = run_multiple_executions(
        run_scenario_1, args.executions, args.n, args.d, 
        args.min_msg_len, args.max_msg_len
    )
    s1_stats = calculate_statistics(s1_results)
    print("Done")
    
    # Run Scenario S.2
    print("Running Scenario S.2 (2 active parties)...", end=" ", flush=True)
    s2_results = run_multiple_executions(
        run_scenario_2, args.executions, args.n, args.d,
        args.min_msg_len, args.max_msg_len
    )
    s2_stats = calculate_statistics(s2_results)
    print("Done")
    
    # Run Scenario S.4
    print("Running Scenario S.4 (4 active parties)...", end=" ", flush=True)
    s4_results = run_multiple_executions(
        run_scenario_4, args.executions, args.n, args.d,
        args.min_msg_len, args.max_msg_len
    )
    s4_stats = calculate_statistics(s4_results)
    print("Done")
    
    # Print detailed results
    print("\n" + "=" * 80)
    print("Detailed Results")
    print("=" * 80)
    
    print_scenario_results("Scenario S.1 (1 active party)", s1_stats, args.n)
    print_scenario_results("Scenario S.2 (2 active parties)", s2_stats, args.n)
    print_scenario_results("Scenario S.4 (4 active parties)", s4_stats, args.n)
    
    # Print summary table
    print_summary_table(s1_stats, s2_stats, s4_stats)

    print("Simulation complete!")

if __name__ == "__main__":
    main()
