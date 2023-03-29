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

import step_1_get_file_per_instance_type
import step_2_sorted_order_overall
import step_3_sorted_order_by_pattern
import step_4_per_factor_analysis

# ------------------------------------------
# FUNCTION 01 - my_main
# ------------------------------------------
def my_main(input_file,
            instance_names,
            output_folder,
            step_1_output_folder,
            step_2_output_folder,
            step_4_output_folder,
            patterns_list
           ):

    # 1. If the output folder exists, we remove it
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # 2. We perform the step_1
    step_1_get_file_per_instance_type.my_main(input_file,
                                              instance_names,
                                              step_1_output_folder
                                             )

    # 3. We perform the step_2
    step_2_sorted_order_overall.my_main(step_1_output_folder, step_2_output_folder)

    # 4. We perform the step_3
    step_3_sorted_order_by_pattern.my_main(step_1_output_folder,
                                           output_folder,
                                           patterns_list
                                          )

    # 5. We perform the step_4
    step_4_per_factor_analysis.my_main(output_folder,
                                       step_4_output_folder,
                                       instance_names
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
    input_file = "../../4_Solutions/Analysis/solution.csv"
    instance_names = [ "a_example.csv", "b_should_be_easy.csv", "c_no_hurry.csv", "d_metropolis.csv", "e_high_bonus.csv" ]
    output_folder = "../../4_Solutions/Num_TP_Satisfied/"

    step_1_output_folder = output_folder + "1_Raw_Analysis/"
    step_2_output_folder = output_folder + "2_Sorted_Order_Overall/"
    step_4_output_folder = output_folder + "4_per_factor_analysis/"

    patterns_list = [ "TPs_2_",
                      "TPs_10_",
                      "TPs_25_",
                      "TPs_50_",
                      "Num_SECs_1_",
                      "Num_SECs_4_",
                      "Num_SECs_16_",
                      "START_",
                      "SPREAD_",
                      "Energy_Factor_05",
                      "Energy_Factor_10",
                      "Energy_Factor_20"
                    ]

    # 2. We call to the function my_main
    my_main(input_file,
            instance_names,
            output_folder,
            step_1_output_folder,
            step_2_output_folder,
            step_4_output_folder,
            patterns_list
           )
