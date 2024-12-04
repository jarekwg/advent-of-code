InputToNArray ← ⊜(□⊜⋕≠@ .)≠@\n.
IsSafe        ← /+≡(/××⊃(>0|<4)≡/-◫2)[⇌.]

DATA ← InputToNArray &fras "2"

$"Part 1: _"/+≡(IsSafe°□) DATA

RemoveNth        ← ⍜⊏≡⋅[] # removes the nth element, can also be written as "⍜↻(↘1)"
GenPerms         ← ≡RemoveNth⊙¤⇡⧻.
IsSafeToleranced ← ≥1/+≡IsSafe GenPerms # checks if any variant of the report is safe

$"Part 2: _" /+≡(IsSafeToleranced°□) DATA
