class Program:
    A: int
    B: int
    C: int
    program: list[int]
    iptr: int
    out: list[int]

    def __init__(self, program: list[int]) -> None:
        self.program = program

    def combo(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case _:
                raise ValueError("Invalid combo operand")

    def process_instruction(self, opcode: int, operand: int):
        self.iptr += 2
        match opcode:
            case 0:  # adv
                self.A >>= self.combo(operand)
            case 1:  # bxl
                self.B ^= operand
            case 2:  # bst
                self.B = self.combo(operand) % 8
            case 3:  # jnz
                if self.A != 0:
                    self.iptr = operand
            case 4:  # bxc
                self.B ^= self.C
            case 5:  # out
                self.out.append(self.combo(operand) % 8)
            case 6:  # bdv
                self.B = self.A >> self.combo(operand)
            case 7:  # cdv
                self.C = self.A >> self.combo(operand)

    def run(self, A: int, B: int, C: int) -> list[int]:
        self.A = A
        self.B = B
        self.C = C
        self.iptr = 0
        self.out = []
        while True:
            try:
                self.process_instruction(
                    self.program[self.iptr], self.program[self.iptr + 1]
                )
            except IndexError:
                break
        return self.out


[A], [B], [C], _, PROGRAM = [
    [*map(int, (s + ":0").split(":")[1].split(","))] for s in open("17")
]

program = Program(PROGRAM)

print(f"Part 1: {program.run(A, B, C)}")

# Cracking open the sample input:
# 2,4: B = A % 8                                        (ie B is now holding the last three bits of A)
# 1,2: B ^= 2 (ie XOR with 010)                         (ie B now has the last three bits of A, with the second one flipped)
# 7,5: C = A >> B                                       (ie C is now holding the result of bitshifting A by B. Only the three LSBs will be used though.)
# 1,7: B ^= 7 (ie XOR with 111) (ie flip all bits)      (ie B now has the last three bits of A with the first & third flipped)
# 4,4: B ^= C (ie XOR with C)                           (ie B now has the last three bits of A with the first & third flipped, XORed with C)
# 0,3: A >>= 3 (ie drop the last 3 bits, aka div by 8)
# 5,5: print(B % 8)
# 3,0: go back to the start, unless A is 0

# Deductions
# 1. The program loops until A is 0. A is divided by 8 with each iteration.
#   => We need the program to print out 16 numbers, so it must loop 16 times.
#     => A must in the range [8^15, 8^16).
# 2. Each run of three bits in A is responsible for giving us one of the 16 numbers, however we
#    don't get clear isolation, as the three LSB bits pick out and are then entagled with three
#    other bits in A prior to printing out one of our 16 numbers.
#   => If we start from the back, with A being a three bit number, and us needing to find a value
#      for it that will give us the last number in the program, we can then work backwards to
#      find the value of A that will give us the second last number, and so on.
#     => This drops our search space down from 8^16-8^15 to 8*16, which is trivial!

a = 0
for i in range(len(PROGRAM)):
    a <<= 3
    # Find the lowest value for A that will print the last number in the program.
    # NOTE: We should be finding ALL values of A here, in case the lowest one falls over further
    # down the line, however simply leaving it up to the next iteration to do this searching is
    # sufficient for the sample data provided. Yes, it does mean searching goes up from <8 to
    # thousands, but we still get sub-second runtime.
    while program.run(a, B, C) != PROGRAM[-i - 1 :]:
        a += 1

print(f"Part 2: {a}")
