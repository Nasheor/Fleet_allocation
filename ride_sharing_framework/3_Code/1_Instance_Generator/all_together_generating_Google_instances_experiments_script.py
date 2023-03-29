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
import step_1_setup_Google_instances_City_TPs
import step_2_setup_Google_instances_City_SECs_EVs_TPs
#
import os

# ------------------------------------------
# FUNCTION 01 - my_main
# ------------------------------------------
def my_main(input_folder,
            step1_output_folder,
            range_tightness_flag_and_pick_up,
            range_num_SECs,
            range_EV_release_start_or_across,
            range_EV_2_TP_energy_factor
           ):

    # 1. We run the step1
    for item in range_tightness_flag_and_pick_up:
        step_1_setup_Google_instances_City_TPs.my_main(input_folder,
                                                       step1_output_folder,
                                                       item
                                                      )

    # 2. We collect the names of the folders being created
    list_of_folders = os.listdir(step1_output_folder)
    if (".DS_Store") in list_of_folders:
        list_of_folders.remove(".DS_Store")
    list_of_folders.sort()

    # 3. We run the step2 for each of these folders and configurations
    for intermediate_folder in list_of_folders:
        for value_num_SECs in range_num_SECs:
            for value_EV_release_start_or_across in range_EV_release_start_or_across:
                for value_EV_2_TP_energy_factor in range_EV_2_TP_energy_factor:
                    step_2_setup_Google_instances_City_SECs_EVs_TPs.my_main(step1_output_folder + intermediate_folder + "/",
                                                                            value_num_SECs,
                                                                            value_EV_release_start_or_across,
                                                                            value_EV_2_TP_energy_factor
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
    # input_folder = "../../2_Instances/Google_Hash_Code_2018/"
    # step1_output_folder = "../../2_Instances/Analysis/"

    input_folder = "../../2_Instances/Scalability/Google_Hash_Code_2018/"
    step1_output_folder = "../../2_Instances/Scalability/Analysis/"

    # 1.2. We get the tightness parameter range for both the trip flag and the pick-up intervals
    range_tightness_flag_and_pick_up = [ 2, 10, 25, 50 ]
    range_num_SECs = [ 1, 4, 16 ]
    range_EV_release_start_or_across = [ 0, 1 ]
    range_EV_2_TP_energy_factor = [ 0.5, 1.0, 2.0 ]

    # 2. We call to the function my_main
    my_main(input_folder,
            step1_output_folder,
            range_tightness_flag_and_pick_up,
            range_num_SECs,
            range_EV_release_start_or_across,
            range_EV_2_TP_energy_factor
           )
