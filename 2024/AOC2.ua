InputToNArray ← ⊜(□⊜⋕≠@ .)≠@\n.
IsSafe        ← /+≡(/××⊃(>0|<4)≡/-◫2)[⇌.]

DATA ← InputToNArray &fras "2"

$"Part 1: _"/+≡(IsSafe °□) DATA

X                ← °□⊡ 1 DATA                     # a single report..
RemoveNth        ← ⍜⊏≡⋅[]                         # removes the nth element, can also be written as "⍜↻(↘1)"
IsSafeToleranced ← ≥1/+≡IsSafe≡(RemoveNth :X) ⇡⧻X # checks if any variant of the report is safe

$"Part 2 (operating on single report _): _":(IsSafeToleranced °□) X
