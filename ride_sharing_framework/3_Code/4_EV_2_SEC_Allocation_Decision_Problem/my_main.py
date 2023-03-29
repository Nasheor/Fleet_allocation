# --------------------------------------------------------
#           PYTHON PROGRAM
# Here is where we are going to define our set of...
# - Imports
# - Global Variables
# - Functions
# ...to achieve the functionality required.
# When executing > python 'this_file'.py in a terminal,
# the Python interpreter will load our program,
# but it will execute nothing yet.
# --------------------------------------------------------

# ------------------------------------------
# IMPORTS
# ------------------------------------------
import sys
#
import generate_instance_sub_problems
import solve_all_sub_problems
# import mip


# ------------------------------------------
# FUNCTION 01 - my_main
# ------------------------------------------
def my_main(instance_folder,
            instance_analysis_folder,
            solution_folder,
            solution_analysis_folder,
            mip_time_limit,
            mip_input_file,
            mip_output_file
           ):

    # 1. We generate the sub_problems
    generate_instance_sub_problems.generate_sub_problems(instance_folder, instance_analysis_folder)

    # 2. We solve the sub_problems
    solve_all_sub_problems.solve_sub_problems(instance_analysis_folder,
                                              solution_analysis_folder,
                                              solution_folder
                                             )

    # 3. We compute the optimal configuration
    # mip.compute_best_EV_allocation(mip_input_file,
    #                                mip_output_file,
    #                                mip_time_limit
    #                               )


# ---------------------------------------------------------------
#           PYTHON EXECUTION
# This is the main entry point to the execution of our program.
# It provides a call to the 'main function' defined in our
# Python program, making the Python interpreter to trigger
# its execution.
# ---------------------------------------------------------------
if __name__ == '__main__':
    # 1. We read the instance content
    instance_folder = '../../2_Instances/Instance_to_solve/'
    instance_analysis_folder = '../../2_Instances/Analysis/'
    solution_folder = '../../4_Solutions/Instance_to_solve/'
    solution_analysis_folder = '../../4_Solutions/Analysis/'
    mip_time_limit = 60

    if (len(sys.argv) > 1):
        instance_folder = sys.argv[1]
        instance_analysis_folder = sys.argv[2]
        solution_folder = sys.argv[3]
        solution_analysis_folder = sys.argv[4]
        mip_time_limit = int(sys.argv[5])

    mip_input_file = solution_folder + "sub_problem_solutions.csv"
    mip_output_file = solution_folder + "optimal_EV_2_SEC_allocation.csv"

    # 2. We call to my_main
    my_main(instance_folder,
            instance_analysis_folder,
            solution_folder,
            solution_analysis_folder,
            mip_time_limit,
            mip_input_file,
            mip_output_file
           )

