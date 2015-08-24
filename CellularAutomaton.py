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

    row_list = ['0']*num_of_timesteps + ['1'] + ['0']*num_of_timesteps
    row_string = ''.join(row_list)

    return row_string


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

    # Add a 0 to the beginning and end of the row because all elements outside
    # of the automaton should be 0's.
    extended_row = '0' + previous_row + '0'

    # Slice the extended row into three bit long binary strings
    bin_list = [extended_row[i-1:i+2] for i in range(1, len(extended_row)-1)]

    # For each binary string just created, convert to a decimal number. Retrieve
    # the corresponding digit in the rule number and add this to the new row.
    for bin_num in bin_list:
        dec_num = int(bin_num, 2)
        new_row += rule_number[len(rule_number) - dec_num - 1]

    return new_row

if __name__ == "__main__":
    import doctest
    doctest.testmod()


TIME_STEP = 1
BITMAP_WIDTH = 2*int(sys.argv[2]) + 1
BITMAP_HEIGHT = int(sys.argv[2]) + 1
BINARY_RULE = bin(int(sys.argv[1]))[2:]

FIRST_ROW = create_first_row(int(sys.argv[2]))

# Format the .pbm file by printing the first line in the form "P1 width height."
print "P1 " + str(BITMAP_WIDTH) + " " + str(BITMAP_HEIGHT)
print FIRST_ROW

# Create rows of the automaton
while TIME_STEP <= int(sys.argv[2]):
    NEXT_ROW = determine_next_time_step(FIRST_ROW, BINARY_RULE)
    print NEXT_ROW
    FIRST_ROW = NEXT_ROW

    TIME_STEP += 1
