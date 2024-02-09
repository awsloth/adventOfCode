## Instructions

1  {a} {b} {c} - c = a + b
2  {a} {b} {c} - c = a * b
3  {a}         - a = input
4  {a}         - output a
5  {a} {b}     - if a: GOTO b
6  {a} {b}     - if not a: GOTO b
7  {a} {b} {c} - c = (a < b)
8  {a} {b} {c} - c = (a == b)
9  {a}         - relbase += a
99             - halt

0 - memory address (position from the data at x in memory)
1 - direct         (value x)
2 - relative base  (i.e. memory address + rel base)

## Program

### VARIABLES
| Name        | Position |
|-------------|----------|
| INPUT       |   900    |
| WIDTH       |   901    |
| COUNTER     |   902    |
| IFVAL       |   903    |
| Y_POS       |   904    |
| X_POS       |   905    |
| CHECKVAL    |   906    |
| TOTAL       |   907    |
| NEGINPUT    |   908    |
| CUR_POS     |   909    |
| NEG_CUR_POS |   910    |
| TEMP_X_POS  |   911    |
| TEMP_Y_POS  |   912    |
| CHECK_X_POS |   913    |
| TEMP_NUM    |   914    |
| MULT        |   915    |
| DIGIT       |   916    |
| Y_ADD       |   917    |
| OFFSET      |   918    |

### Positions + 4 to all + x to all after start
| Name      | Position |
|-----------|----------|
| START     |   18     |
| OUTERLOOP |   41     |
| INNERLOOP |   49     |
| OUTERNUM  |   152    |
| INNERNUM  |   156    |
| SKIP      |   338    | 342
| OSKIP     |   226    |
| INNERPARSE|   279    |
| INNERREAD |   99     |
| READBREAK |   148    |
| FOUND     |   264    | 267 
| END       |   346    | 

### Plan
input grid
for y in grid
for x in grid

if on num loop around num and check for a symbol
if found add num to total
else skip after num

### Reading Input (Implemented)
(3 INPUT) - input length of input
(3 WIDTH) - input width of grid
(1101 0 0 TOTAL) - set total to 0
(109 1000) - Increment rel base to 1000
(102 -1 INPUT NEG_INPUT) - init neg input
(1101 0 0 COUNTER) - Set counter to 0
(Let this be position START)
(101 1 COUNTER COUNTER) - Increment counter
(203 0) - Add value at 1000 + counter
(109, 1) - Increment rel_base
(7 COUNTER INPUT IFVAL) - If counter less than input
(5 IFVAL START)  - jump if counter less than input
(9, -999) - reset rel_base
(9, NEG_INPUT) - reset rel_base

### Check through grid
(1101 0 -1 Y_POS) - set y to -1 (increment is at start)
(Let this be OUTERLOOP) - First for loop
(101 1 Y_POS Y_POS) - increment y
(1101 0 -1 X_POS) - set x to -1 (increment is at start)
(Let this be INNERLOOP) - Second for loop
(101 1 X_POS X_POS) - increment x

#### Check current is a number
(2 WIDTH Y_POS Y_ADD) - mult y by width
(1 Y_ADD X_POS CUR_POS) - Add x and y to get pos
(101 1000 CUR_POS CUR_POS) - add offset
(1002 CUR_POS -1 NEG_CUR_POS) - Get negative cur_pos
(9 CUR_POS) - Update rel_base
(1207 0 58 CHECKVAL) -- check if curnum less than 58
(9 NEG_CUR_POS) - Reset rel_base
(1006 CHECKVAL END) -- goto end if not less than
(9 CUR_POS) - Update rel_base
(2107 47 0 CHECKVAL) -- check if curnum larger than 47
(9 NEG_CUR_POS) - Reset rel_base
(1006 CHECKVAL END) -- goto end if not num

##### Read right to find end of number
(101 0 X_POS TEMP_X_POS) - init temp_x_pos to x_pos
(101 1 TEMP_X_POS TEMP_X_POS) - increment temp_x_pos
(Let this be INNERREAD)
(2 WIDTH Y_POS Y_ADD) - mult y by width
(1 Y_ADD TEMP_X_POS CUR_POS) - Add x and y to get pos
(101 1000 CUR_POS CUR_POS) - add offset
(1002 CUR_POS -1 NEG_CUR_POS) - Get negative cur_pos
(9 CUR_POS) - update rel_base
(1207 0 58 CHECKVAL) -- check if curnum less than 58
(9 NEG_CUR_POS) - Reset rel_base
(1006 CHECKVAL READBREAK) -- goto readbreak if not less than
(9 CUR_POS) - Update rel_base
(2107 47 0 CHECKVAL) -- check if curnum larger than 47
(9 NEG_CUR_POS) - Reset rel_base
(1006 CHECKVAL READBREAK) -- goto readbreak if not num
(101 1 TEMP_X_POS TEMP_X_POS) - increment temp_x_pos
(7 TEMP_X_POS WIDTH CHECKVAL) - check x_pos less than width
(1005 CHECKVAL INNERREAD) - if it is skip to beginning
(Let this be READBREAK)

##### Check whether symbols are surrounding number
(101 -1 X_POS CHECK_X_POS) - set checkx to x-1
(Let this be OUTERNUM)
(101 -1 Y_POS TEMP_Y_POS) - set tempy to y-1
(Let this be INNERNUM)
(2 WIDTH TEMP_Y_POS Y_ADD) - mult y by width
(1 Y_ADD CHECK_X_POS CUR_POS) - Add x and y to get pos
(101 1000 CUR_POS CUR_POS) - add offset
(1007 CUR_POS 1000 CHECKVAL) - check not below
(1005 CHECKVAL OSKIP)        - jump if is
(101 1000 INPUT OFFSET)      - check not above
(7 OFFSET CUR_POS CHECKVAL)  - jump if is
(1005 CHECKVAL OSKIP)
(1002 CUR_POS -1 NEG_CUR_POS) - Get negative cur_pos
(9 CUR_POS) - set rel_base
(2108 46 0 CHECKVAL) - Check whether current is "."
(9 NEG_CUR_POS) - reset rel base
(1005 CHECKVAL OSKIP) - Check whether "." and skip if is
(9 CUR_POS) - update rel_base
(1207 0 58 CHECKVAL) -- check if curnum less than 58
(9 NEG_CUR_POS) - Reset rel_base
(1006 CHECKVAL FOUND) -- goto oskip if not less than
(9 CUR_POS) - Update rel_base
(2107 47 0 CHECKVAL) -- check if curnum larger than 47
(9 NEG_CUR_POS) - Reset rel_base
(1005 CHECKVAL OSKIP) -- goto oskip if not num

(1005 900 FOUND)

(Let this be OSKIP)
(101 1 TEST_Y_POS TEST_Y_POS) - increment testy
(101 2 Y_POS Y_POS) - increment y
(7 TEST_Y_POS Y_POS CHECKVAL) - check testy < y + 2
(101 -2 Y_POS Y_POS) - decrement y
(1005 CHECKVAL INNERNUM)

(101 1 CHECK_X_POS CHECK_X_POS) -increment checkx
(101 1 TEMP_X_POS TEMP_X_POS) - increment tempx
(7 CHECK_X_POS TEMP_X_POS CHECKVAL) - check checkx < tempx +1
(101 -1 TEMP_X_POS TEMP_X_POS) - decrement tempx
(1005 CHECKVAL OUTERNUM)

##### Not got a symbol so skip past parsing
(jump to SKIP)

(Let this be FOUND)

##### Parsing
(1101 0 0 TEMP_NUM) - Set temp_num to 0
(1101 1 0 MULT) - Set mult to 1
(101 -1 TEMP_X_POS CHECK_X_POS) - set checkx to tempx -1
(Let this be INNERPARSE)
(2 WIDTH Y_POS Y_ADD) - get y row
(1 Y_ADD CHECK_X_POS CUR_POS) - add curpos
(101 1000 CUR_POS CUR_POS) - set curpos
(102 -1 CUR_POS NEG_CUR_POS) - set neg curpos
(9 CUR_POS) - set rel base
(21201 0 -48 0) - convert to num
(202 0 MULT DIGIT) - multiply checkx by multiplier
(21201 0 48 0) - unconvert
(9 NEG_CUR_POS) - reset rel base
(1 TEMP_NUM DIGIT TEMP_NUM) - add digit to tempnum
(1002 MULT 10 MULT) - multiply multiplier by 10
(101 -1 CHECK_X_POS CHECK_X_POS) - decrement checkx
(101 -1 X_POS X_POS) - decrement xpos
(7 X_POS CHECK_X_POS CHECKVAL) - check checkx > x - 1
(101 1 X_POS X_POS) - increment xpos
(105 CHECKVAL INNERPARSE) - loop if checkx > x - 1
(1 TOTAL TEMP_NUM TOTAL) - add num to total

##### Skip past found num
(Let this be SKIP)
(101 0 TEMP_X_POS X_POS)

(Let this be END)
(101 -1 WIDTH WIDTH) - 101,-1,901,901
(7 X_POS WIDTH CHECKVAL) - Check x < width
(101 1 WIDTH WIDTH) - 101,1,901,901
(1005 CHECKVAL INNERLOOP) - Jump to inner for if x < width
(101 -1 WIDTH WIDTH)
(7 Y_POS WIDTH CHECKVAL) - Check counter < size
(101 1 WIDTH WIDTH)
(1005 CHECKVAL OUTERLOOP) - Jump to outer if counter < size

(4 907) - Output total
(99) - Halt