import os
year, day = [2023, 3]
ROOT_DIR: str = os.path.join(os.getcwd(), str(year), f"day{day}", "varied_solution")

class IntCom:
    """Class to handle running the intcode computer"""

    def __init__(self, memory: str):
        self.pointer: int = 0
        self.rel_base: int = 0
        self.mem: dict[int, int] = {i: int(val) for (i, val) in enumerate(memory.split(","))}
        self.halted: bool = False
        self.inputpos = 0

    def find_pos(self, mode: int, pointer: int) -> int:
        """Find value of variable based on pointer and mode"""
        match (mode):
            case 2:
                if self.mem[pointer]+self.rel_base not in self.mem:
                    self.mem[self.mem[pointer]+self.rel_base] = 0

                return self.mem[self.mem[pointer]+self.rel_base]
            case 1:
                if pointer not in self.mem:
                    self.mem[pointer] = 0

                return self.mem[pointer]
            case _:
                if self.mem[pointer] not in self.mem:
                    self.mem[self.mem[pointer]] = 0

                return self.mem[self.mem[pointer]]

    def find_pointer(self, mode: int, pointer: int) -> int:
        """Find pointer to output data to"""
        match (mode):
            case 2:
                if self.mem[pointer]+self.rel_base not in self.mem:
                    self.mem[self.mem[pointer]+self.rel_base] = 0

                return self.mem[pointer]+self.rel_base
            case _:
                if self.mem[pointer] not in self.mem:
                    self.mem[self.mem[pointer]] = 0

                return self.mem[pointer]

    def run_step(self, input: list[int]) -> int | None:
        """Runs a step of the code, with pot_input being potential input"""
        self.cur_instruction = str(self.mem[self.pointer])[-2:]
        modes = [int(x) for x in str(self.mem[self.pointer])[:-2].rjust(3, "0")]

        match (int(self.cur_instruction)):
            case 1:
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                pointer_val = self.find_pointer(modes[-3], self.pointer+3)

                self.mem[pointer_val] = var1 + var2
                self.pointer+= 4
            case 2:
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                pointer_val = self.find_pointer(modes[-3], self.pointer+3)

                self.mem[pointer_val] = var1 * var2
                self.pointer+= 4
            case 3:
                pointer_val = self.find_pointer(modes[-1], self.pointer+1)

                self.mem[pointer_val] = input[self.inputpos]
                self.inputpos += 1

                self.pointer+= 2
            case 4:
                self.pointer+= 2

                if modes[-1] == 2:
                    return self.mem[self.mem[self.pointer-1]+self.rel_base]
                if modes[-1]:
                    return self.mem[self.pointer-1]

                return self.mem[self.mem[self.pointer-1]]
            case 5:
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                if var1:
                    self.pointer= var2
                else:
                    self.pointer+= 3
            case 6:
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                if not var1:
                    self.pointer= var2
                else:
                    self.pointer+= 3
            case 7:
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                pointer_val = self.find_pointer(modes[-3], self.pointer+3)

                self.mem[pointer_val] = int(var1 < var2)

                self.pointer+= 4
            case 8:
                var1 = self.find_pos(modes[-1], self.pointer+1)
                var2 = self.find_pos(modes[-2], self.pointer+2)

                pointer_val = self.find_pointer(modes[-3], self.pointer+3)

                self.mem[pointer_val] = int(var1 == var2)

                self.pointer+= 4
            case 9:
                var1 = self.find_pos(modes[-1], self.pointer+1)

                self.rel_base += var1
                self.pointer+= 2
            case 99:
                self.halted = True
            case _:
                raise ValueError(f"Came across unexpected instruction {self.cur_instruction}")

        return None
    
if __name__ == "__main__":
    with open(os.path.join(ROOT_DIR, "solution.intcode"), 'r', encoding="utf8") as f:
        inp: list[str] = [line.strip() for line in f.readlines()]
    
    intcom = IntCom(inp[0])

    with open(os.path.join(ROOT_DIR, "input.txt"), 'r', encoding="utf8") as f:
        temp_grid: list[str] = [line.strip() for line in f.readlines()]
    
    grid = ""
    for line in temp_grid:
        grid += line

    inputs: list[int] = [len(grid), len(temp_grid[0]), *[ord(x) for x in grid]]
    
    prev_x = 0
    prev_y = 0
    y = 0
    cur_char = "Q"
    cur_loc = 0
    position_dict = {41:"OUTERLOOP", 49:"INNERLOOP", 152:"OUTERNUM", 156:"INNERNUM", 339: "SKIP", 
                     223:"OSKIP", 279: "INNERPARSE", 99: "INNERREAD", 148: "READBREAK", 264: "FOUND", 346: "END"}
    
    while not intcom.halted:
        x = intcom.run_step(inputs)

        if x:
            print(x)

        # print(intcom.cur_instruction,end=" || ")

        # if intcom.pointer in position_dict:
        #     print(f"\nAt position {position_dict[intcom.pointer]}, {prev_x, prev_y, cur_char}")
        
        # if 904 in intcom.mem:
        #     y = intcom.mem[904]

        # if 912 in intcom.mem and prev_y != intcom.mem[912]:
        #     prev_y = intcom.mem[912]
            
        # if 913 in intcom.mem and prev_x != intcom.mem[913]:
        #     prev_x = intcom.mem[913]

        # if prev_y*len(temp_grid)+prev_x+1000 in intcom.mem and cur_char != chr(intcom.mem[prev_y*len(temp_grid)+prev_x+1000]):
        #     cur_char = chr(intcom.mem[prev_y*len(temp_grid)+prev_x+1000])

        # if 909 in intcom.mem and cur_loc != intcom.mem[909]:
        #     cur_loc = intcom.mem[909]
                                                              
    # print(intcom.mem)