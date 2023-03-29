# --------------------------------------------------------
#
# PYTHON PROGRAM DEFINITION
#
# The knowledge a computer has of Python can be specified in 3 levels:
# (1) Prelude knowledge --> The computer has it by default.
# (2) Borrowed knowledge --> The computer gets this knowledge from 3rd party libraries defined by others
#                            (but imported by us in this program).
# (3) Generated knowledge --> The computer gets this knowledge from the new functions defined by us in this program.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer first processes this PYTHON PROGRAM DEFINITION section of the file.
# On it, our computer enhances its Python knowledge from levels (2) and (3) with the imports and new functions
# defined in the program. However, it still does not execute anything.
#
# --------------------------------------------------------

# ------------------------------------------
# IMPORTS
# ------------------------------------------
import time
import codecs
import random
import math
import os
import shutil
import sys
import math

# ------------------------------------------
# FUNCTION 01 - my_main
# ------------------------------------------
def my_main(input_file,
            output_file,
            factor
           ):

    # 1. We open the files
    my_input_stream = codecs.open(input_file, "r", encoding='utf-8')
    my_output_stream = codecs.open(output_file, "w", encoding='utf-8')

    # 2. We process the first line
    line = my_input_stream.readline()
    content = list(map(int, line.strip().split(" ")))
    content[2] = int(content[2]) // factor
    content[3] = int(content[3]) // factor
    content = [ str(x) for x in content ]
    my_str = " ".join(content) + "\n"
    my_output_stream.write(my_str)

    # 3. We process the rest of the content
    index = 0
    for line in my_input_stream:
        if (index == 0):
            my_output_stream.write(line)
        index += 1
        if (index == factor):
            index = 0

    # 4. We close the files
    my_input_stream.close()
    my_output_stream.close()


# --------------------------------------------------------
#
# PYTHON PROGRAM EXECUTION
#
# Once our computer has finished processing the PYTHON PROGRAM DEFINITION section its knowledge is set.
# Now its time to apply this knowledge.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer finally processes this PYTHON PROGRAM EXECUTION section, which:
# (i) Specifies the function F to be executed.
# (ii) Define any input parameter such this function F has to be called with.
#
# --------------------------------------------------------
if __name__ == '__main__':
    # 1. We get the input parameters
    factor = 10
    input_file = "./START_100_SEC_1_ENERGY_6_EV-FACTOR_2152_EV_20_FLEX_10000_TPS.txt"
    output_file = "./START_100_SEC_1_ENERGY_6_EV-FACTOR_2152_EV_20_FLEX_10000_TPS" + str(factor) + ".txt"

    my_main(input_file,
            output_file,
            factor
           )



