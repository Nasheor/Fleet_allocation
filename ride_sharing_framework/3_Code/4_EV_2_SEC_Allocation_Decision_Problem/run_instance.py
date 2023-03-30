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
import parse_in
import solve
import parse_out
#
import sys
import time


# ------------------------------------------
# FUNCTION 01 - my_main
# ------------------------------------------
def my_main(input_file_name, output_file_name):
    # 1. We create the output variable
    res = 0

    # 2. We parse the instance in
    (city, SECs, EVs, TPs, TDs) = parse_in.parse_in(input_file_name)

    #

    # 3. We run the reactive simulation
    res = solve.solve_reactive_simulation(SECs,
                                          EVs,
                                          TPs
                                         )

    # 4. We parse the instance out
    total_energy = parse_out.parse_out(output_file_name,
                        res,
                        EVs,
                        TPs,
                        TDs
                       )

    # 5. We return res
    return res, total_energy


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
    # 1. We get the name of the input and output folder
    # input_file = "../../2_Instances/b_should_be_easy.txt"
    # output_file = "../../4_Solutions/b_should_be_easy.txt"

    input_file = "./b_should_be_easy.in"
    output_file = "./b_should_be_easy.out"

    if (len(sys.argv) > 1):
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    # 2. We call to the function my_main
    start_time = time.time()

    my_main(input_file, output_file)

    total_time = time.time() - start_time
    print("Total time = " + str(total_time))
