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
import codecs
import os
import shutil

# ------------------------------------------
# FUNCTION 01 - my_main
# ------------------------------------------
def my_main(input_file,
            instance_names,
            output_folder
           ):

    # 1. We open the file for reading
    my_input_stream = codecs.open(input_file, "r", encoding="utf-8")

    # 2. If the output folder exists, we remove it
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # 3. We open the files for writing
    output_streams = []
    for name in instance_names:
        my_output_stream = codecs.open(output_folder + name, "w", encoding="utf-8")
        output_streams.append( my_output_stream )

    # 4. We read the file
    index = 0
    num_files = len(instance_names)

    for line in my_input_stream:
        output_streams[ index % num_files ].write(line[32:])
        index += 1

    # 5. We close the files
    my_input_stream.close()
    for index in range(num_files):
        output_streams[index].close()

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
    input_file = "../../4_Solutions/Analysis/solution.csv"
    instance_names = [ "a_example.csv", "b_should_be_easy.csv", "c_no_hurry.csv", "d_metropolis.csv", "e_high_bonus.csv" ]
    output_folder = "../../4_Solutions/Num_TP_Satisfied/1_Raw_Analysis/"

    # 2. We call to the function my_main
    my_main(input_file,
            instance_names,
            output_folder
           )
