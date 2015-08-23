"""
 * Program Name: Cellular Automaton
 * Created Date: September 13, 2014
 * Created By: William Grenard
 * Purpose: This program is designed to create a cellular Automaton. It creates a portable bitmap image based off of two command line inputs: the rule number and the number of iterations.
 * Acknowledgements:
"""

import sys      #importing sys allows access to command line inputs


def convert_to_binary(decimal_num):
    """
    *Input(s):      This function is designed to take one integer from 0-255 inclusive as input. This integer
                    should be a number represented in base 10 (decimal) form.
        
    *Output(s):     This function produces one string as output, which holds the binary form of the integer input.
        
    *Purpose:       This function returns an 8 bit binary string which is equivalent to the base 10 input integer. It is
                    important to note that this function only works for base 10 inputs from 0-255 inclusive
        
    *Tests:
    >>> convert_to_binary(0)
    '00000000'
    
    >>> convert_to_binary(30)
    '00011110'
    
    >>> convert_to_binary(150)
    '10010110'
    
    >>> convert_to_binary(255)
    '11111111'
    
    """
    
    binary_num = ""                 #defines and initializes variable to hold the binary form of the input
    
    #iterates through x-values from 7-0 to determine the value of each of the 8 bits in the binary string. First, the rightmost bit, which represents the place value 2^7 is determined. Then, the bit directly to the left, which represents 2^6, is determined. This process continues until the rightmost bit (2^0) is determined.
    for x in range(7, -1, -1):
        if 2**x > decimal_num:      #if the base 10 integer is less than the place value of the current bit (2^7 for x=7, 2^6 for x=6, and so on), then said bit should be assigned '0'
            binary_num += "0"       #0 is then added to the binary string
        else:
            binary_num += "1"       #if the base 10 integer is larger than or equal to the current bit's place value, then the bit should be assigned '1.' This is added to the string
            decimal_num -= 2**x     #subtract from the base 10 integer the portion that has already been converted to binary

    return binary_num               #return the resulting binary string, which is the input base 10 integer converted to binary



def convert_to_decimal(binary_string):
    """
    *Input(s):      This function is designed to take one string as input. This string should be a binary string to be converted to a decimal integer.
        
    *Output(s):     This function produces one integer as output, which is the binary string converted to a base 10 integer
        
    *Purpose:       This function converts a binary input to a base 10 integer, and returns this integer. Unlike the output string in the convert_to_binary function,
                    this input string is not limited to being 8-bits long.
                    
    *Tests:
    >>> convert_to_decimal('00000000')
    0
    
    >>> convert_to_decimal('00011011')
    27
    
    >>> convert_to_decimal('00111011')
    59
    
    >>> convert_to_decimal('11111111')
    255
    
    >>> convert_to_decimal('1110110101111')
    7599
    """

    decimal_num = 0                #defines and initializes variable to hold the base 10 form of the input
    index = 0                      #defines and initializes a counter variable to keep track of iterations through the following while loop

    #iterates through the binary input string from left to right adding the base 10 value of each bit to the decimal_num variable. (i.e. the first bit on the left, in base 10 is equal to (2^7) multiplied by 0 or 1, depending on which of those two is held there. The second bit is equal to (2^6) times 0 or 1. The final base 10 number is the sum of all of these values determined from each bit). By the end of the loop, decimal_num holds the converted integer.
    while index < len(binary_string):

        decimal_num += (2**index)*int(binary_string[len(binary_string) - 1 - index])    #multiplies the current bit's placevalue (2^7, 2^6, 2^5 . . .) by the current bit (0 or 1).

        index += 1                 #add one to the index

    return decimal_num             #once the loop is complete, return the integer which is the input binary string converted to base 10



def create_first_row(num_of_timesteps):
    """
    *Input(s):      This function takes the number of timesteps as an input. This is taken as the integer form of the first command line argument.
        
    *Output(s):     This function outputs a string of '0's with a single '1' directly in the center. The length of the string depends on the command line input that specifies the
                    number of time steps in the automaton.
        
    *Purpose:       This function produces the starting string for the cellular automaton. This string is the first row in the bitmap image created by this program, and it consists
                    of all zeroes, save for a single 1 directly in the center. The length of the string is equal to 2*n+1, where n is the number of timesteps, specified by the second
                    command line argument. Note that because the length is always 2*n+1, an odd number, a 1 can always be placed directly in the center of the string.
                    
    *Tests:
    >>> create_first_row(1)
    '010'
    
    >> create_first_row(3)
    '0001000'
    
    >>> create_first_row(5)
    '00000100000'
    
    >> create_first_row(10)
    '000000000010000000000'
    """

    row_length = 2*(num_of_timesteps) + 1    #initialize the length of the row to have 1 plus twice the amount of timesteps.
    row_one = ""                               #initialize the string to hold the first row
    
    #iterate once for each element that should be in the initial row. In the center of the row, place a '1'. Elsewhere, place '0's.
    for x in range(row_length):
        if x == (row_length - 1)/2:     #if the loop is halfway through the row's length, place a '1' in the row string
            row_one += "1"
        else:                           #if the loop is anywhere but halfway through the row's length, place a '0' in the row string.
            row_one += "0"

    return row_one                      #once the entire row string is constructed, return it



def determine_next_time_step(previous_row, rule_number):
    
    """
    *Input(s):      This function is designed to take as input the string that holds the row of '1's and '0's created in the previous timestep.
        
    *Output(s):     This function outputs the string of '1's and '0's corresponding to the next time step.
        
    *Purpose:       This function evaluates the previous row of the automaton, and uses the rule number specified by the first command line argument to determine what the next row
                    should be. For each character in the previous string it evaluates the character directly to the left and to the right to determine if each is a '1' or a '0'. The
                    character to the left of the first in the string, and the character to the right of the last in the string are both evaluated as '0'. The binary string produced by
                    the character to the left, the evaluated character itself, and the character to the right is converted to a base 10 number from 0-7. This number is then used as an
                    index, and the bit (0 or 1) of the rule number at that index is placed at the current position in the new string. Note, for indexing the rule number's bits are
                    labeled from left to right as (7, 6, 5, . . . 0).
                    
    *Tests:
    >>> determine_next_time_step('00100', '00011110')
    '01110'
    
    >>> determine_next_time_step('0010100', '1011010')
    '0100010'
    
    >>> determine_next_time_step('00010101000', '10110101101001')
    '11001010011'
    """

    new_row = ""                                            #initialize the string to hold the new row of the automaton
    input_string = ""                                       #initialize the string to hold the binary form of the input of the three consecutive characters
    index = 0                                               #initialize an index for the following while loop

    #loop through the entire length of the previous row, which is being evaluated, and for each character in the string determine the input created from the current character and its
    #two adjacent characters. Once this is done, compare this input to the rule number, and place the appropriate character in the new string.
    while index < len(previous_row):
        if index == 0:
            input_string = "0" + previous_row[index] + previous_row[index + 1]    #for the first character in the row, the input is '0', the current character, and the next character

        if index == len(previous_row) - 1:
            input_string = previous_row[index - 1] + previous_row[index] + "0"    #for the last character in the row, the input is the previous character, the current character, and '0'

        else:
            input_string = previous_row[index - 1] + previous_row[index] + previous_row[index + 1]  #for all other characters in the row, the input is the previous, current, and next characters
        
        input_decimal = convert_to_decimal(input_string)                #convert the three character input for the current row character to a decimal using the convert_to_decimal function
        new_row += rule_number[len(rule_number) - 1 - input_decimal]    #determine the value (0 or 1) of the rule number's character at the index specified by the input. Add this 0 or 1 to the new string

        index += 1      #increase the index so the process will begin again with the next character in the row

    return new_row      #return the entire new row once it is constructed

if __name__ == "__main__":
    import doctest
    doctest.testmod()


"""
    Start of program
"""
time_step = 1                                       #initialize a time step variable to keep track of the current time step
bitmap_width = 2*int(sys.argv[2]) + 1               #initialize the width of the bitmap file as 1 plus twice the number of timesteps
bitmap_height = int(sys.argv[2]) + 1                #initialize the height of the bitmap as 1 plus the number of timesteps
binary_rule = convert_to_binary(int(sys.argv[1]))   #convert the rule number input in the command line to binary and store as a string

eval_row = create_first_row(int(sys.argv[2]))       #use the create_first_row function to initialize the first row, a string with all '0's and a single '1' in the center

print("P1 " + str(bitmap_width) + " " + str(bitmap_height)) #print the first line of the bitmap file, which should give the length and width of the file as so: "P1 width length"
print(eval_row)                                     #print the row created above with the create_first_row() function

#each iteration through this loop creates the row for the next timestep using the determine_next_time_step function with the previous row as input. It then prints the row. This loop
#should iterate through all of the timesteps as specified by the first command line argument
while time_step <= int(sys.argv[2]):
    new_row = determine_next_time_step(eval_row, binary_rule)    #produce the next row to be displayed and store it in new_row. Use eval_row, which is the row from the previous time step, as the input row. And use the binary form of the rule number as the input rule.
    print(new_row)                                  #print new row
    eval_row = new_row                              #the new row should become the previous row for the next time step

    time_step += 1                                  #increase the timestep

"""
    End of program
"""
