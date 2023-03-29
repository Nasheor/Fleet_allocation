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

# ------------------------------------------
# FUNCTION 01 - parse_in
# ------------------------------------------
# Description:
# We read the instance_input from a file
# ----------------------------------------------------
# Input Parameters:
# (1) input_file_name. => The name of the file to read our instance from.
# (2) tightness_flag_and_pick_up. => The % of tightness for the TP pick_up and flag intervals.
# ----------------------------------------------------
# Output Parameters:
# (1) instance_input_object. => The 'instance_info object', represented as
# instance_info[0] -> grid_x_axis
# instance_info[1] -> grid_y_axis
# instance_info[2] -> time_horizon
# instance_info[3] -> num_EVs
# instance_info[4] -> num_TPs
# instance_info[5] -> total_distance
# instance_info[6] -> TPs
# ----------------------------------------------------
def parse_in(input_file_name, tightness_flag_and_pick_up):
    #  1. We create the output variable
    res = ()

    # 1.1. We output the x-axis dimension of the grid
    grid_x_axis = 0

    # 1.2. We output the y-axis dimension of the grid
    grid_y_axis = 0

    # 1.3. We output the time horizon
    time_horizon = 0

    # 1.4. We output the number of EVs
    num_EVs = 0

    # 1.5. We output the number of valid trips
    num_TPs = 0

    # 1.6. We output the total distance
    total_distance = 0

    # 1.7. We output the trip petitions
    TPs = []

    # 2. We open the file for reading
    my_input_stream = codecs.open(input_file_name, "r", encoding='utf-8')

    # 3. We read the first line
    (grid_x_axis, grid_y_axis, num_EVs, num_TPs, _, time_horizon) = tuple(map(int, my_input_stream.readline().strip().split(" ")))

    # 4. We get the information for the trips
    for _ in range(num_TPs):
        # 4.1. We read the trip info
        (SX, SY, TX, TY, EP, UB) = tuple(map(int, my_input_stream.readline().strip().split(" ")))

        # 4.2. We compute the trip distance
        trip_distance = 0 + abs(TX - SX) + abs(TY - SY)
        total_distance += trip_distance

        # 4.3. We compute the time window
        time_window = UB - EP

        # 4.4. We ensure that the trip is a valid one
        assert (SX >= 0)
        assert (SX < grid_x_axis)
        assert (SY >= 0)
        assert (SY < grid_y_axis)
        assert (TX >= 0)
        assert (TX < grid_x_axis)
        assert (TY >= 0)
        assert (TY < grid_y_axis)

        assert (EP >= 0)
        assert (EP <= time_horizon)
        assert (UB >= 0)
        assert (UB <= time_horizon)
        assert (EP < UB)

        assert (time_window >= trip_distance)

        # 4.5. We compute the LB or time the trip petition is launched / announced.
        LB = None
        if (tightness_flag_and_pick_up == -1):
            LB = random.randint(0, EP)
        else:
            value = int((EP * tightness_flag_and_pick_up * 1.0) / 100)
            LB = EP - value
            if (LB < 0):
                LB = 0
            if (LB > EP):
                LB = EP

        # 4.6. We compute the ED automatically, from the EP + trip distance
        ED = EP + trip_distance

        # 4.7. We compute the LP as any number among EP and ED
        LP = None
        if (tightness_flag_and_pick_up == -1):
            LP = random.randint(EP, ED - 1)
        else:
            max_value = (ED - 1) - EP
            value = int((max_value * tightness_flag_and_pick_up * 1.0) / 100)
            LP = EP + value
            if (LP < EP):
                LP = EP
            if (LP > ED - 1):
                LP = ED - 1
            UB = ED + value

        # 4.8. We generate the trip info
        trip_info = ( LB, SX, SY, TX, TY, EP, LP, ED, UB )

        # 4.9. We append it to the list
        TPs.append( trip_info )

    # 5. We sort the TPs by increasing order in the LB
    TPs.sort()

    # 6. We close the file
    my_input_stream.close()

    # 7. We assign and return res
    res = (grid_x_axis,
           grid_y_axis,
           time_horizon,
           num_EVs,
           num_TPs,
           total_distance,
           TPs
          )

    # 8. We return res
    return res

# ------------------------------------------
# FUNCTION 02 - parse_out
# ------------------------------------------
# Description:
# We write the instance_solution to a file
# ----------------------------------------------------
# Input Parameters:
# (1) output_file_name. => The name of the file to write our solution to.
# (2) instance_info. => The 'instance_info object', represented as
# instance_info[0] -> grid_x_axis
# instance_info[1] -> grid_y_axis
# instance_info[2] -> time_horizon
# instance_info[3] -> num_EVs
# instance_info[4] -> num_TPs
# instance_info[5] -> total_distance
# instance_info[6] -> TPs
# ----------------------------------------------------
# Output Parameters:
# ----------------------------------------------------
def parse_out(output_file_name, instance_info):
    # 1. We open the file for writing
    my_output_stream = codecs.open(output_file_name, "w", encoding="utf-8")

    # 2. We unpack all the info from instance_info
    grid_x_axis = instance_info[0]
    grid_y_axis = instance_info[1]
    time_horizon = instance_info[2]
    num_EVs = instance_info[3]
    num_TPs = instance_info[4]
    total_distance = instance_info[5]
    TPs = instance_info[6]

    # 3. We write the Simulation information section
    my_str = str(grid_x_axis) + " " + str(grid_y_axis) + " " + str(time_horizon) + "\n"
    my_output_stream.write(my_str)

    # 4. We hardcode the SEC information section
    my_str = str(1) + "\n"
    my_output_stream.write(my_str)
    my_str = str(1) + " " + str(0) + " " + str(0) + "\n"
    my_output_stream.write(my_str)

    # 5. We hardcode the EVs information section
    my_str = str(num_EVs) + "\n"
    my_output_stream.write(my_str)

    # 5.1. We hardcode the battery level, for it to be collectively the same as the energy required
    # EV_battery_energy = math.ceil(total_distance / num_EVs)
    EV_battery_energy = total_distance

    # 5.2. We traverse each EV
    for EV_id in range(1, num_EVs + 1):
        # 5.2.1. We print the first line for it
        my_str = str(EV_id) + " 1 0 " + str(EV_battery_energy) + " 5\n"
        my_output_stream.write(my_str)

        # 5.2.2. We hardcode an empty schedule for them
        my_str = "0\n"
        my_output_stream.write(my_str)

    # 6. We write the TPs information section

    # 6.1. We write the number of trip petitions
    my_str = str(num_TPs) + "\n"
    my_output_stream.write(my_str)

    # 6.2. We traverse the trip petitions
    for TP_id in range(1, num_TPs + 1):
        # 6.2.1. We print the information of the trip
        my_str = str(TP_id) + " 1 -1\n"
        my_output_stream.write(my_str)

        # 6.2.2. We print the trip info
        trip_info = TPs[TP_id - 1]
        my_str = ", ".join([str(x) for x in trip_info]) + "\n"
        my_output_stream.write(my_str)

    # 7. We close the file
    my_output_stream.close()

# ------------------------------------------
# FUNCTION 03 - parse_instance
# ------------------------------------------
def parse_instance(input_file_name,
                   output_file_name,
                   tightness_flag_and_pick_up
                   ):
    # 1. We parse the Google Hash Code instance in
    instance_info = parse_in(input_file_name, tightness_flag_and_pick_up)

    # 2. We adapt it to the format required
    parse_out(output_file_name, instance_info)

# ------------------------------------------
# FUNCTION 04 - my_main
# ------------------------------------------
def my_main(input_folder,
            output_folder,
            tightness_flag_and_pick_up
           ):

    # 1. We get the actual name of the output folder
    value_tightness_flag_and_pick_up = "Random"
    if (tightness_flag_and_pick_up != -1):
        value_tightness_flag_and_pick_up = str(tightness_flag_and_pick_up)
    output_folder = output_folder + "City_TPs_" + str(value_tightness_flag_and_pick_up) + "/"

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
                       tightness_flag_and_pick_up
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
    input_folder = "../../2_Instances/Google_Hash_Code_2018/"
    output_folder = "../../2_Instances/Analysis/"

    # 1.2. We get the tightness parameter for both the trip flag and the pick-up intervals
    tightness_flag_and_pick_up = 100

    if (len(sys.argv) > 1):
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        tightness_flag_and_pick_up = int(sys.argv[3])

    assert (tightness_flag_and_pick_up >= -1) and (tightness_flag_and_pick_up <= 100)

    # 2. We call to the function my_main
    my_main(input_folder,
            output_folder,
            tightness_flag_and_pick_up
           )
