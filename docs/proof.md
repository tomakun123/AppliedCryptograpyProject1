**Definitions**

Pad Sequence:
    Let there be a shared ordered sequence of pads such that P = {p0,p1,...,p(n-1)} where each pad may be used once.

Parties & Positions
    Let there be 4 parties par1, par2, par3, par4 where each contains an index that they will start at and use pads as they move along.
    Initial Positions:
        Let n be the length of the message
        par1 --> starts at 0, moves right
        par2 --> starts at [(n//2)-1], moves left
        par3 --> starts at (n//2), moves right
        par4 --> starts at n-1, moves left

Used Pads:
    A pad is considered used at send time where U ⊆ {0,...,n-1} is the set of pad indices that have been used

Sending Conditions:
    A party member is allowed to use a pad and send messaages if and only if:
        pi ∈/ (not an element of) U
        Two parties cannot choose the same pad index, and their claimed pad regions never intersect 
        OR 
        par1[ind]​≤par2[ind]​<par3[ind]​≤par4[ind]​, where ind represents the index of that party member
    