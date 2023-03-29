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
# FUNCTION 01 - get_info_from_file
# ------------------------------------------
def get_info_from_file(file_name):
    # 1. We create the output variable
    res = ()

    # 1.1. We output the min
    my_min = 0

    # 1.2. We output the max
    my_max = 0

    # 1.3. We output the median
    my_median = 0

    # 1.4. We output the mean
    my_mean = 0

    # 2. We open the file for reading
    my_input_stream = codecs.open(file_name, "r", encoding="utf-8")

    # 3. We parse the content of the file
    content = my_input_stream.readlines()
    content = [ line.strip().replace(",", ";").split(";") for line in content ]
    content = [ int(item[1]) for item in content ]
    content.sort()

    # 4. We close the file
    my_input_stream.close()

    # 5. We assign the values
    my_min = content[0]
    my_max = content[-1]

    size = len(content)

    my_median = content[size // 2]
    my_mean = sum(content) // size

    # 6. We assign res
    res = (my_min, my_max, my_median, my_mean)

    # 7. We return res
    return res


# ------------------------------------------
# FUNCTION 02 - my_main
# ------------------------------------------
def my_main(input_folder,
            output_folder,
            instance_names
           ):

    # 1. If the output folder exists, we remove it
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # 2. We open the files for writing
    output_streams = []
    size = len(instance_names)
    for name in instance_names:
        my_output_stream = codecs.open(output_folder + name, "w", encoding="utf-8")
        output_streams.append( my_output_stream )

    # 3. We add the header to the files
    my_str = "Factor;Min;Max;Median;Mean;\n"
    for index in range(size):
        output_streams[index].write(my_str)

    # 4. We get the list of folders we want to explore
    list_of_folders = os.listdir(input_folder)
    if (".DS_Store") in list_of_folders:
        list_of_folders.remove(".DS_Store")
    list_of_folders.remove("1_Raw_Analysis")
    list_of_folders.remove("2_Sorted_Order_Overall")
    list_of_folders.remove("4_per_factor_analysis")
    list_of_folders.sort()

    # 5. We traverse the different patterns in the list
    for folder_name in list_of_folders:
        # 5.1. We get the names of the files in order
        list_of_files = os.listdir(input_folder + folder_name)
        if (".DS_Store") in list_of_files:
            list_of_files.remove(".DS_Store")
        list_of_files.sort()

        # 5.2. We process their content
        index = 0
        for file in list_of_files:
            # 5.2.1. We get the info from the file
            (my_min, my_max, my_median, my_mean) = get_info_from_file(input_folder + folder_name + "/" + file)

            # 5.2.2. We add this info to output stream
            my_str = folder_name + ";" + str(my_min) + ";" + str(my_max) + ";" + str(my_median) + ";" + str(my_mean) + "\n"
            output_streams[index].write(my_str)

            # 5.2.3. We increase the index
            index += 1

    # 6. We close the files
    for index in range(size):
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
    input_folder = "../../4_Solutions/Num_TP_Satisfied/"
    output_folder = "../../4_Solutions/Num_TP_Satisfied/4_per_factor_analysis/"
    instance_names = [ "a_example.csv", "b_should_be_easy.csv", "c_no_hurry.csv", "d_metropolis.csv", "e_high_bonus.csv" ]

    # 2. We call to the function my_main
    my_main(input_folder,
            output_folder,
            instance_names
           )
