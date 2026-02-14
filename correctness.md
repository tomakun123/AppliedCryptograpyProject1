Theorem: In the Parallel pairs protocol with m=4 parties and n pads, no two parties ever write to the same pad index

Proof:
We prove this by partitioning the collision space and showing that collisions are impossible in each partition.

Let:
-A, B, C, D denote the four parties (Alice, Bob, Charlie, Dave)
-Zone₁ = [0, n/2-1] and Zone₂ = [n/2, n-1]
-Next(X) denote the next pad index party X will write to
-Last(X) denote the last pad index party X wrote to
-d denote the safety buffer distance

Case 1: Inter-zone collisions(between parties in different zones)
Parties A and b are restricted to Zone1, while parties C and D are restricted to Zone1
By construction:
-max(Next(A))<=n/2-1
-max(Next(B))<=n/2-1
-min(Next(C))>=n/2
-min(Next(D))>=n/2

Since Zone₁ ∩ Zone₂ = ∅, we have:
-Next(A) ≠ Next(C), Next(A) ≠ Next(D)
-Next(B) ≠ Next(C), Next(B) ≠ Next(D)

Therefore, no inter-zone collision is possible.

Case 2: Intra-zone collisions(within zone)
Alice starts at position 0 moving right (→), Bob starts at position n/2-1 moving left (←).

The protocol enforces:
-Alice sends only if: Next(A) < Last(B) - d
-Bob sends only if: Next(B) > Last(A) + d

Sub-case 2a: Initial state(no messages sent yet)
-Last(A) = -1 (undefined/no previous message)
-Last(B) = n/2 (undefined/no previous message)
-Next(A) = 0, Next(B) = n/2-1
-Distance = n/2-1 - 0 = n/2-1 > 2d (given safe initialization)
No collision possible

Sub-case 2b: After k messages have been sent by A and B combined
By induction on the number of messages:
-Base case (k=0): Shown in sub-case 2a.
-Inductive step: Assume after k messages, Last(A) + d < Last(B) - d (safety invariant holds).

When Alice sends message k+1:
-Condition checked: Next(A) < Last(B) - d
-Alice writes to Next(A)
-New invariant: Last(A) < Last(B) - d (by the send condition)
-Therefore: Last(A) + d < Last(B), maintaining safe distance

When Bob sends message k+1:
-Condition checked: Next(B) > Last(A) + d
-Bob writes to Next(B)
-New invariant: Last(B) > Last(A) + d (by the send condition)
-Therefore: Last(A) + d < Last(B), maintaining safe distance

Since both operations preserve the invariant Last(A) + d < Last(B) - d, we have:
-Last(A) < Last(A) + d < Last(B) - d < Last(B)
-Therefore: Last(A) ≠ Last(B)

By induction, no collision occurs in Zone₁ for any number of messages.

Case 3: Intra-zone collisions(within Zone2)
The proof is symmetric to Case 2:
-Charlie starts at n/2 moving right(->)
-Dave starts at n-1 moving left(<-)
-Same safety conditions apply: Next(C)<Last(D)-d and Next(D)>Last(C)+d
-By the same inductive argument, no collision occurs in Zone2.

Conclusion: Since all possible collision cases(inter-zone and both intra-zone cases) are proven impossible, the protocol guarantees that no two parties ever write to the same pad index.
