"""This program creates a cellular automaton, which can be viewed as a pbm file.

The output is a printed 2 dimensional array of 0's and 1's, created based upon
the rule number and number of time steps entered by the user. If the output is
saved as a .pbm file, the 0's and 1's will be corresponded to white and black
cells, respectively, in the file.
"""

def obtain_user_input():
    """Return a tuple containing the rule number and number of timesteps.

    This function will obtain from the user the rule number and the number of
    timesteps to be used in the creation of the automaton. It will check that
    the input is valid, ensuring the rule number entered is an integer from
    0-255 and that the number of timesteps is a positive integer."""

    while True:
        try:
            rule_number = int(raw_input("Enter a rule number from 0-255: "))

            # If the input is outside of 0-255 then user needs to re-enter.
            if rule_number < 0 or rule_number > 255:
                raise ValueError()
            break

        except ValueError:
            print "Not a valid input."

    while True:
        try:
            num_of_timesteps = int(raw_input("Enter the number of timesteps to be used: "))

            # If the input is 0 or negative, then the user needs to re-enter.
            if num_of_timesteps <= 0:
                raise ValueError()
            break

        except ValueError:
            print "Not a valid input."

    return (rule_number, num_of_timesteps)


def create_first_row(num_of_timesteps):
    """Return the first row of the automaton in the form of a string.

    This function will produce a string of length 2*num_of_timesteps + 1. The
    string contains all 0's except for a single 1 in the center.

    Args:
        num_of_timesteps -- The number of timesteps to be used in creation of the automaton.

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

    Args:
        previous_row -- The last created row of the automaton as a String.
        rule_number -- The rule number being used for the current automaton.

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
    # the corresponding digit in the rule number and append this to the new row.
    for bin_num in bin_list:
        dec_num = int(bin_num, 2)
        new_row += rule_number[len(rule_number) - dec_num - 1]

    return new_row

def run_automaton():
    """Run the cellular automaton program."""

    time_step = 1
    (decimal_rule, num_of_timesteps) = obtain_user_input()
    bitmap_width = 2*num_of_timesteps + 1
    bitmap_height = num_of_timesteps + 1
    binary_rule = bin(decimal_rule)[2:]

    first_row = create_first_row(num_of_timesteps)

    # Format the .pbm file by printing the first line in the form "P1 width height."
    print "P1 " + str(bitmap_width) + " " + str(bitmap_height)
    print first_row

    # Create rows of the automaton
    while time_step <= num_of_timesteps:
        next_row = determine_next_time_step(first_row, binary_rule)
        print next_row
        first_row = next_row

        time_step += 1

if __name__ == "__main__":
    run_automaton()

