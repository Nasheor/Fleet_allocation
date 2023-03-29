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
# FUNCTION 01 - get_output_folder_name
# ------------------------------------------
def get_output_folder_name(input_folder,
                           num_SECs,
                           EV_release_start_or_across,
                           EV_2_TP_energy_factor
                          ):

    # 1. We create the output variable
    res = input_folder[:-1]

    # 2. We append the number of SECs
    res = res + "_Num_SECs_" + str(num_SECs) + "_"

    # 3. We append the release time of EVs
    res = res + "EV_Release_"
    if (EV_release_start_or_across == 0):
        res = res + "START_"
    else:
        res = res + "SPREAD_"

    # 4. We append the energy factor
    new_EV_2_TP_energy_factor = str(EV_2_TP_energy_factor)
    new_EV_2_TP_energy_factor = new_EV_2_TP_energy_factor.replace(".", "")

    res = res + "EV_2_TP_Energy_Factor_" + new_EV_2_TP_energy_factor + "/"

    # 5. We return res
    return res

# ------------------------------------------
# FUNCTION 02 - get_SECs_positions
# ------------------------------------------
def get_SECs_positions(n,
                       x_lb,
                       x_ub,
                       y_lb,
                       y_ub
                      ):

    # 1. We create the output variable
    res = []

    # 2. We ensure that n > 0
    assert (n > 0)

    # 3. Base case
    if (n == 1):
        # 3.1. We compute the middle point
        new_x_pos = ((x_ub - x_lb) // 2) + x_lb
        new_y_pos = ((y_ub - y_lb) // 2) + y_lb
        new_location = (new_x_pos, new_y_pos)

        # 3.2. We add it to the result
        res.append( new_location )

    # 4. Recursive case
    else:
        # 4.1. We divide the matrix into 4 sub-squares
        x_half = ((x_ub - x_lb) // 2) + x_lb
        y_half = ((y_ub - y_lb) // 2) + y_lb
        new_n = n // 4

        # 4.2. We call recursively for each of these 4 squares
        res_1 = get_SECs_positions(new_n,
                                   x_lb,
                                   x_half,
                                   y_lb,
                                   y_half
                                  )

        res_2 = get_SECs_positions(new_n,
                                   x_lb,
                                   x_half,
                                   y_half + 1,
                                   y_ub
                                  )

        res_3 = get_SECs_positions(new_n,
                                   x_half + 1,
                                   x_ub,
                                   y_lb,
                                   y_half
                                   )

        res_4 = get_SECs_positions(new_n,
                                   x_half + 1,
                                   x_ub,
                                   y_half + 1,
                                   y_ub
                                   )

        res = res_1 + res_2 + res_3 + res_4

    # 5. We return res
    return res

# ------------------------------------------
# FUNCTION 03 - parse_instance
# ------------------------------------------
def parse_instance(input_file_name,
                   output_file_name,
                   num_SECs,
                   EV_release_start_or_across,
                   EV_2_TP_energy_factor
                  ):

    # 1. We open the files for reading and writing
    my_input_stream = codecs.open(input_file_name, "r", encoding="utf-8")
    my_output_stream = codecs.open(output_file_name, "w", encoding="utf-8")

    # 2. We copy the City section as it is
    line = my_input_stream.readline()
    (grid_x_axis, grid_y_axis, time_horizon) = tuple(map(int,line.strip().split(" ")))
    my_output_stream.write(line)

    # 3. We consume the two lines of the SEC
    my_input_stream.readline()
    my_input_stream.readline()

    # 4. We compute the positions of the SECs
    SEC_positions = get_SECs_positions(num_SECs,
                                       0,
                                       grid_x_axis,
                                       0,
                                       grid_y_axis
                                      )

    # 5. We write the number of SECs
    my_str = str(num_SECs) + "\n"
    my_output_stream.write(my_str)

    # 6. We write all SECs
    for SEC_id in range(1, num_SECs + 1):
        (x_pos, y_pos) = SEC_positions[SEC_id - 1]
        my_str = str(SEC_id) + " " + str(x_pos) + " " + str(y_pos) + "\n"
        my_output_stream.write(my_str)

    # 7. We read and write the number of EVs
    num_EVs = int(my_input_stream.readline().strip())
    my_str = str(num_EVs) + "\n"
    my_output_stream.write(my_str)

    # 8. We create auxiliary values for the EV values
    total_energy = -1
    EV_energy = -1

    # 9. We create the EV release intervals
    EVs_per_SEC = math.ceil(num_EVs / num_SECs)
    if (EVs_per_SEC == 0):
        EVs_per_SEC = 1

    EV_release_interval = time_horizon // EVs_per_SEC
    release_intervals = [(index * EV_release_interval) for index in range(EVs_per_SEC + 1)]

    # 10. We read the info for each EV
    for iteration in range(num_EVs):
        # 10.1. We read the info from the EV
        (EV_id, SEC_id, release_time, total_energy, max_passengers) = tuple(map(int, my_input_stream.readline().strip().split(" ")))
        my_input_stream.readline()

        # 10.2. We create the auxiliary variables for the values of the EVs
        SEC_id = (iteration % num_SECs) + 1
        EV_energy = math.ceil(int(total_energy * EV_2_TP_energy_factor) / num_EVs)

        # 10.3. If the release is spread across the time horizon, we update the release time
        if (EV_release_start_or_across == 1):
            release_time = release_intervals[ iteration // num_SECs ]

        # 10.4. We write the info of the EV
        my_str = str(EV_id) + " " +  str(SEC_id) + " " + str(release_time) + " " + str(EV_energy) + " " + str(max_passengers) + "\n"
        my_output_stream.write(my_str)
        my_str = "0\n"
        my_output_stream.write(my_str)

    # 11. We read and write the number of TPs
    num_TPs = int(my_input_stream.readline().strip())
    my_str = str(num_TPs) + "\n"
    my_output_stream.write(my_str)

    # 12. We read the info for each EV
    for iteration in range(num_TPs):
        # 12.1. We read the info from the TP
        (TP_id, SEC_id, EV_id) = tuple(map(int, my_input_stream.readline().strip().split(" ")))
        SEC_id = (iteration % num_SECs) + 1
        my_str = str(TP_id) + " " + str(SEC_id) + " " + str(EV_id) + "\n"
        my_output_stream.write(my_str)

        # 12.2. We read and write the second line of the TP as it is
        line = my_input_stream.readline()
        my_output_stream.write(line)

    # 13. We close the files
    my_input_stream.close()
    my_output_stream.close()

# ------------------------------------------
# FUNCTION 04 - my_main
# ------------------------------------------
def my_main(input_folder,
            num_SECs,
            EV_release_start_or_across,
            EV_2_TP_energy_factor
           ):

    # 1. We get the actual name of the output folder
    output_folder = get_output_folder_name(input_folder,
                                           num_SECs,
                                           EV_release_start_or_across,
                                           EV_2_TP_energy_factor
                                          )

    # 2. If the output folder exists, we remove it
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # 3. We get the list of files to be solved in sorted order
    list_of_files = os.listdir(input_folder)
    if (".DS_Store") in list_of_files:
        list_of_files.remove(".DS_Store")
    list_of_files.sort()

    # 4. We traverse the list of files to solve them
    for file in list_of_files:
        # 4.1. We get the name of the input and output files
        input_file_name = input_folder + file
        output_file_name = output_folder + file

        # 4.2. We solve the instance
        parse_instance(input_file_name,
                       output_file_name,
                       num_SECs,
                       EV_release_start_or_across,
                       EV_2_TP_energy_factor
                      )

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

    # 1.1. We get the name of the input and output folder
    input_folder = "../../2_Instances/City_TPs_20/"

    # 1.2. We get the tightness parameter for both the trip flag and the pick-up intervals
    num_SECs = 4
    EV_release_start_or_across = 1
    EV_2_TP_energy_factor = 2.0

    if (len(sys.argv) > 1):
        input_folder = sys.argv[1]
        num_SECs = int(sys.argv[2])
        EV_release_start_or_across = int(sys.argv[3])
        EV_2_TP_energy_factor = float(sys.argv[4])

    assert (num_SECs > 0) and ((num_SECs % 4) == 0)
    assert (EV_release_start_or_across == 0) or (EV_release_start_or_across == 1)
    assert (EV_2_TP_energy_factor > 0.0)

    # 2. We call to the function my_main
    my_main(input_folder,
            num_SECs,
            EV_release_start_or_across,
            EV_2_TP_energy_factor
           )

