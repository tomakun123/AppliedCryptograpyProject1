class Party:
    """
    Represents a party in the protocol.
    Each party has a zone, a starting position, and a direction of movement.
    """
    
    def __init__(self, name, start_index, direction, zone_min, zone_max):
        """
        Initialize a party.
        
        Args:
            name: Party name (Alice, Bob, Charlie, Dave)
            start_index: Starting pad index
            direction: +1 for rightward movement, -1 for leftward movement
            zone_min: Minimum index in this party's zone (inclusive)
            zone_max: Maximum index in this party's zone (exclusive)
        """
        self.name = name
        self.start_index = start_index
        self.direction = direction  # +1 for right, -1 for left
        self.zone_min = zone_min
        self.zone_max = zone_max
        self.current_index = start_index
        self.has_sent = False
    
    def get_next_pad_index(self):
        """Returns the next pad index this party would use."""
        return self.current_index
    
    def get_last_used_index(self):
        """
        Get the last index used by this party.
        If party hasn't sent yet, returns their starting position.
        """
        if not self.has_sent:
            return self.start_index
        
        if self.direction > 0:
            # Moving right: last used is one before current
            return self.current_index - 1
        else:
            # Moving left: last used is one after current
            return self.current_index + 1
    
    def can_send(self, message_length, partner_last_index, d, partner_has_sent):
        """
        Check if this party can safely send a message of given length.
        
        Args:
            message_length: Number of pads needed (L)
            partner_last_index: Last pad index used by partner in same zone
            d: Safety gap parameter
            partner_has_sent: Whether partner has sent at least one message
        
        Returns:
            True if message can be sent safely, False otherwise
        """
        # Calculate which pads would be used
        if self.direction > 0:  # Moving right
            next_start = self.current_index
            next_end = self.current_index + message_length - 1
            
            # Check if message fits in zone
            if next_end >= self.zone_max:
                return False
            
            # Safety condition: next_end < partner_last_index - d
            # (Ensure gap of at least d pads between our message and partner's territory)
            if partner_has_sent:
                if not (next_end < partner_last_index - d):
                    return False
            else:
                # Partner hasn't sent; check against their starting position
                if not (next_end < partner_last_index - d):
                    return False
                    
        else:  # Moving left (direction < 0)
            next_start = self.current_index - message_length + 1
            next_end = self.current_index
            
            # Check if message fits in zone
            if next_start < self.zone_min:
                return False
            
            # Safety condition: next_start > partner_last_index + d
            # (Ensure gap of at least d pads between our message and partner's territory)
            if partner_has_sent:
                if not (next_start > partner_last_index + d):
                    return False
            else:
                # Partner hasn't sent; check against their starting position
                if not (next_start > partner_last_index + d):
                    return False
        
        return True
    
    def consume_pads(self, message_length):
        """
        Consume pads for sending a message and advance position.
        
        Args:
            message_length: Number of pads to consume
        
        Returns:
            List of pad indices that were consumed
        """
        if self.direction > 0:
            # Rightward: consume [current_index, current_index + L - 1]
            pads_used = list(range(self.current_index, self.current_index + message_length))
            self.current_index += message_length
        else:
            # Leftward: consume [current_index - L + 1, current_index]
            pads_used = list(range(self.current_index - message_length + 1, self.current_index + 1))
            self.current_index -= message_length
        
        self.has_sent = True
        return pads_used
    
    def __repr__(self):
        return f"{self.name}(pos={self.current_index}, dir={'->' if self.direction > 0 else '<-'})"


class Protocol:
    """
    Implements the Parallel Pairs protocol for 4-party OTP communication.
    Parties are divided into two teams, each operating in their own zone.
    """
    
    def __init__(self, n, d=10):
        """
        Initialize the protocol.
        
        Args:
            n: Total number of pads in the sequence
            d: Gap parameter (max undelivered messages)
        """
        self.n = n
        self.d = d
        self.pad_usage = [False] * n
        
        # Split pad sequence into two zones
        zone_split = n // 2
        
        # Team 1: Alice & Bob (Zone 1: [0, zone_split))
        self.alice = Party("Alice", 0, +1, 0, zone_split)
        self.bob = Party("Bob", zone_split - 1, -1, 0, zone_split)
        
        # Team 2: Charlie & Dave (Zone 2: [zone_split, n))
        self.charlie = Party("Charlie", zone_split, +1, zone_split, n)
        self.dave = Party("Dave", n - 1, -1, zone_split, n)
        
        # Dictionary for easy access
        self.parties = {
            "Alice": self.alice,
            "Bob": self.bob,
            "Charlie": self.charlie,
            "Dave": self.dave
        }
        
        # Define partner pairs (same zone)
        self.pairs = {
            "Alice": self.bob,
            "Bob": self.alice,
            "Charlie": self.dave,
            "Dave": self.charlie
        }
        
        # Statistics
        self.messages_sent = 0
        self.messages_attempted = 0
    
    def attempt_send(self, party_name, message_length):
        """
        Attempt to send a message from the given party.
        
        Args:
            party_name: Name of the party attempting to send
            message_length: Length of message in pads
        
        Returns:
            True if message was sent successfully, False otherwise
        """
        self.messages_attempted += 1
        
        party = self.parties[party_name]
        partner = self.pairs[party_name]
        
        # Check safety condition
        if not party.can_send(message_length, partner.get_last_used_index(), self.d, partner.has_sent):
            return False
        
        # Consume pads
        pads_used = party.consume_pads(message_length)
        
        # Mark pads as used and verify no reuse (perfect secrecy check)
        for pad_idx in pads_used:
            assert not self.pad_usage[pad_idx], \
                f"COLLISION: Pad {pad_idx} was already used! Perfect secrecy violated!"
            self.pad_usage[pad_idx] = True
        
        self.messages_sent += 1
        return True
    
    def is_terminated(self):
        """
        Check if protocol has terminated.
        Termination occurs when no party can send even a minimal message.
        
        Returns:
            True if protocol is terminated, False otherwise
        """
        # Check if any party can send a minimal message (length 1)
        for party_name in self.parties:
            party = self.parties[party_name]
            partner = self.pairs[party_name]
            
            if party.can_send(1, partner.get_last_used_index(), 
                            self.d, partner.has_sent):
                return False  # At least one party can still send
        
        return True
    
    def get_wasted_pads(self):
        """Return count of unused pads."""
        return self.n - sum(self.pad_usage)
    
    def get_used_pads(self):
        """Return count of used pads."""
        return sum(self.pad_usage)
    
    def get_waste_percentage(self):
        """Return percentage of pads wasted."""
        return (self.get_wasted_pads() / self.n) * 100
    
    def get_statistics(self):
        """
        Return protocol statistics.
        
        Returns:
            Dictionary with protocol statistics
        """
        return {
            'total_pads': self.n,
            'used_pads': self.get_used_pads(),
            'wasted_pads': self.get_wasted_pads(),
            'waste_percentage': self.get_waste_percentage(),
            'messages_sent': self.messages_sent,
            'messages_attempted': self.messages_attempted,
            'terminated': self.is_terminated()
        }
    
    def __repr__(self):
        return (f"Protocol(n={self.n}, d={self.d}, "
                f"used={self.get_used_pads()}, "
                f"wasted={self.get_wasted_pads()}, "
                f"msgs={self.messages_sent})")
