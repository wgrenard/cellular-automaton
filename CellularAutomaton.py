"""This program creates a cellular automaton, which can be viewed as a pbm file.

When this program is run, two command line arguments must be given, separated
by a space. The first specifies the rule number of the output. The second
specifies the number of timesteps the automaton uses to create the output.
The output is a printed 2 dimensional array of 0's and 1's. If this is saved
as a .pbm file, these 0's and 1's will be corresponded to white and black
cells, respectively.

Example:
    The following command line prompt will create a cellular automaton with
    20 rows, using rule number 57, and will store the result as a file
    named rule57.pbm.

    python CellularAutomaton.py 57 20 > rule57.pbm
"""

import sys

def convert_to_binary(decimal_num):
    """Convert the input base 10 integer to binary."""

    binary_num = ""

    for digit in range(7, -1, -1):
        if 2**digit > decimal_num:
            binary_num += "0"
        else:
            binary_num += "1"
            decimal_num -= 2**digit

    return binary_num



def convert_to_decimal(binary_string):
    """Convert the input binary string to a base 10 integer."""

    decimal_num = 0
    index = 0

    while index < len(binary_string):
        decimal_num += (2**index)*int(binary_string[len(binary_string) - 1 - index])
        index += 1

    return decimal_num


def create_first_row(num_of_timesteps):
    """Return the first row of the automaton in the form of a string.

    Arguments:
    num_of_timesteps -- The number of timesteps to be used in creation of the automaton.

    This function will produce a string of length 2*num_of_timesteps + 1. The
    string contains all 0's except for a single 1 in the center.

    Tests:
    >>> create_first_row(1)
    '010'

    >>> create_first_row(3)
    '0001000'

    >>> create_first_row(5)
    '00000100000'

    >>> create_first_row(10)
    '000000000010000000000'
    """

    row_length = 2*(num_of_timesteps) + 1
    row_one = ""

    # Iterate once for each element that should be in the initial row. In the
    # center of the row, place a '1'. Elsewhere, place '0's.
    for element in range(row_length):
        if element == (row_length - 1)/2:
            row_one += "1"
        else:
            row_one += "0"

    return row_one



def determine_next_time_step(previous_row, rule_number):
    """Produce the next row of the automaton from the previous row.

    Arguments:
    previous_row -- The last created row of the automaton as a String.
    rule_number -- The rule number being used for the current automaton.

    Here, the rule number, input by the user in the command line will be used
    to produce the next row of the automaton from the previous row.

    Tests:
    >>> determine_next_time_step('00100', '00011110')
    '01110'

    >>> determine_next_time_step('0010100', '1011010')
    '0100010'

    >>> determine_next_time_step('00010101000', '10110101101001')
    '11001010011'
    """

    new_row = ""
    input_string = ""   # This will hold the 3-bit binary label
    index = 0

    # Loop through the previous row, and for each character in the string
    # determine the input created from the current character and its two adjacent
    # characters. Compare this input to the rule number, and place the appropriate
    # character in the new string.
    while index < len(previous_row):
        if index == 0:
            input_string = "0" + previous_row[index] + previous_row[index + 1]

        if index == len(previous_row) - 1:
            input_string = previous_row[index - 1] + previous_row[index] + "0"

        else:
            input_string = previous_row[index - 1] + previous_row[index] + previous_row[index + 1]

        input_decimal = convert_to_decimal(input_string)
        new_row += rule_number[len(rule_number) - 1 - input_decimal]

        index += 1

    return new_row

if __name__ == "__main__":
    import doctest
    doctest.testmod()


TIME_STEP = 1
BITMAP_WIDTH = 2*int(sys.argv[2]) + 1
BITMAP_HEIGHT = int(sys.argv[2]) + 1
BINARY_RULE = convert_to_binary(int(sys.argv[1]))

EVAL_ROW = create_first_row(int(sys.argv[2]))

print "P1 " + str(BITMAP_WIDTH) + " " + str(BITMAP_HEIGHT)
print EVAL_ROW

while TIME_STEP <= int(sys.argv[2]):
    NEXT_ROW = determine_next_time_step(EVAL_ROW, BINARY_RULE)
    print NEXT_ROW
    EVAL_ROW = NEXT_ROW

    TIME_STEP += 1
