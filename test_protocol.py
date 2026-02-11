"""
Simple tests to verify protocol implementation works correctly.
Run this to test the basic functionality before implementing scenarios.
"""

from protocol import Protocol


def test_basic_sending():
    """Test basic message sending functionality."""
    print("Test 1: Basic message sending")
    print("-" * 50)
    
    # Create protocol with 1000 pads, gap d=10
    protocol = Protocol(n=1000, d=10)
    
    # Alice sends a message of length 5
    success = protocol.attempt_send("Alice", 5)
    print(f"Alice sends L=5: {success}")
    print(f"Alice position: {protocol.alice.current_index}")
    print(f"Pads used: {protocol.get_used_pads()}")
    
    # Bob sends a message of length 3
    success = protocol.attempt_send("Bob", 3)
    print(f"Bob sends L=3: {success}")
    print(f"Bob position: {protocol.bob.current_index}")
    print(f"Pads used: {protocol.get_used_pads()}")
    
    print(f"\n{protocol}")
    print()


def test_zone_separation():
    """Test that zones are properly separated."""
    print("Test 2: Zone separation")
    print("-" * 50)
    
    protocol = Protocol(n=100, d=5)
    
    print(f"Alice zone: [{protocol.alice.zone_min}, {protocol.alice.zone_max})")
    print(f"Bob zone: [{protocol.bob.zone_min}, {protocol.bob.zone_max})")
    print(f"Charlie zone: [{protocol.charlie.zone_min}, {protocol.charlie.zone_max})")
    print(f"Dave zone: [{protocol.dave.zone_min}, {protocol.dave.zone_max})")
    
    # Alice and Charlie should be able to send without interfering
    for i in range(10):
        alice_ok = protocol.attempt_send("Alice", 1)
        charlie_ok = protocol.attempt_send("Charlie", 1)
        if not (alice_ok and charlie_ok):
            print(f"Iteration {i}: Alice={alice_ok}, Charlie={charlie_ok}")
            break
    
    print(f"Messages sent: {protocol.messages_sent}")
    print(f"Pads used: {protocol.get_used_pads()}")
    print()


def test_gap_constraint():
    """Test that gap constraint prevents collision."""
    print("Test 3: Gap constraint (same zone)")
    print("-" * 50)
    
    protocol = Protocol(n=100, d=10)
    
    # Alice and Bob are in same zone, moving toward each other
    print(f"Initial - Alice: {protocol.alice.current_index}, Bob: {protocol.bob.current_index}")
    
    count = 0
    while not protocol.is_terminated():
        # Try alternating sends
        if count % 2 == 0:
            success = protocol.attempt_send("Alice", 2)
            if success:
                print(f"Alice sent, now at {protocol.alice.current_index}")
        else:
            success = protocol.attempt_send("Bob", 2)
            if success:
                print(f"Bob sent, now at {protocol.bob.current_index}")
        
        count += 1
        if count > 20:  # Safety limit
            print("Reached safety limit")
            break
    
    print(f"\nFinal positions - Alice: {protocol.alice.current_index}, Bob: {protocol.bob.current_index}")
    print(f"Gap between them: {abs(protocol.alice.current_index - protocol.bob.current_index)}")
    print(f"Required gap (d): {protocol.d}")
    print(f"Messages sent: {protocol.messages_sent}")
    print(f"Waste: {protocol.get_wasted_pads()} pads ({protocol.get_waste_percentage():.1f}%)")
    print()


def test_single_party_scenario():
    """Test scenario where only one party sends (should waste ~50%)."""
    print("Test 4: Single party sending (Alice only)")
    print("-" * 50)
    
    protocol = Protocol(n=1000, d=10)
    
    # Only Alice sends until she can't
    while protocol.attempt_send("Alice", 5):
        pass
    
    stats = protocol.get_statistics()
    print(f"Messages sent: {stats['messages_sent']}")
    print(f"Pads used: {stats['used_pads']}")
    print(f"Pads wasted: {stats['wasted_pads']}")
    print(f"Waste percentage: {stats['waste_percentage']:.1f}%")
    print(f"Expected waste: ~50% (Zone 2 unused)")
    print()


def test_cross_zone_scenario():
    """Test scenario where one party from each zone sends."""
    print("Test 5: Cross-zone sending (Alice & Charlie)")
    print("-" * 50)
    
    protocol = Protocol(n=1000, d=10)
    
    # Alice and Charlie alternate
    count = 0
    while not protocol.is_terminated():
        if count % 2 == 0:
            if not protocol.attempt_send("Alice", 3):
                break
        else:
            if not protocol.attempt_send("Charlie", 3):
                break
        count += 1
    
    stats = protocol.get_statistics()
    print(f"Messages sent: {stats['messages_sent']}")
    print(f"Pads used: {stats['used_pads']}")
    print(f"Pads wasted: {stats['wasted_pads']}")
    print(f"Waste percentage: {stats['waste_percentage']:.1f}%")
    print(f"Expected waste: ~0% (both zones utilized)")
    print()


if __name__ == "__main__":
    print("=" * 50)
    print("Protocol Implementation Tests")
    print("=" * 50)
    print()
    
    test_basic_sending()
    test_zone_separation()
    test_gap_constraint()
    test_single_party_scenario()
    test_cross_zone_scenario()
    
    print("=" * 50)
    print("All tests completed!")
    print("=" * 50)
