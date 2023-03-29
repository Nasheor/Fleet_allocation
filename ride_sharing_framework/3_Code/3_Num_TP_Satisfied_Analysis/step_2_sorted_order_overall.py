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
# FUNCTION 01 - sort_instance
# ------------------------------------------
def sort_instance(input_file, output_file):
    # 1. We open the files
    my_input_stream = codecs.open(input_file, "r", encoding="utf-8")
    my_output_stream = codecs.open(output_file, "w", encoding="utf-8")

    # 2. We read the file content
    content = my_input_stream.readlines()
    content = [ line.strip().replace(",", ";").split(";") for line in content ]
    content = [ ( int(item[1]), item[0] ) for item in content ]
    content.sort(reverse=True)

    for item in content:
        my_str = item[1] + ";" + str(item[0]) + "\n"
        my_output_stream.write(my_str)

    # 3. We close the files
    my_input_stream.close()
    my_output_stream.close()

# ------------------------------------------
# FUNCTION 02 - my_main
# ------------------------------------------
def my_main(input_folder, output_folder):

    # 1. If the output folder exists, we remove it
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # 2. We get the list of files to be solved in sorted order
    list_of_files = os.listdir(input_folder)
    if (".DS_Store") in list_of_files:
        list_of_files.remove(".DS_Store")
    list_of_files.sort()

    # 3. We traverse the list of files to sort them
    for file in list_of_files:
        # 4.1. We get the name of the input and output files
        input_file_name = input_folder + file
        output_file_name = output_folder + file

        # 4.2. We solve the instance
        sort_instance(input_file_name, output_file_name)

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
    input_folder = "../../4_Solutions/Num_TP_Satisfied/1_Raw_Analysis/"
    output_folder = "../../4_Solutions/Num_TP_Satisfied/2_Sorted_Order_Overall/"

    # 2. We call to the function my_main
    my_main(input_folder, output_folder)
