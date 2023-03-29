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
import docplex.mp.model
import codecs

# -----------------------------------------------
# FUNCTION 01 - get_num_SECs_num_EVs_and_ub_TPs
# -----------------------------------------------
def get_num_SECs_num_EVs_and_ub_TPs(input_instance):
    # 1. We create the output variable
    res = ()

    # 1.1. We output the num_SECs
    num_SECs = 0

    # 1.2. We output the num_EVs
    num_EVs = 0

    # 1.3. We output the ub_TPs
    ub_TPs = 0

    # 2. We open the file for reading
    my_input_stream = codecs.open(input_instance, "r", encoding="utf-8")

    # 3. We keep track of the current SEC_val
    current_SEC_val = -1
    current_best_val = 0

    # 3. We traverse the file
    for line in my_input_stream:
        # 3.1. We get the info from the line
        content = (line.strip().split("/")[-1]).split("_num_EVs_")
        SEC_val = int(content[0].split("_")[1])
        EV_val = int(content[1].split(".")[0])
        new_TP_val = int(content[1].split(";")[1])

        if (SEC_val == 10):
            x = 2

        # 3.2. If the new SEC_val is different from current_SEC_val
        if (SEC_val != current_SEC_val):
            # 3.2.1. We update current_SEC_val
            current_SEC_val = SEC_val

            # 3.2.2. We update ub_TPs
            ub_TPs += current_best_val

            # 3.2.2. We re-start current_best_val
            current_best_val = 0

        # 3.3. If the number of TPs improves the best one, we update it
        if (new_TP_val > current_best_val):
            current_best_val = new_TP_val

        # 3.4. We update num_SECs and num_EVs
        if (SEC_val > num_SECs):
            num_SECs = SEC_val
        if (EV_val > num_EVs):
            num_EVs = EV_val

    # 4. We close the file
    my_input_stream.close()

    # 5. We assign res
    res = (num_SECs,
           num_EVs,
           ub_TPs
          )

    # 6. We return res
    return res


# ------------------------------------------
# FUNCTION 02 - get_array_values
# ------------------------------------------
def get_array_values(input_instance,
                     num_SECs,
                     num_EVs
                    ):

    # 1. We create the output variable
    res = [0] * (num_SECs * (num_EVs + 1))

    # 2. We open the file for reading
    my_input_stream = codecs.open(input_instance, "r", encoding="utf-8")

    # 3. We traverse the file
    for line in my_input_stream:
        # 3.1. We get the info from the line
        content = (line.strip().split("/")[-1]).split("_num_EVs_")
        SEC_val = int(content[0].split("_")[1])
        EV_val = int(content[1].split(".")[0])
        num_TPs_satisfied = int(content[1].split(";")[1])

        # 3.2. We populate the index of res
        res[ ((SEC_val - 1) * (num_EVs + 1)) + EV_val ] = num_TPs_satisfied

    # 4. We close the file
    my_input_stream.close()

    # 5. We return res
    return res


# ------------------------------------------
# FUNCTION 03 - parse_input_file
# ------------------------------------------
def parse_input_file(input_instance):
    # 1. We create the output variable
    res = ()

    # 1.1. We output the num_SECs
    num_SECs = 0

    # 1.2. We output the num_EVs
    num_EVs = 0

    # 1.3. We output the ub_TPs
    ub_TPs = 0

    # 1.4. We output the array of values
    array_values = None

    # 2. We read the file for getting the number of SECs and EVs
    (num_SECs,
     num_EVs,
     ub_TPs
    ) = get_num_SECs_num_EVs_and_ub_TPs(input_instance)

    # 3. We get the array of values
    array_values = get_array_values(input_instance,
                                    num_SECs,
                                    num_EVs
                                   )

    # 4. We assign res
    res = (num_SECs,
           num_EVs,
           ub_TPs,
           array_values
          )

    # 5. We return res
    return res


# ------------------------------------------
# FUNCTION 04 - solve_mip
# ------------------------------------------
def solve_mip(ub_TPs,
              num_SECs,
              num_EVs,
              array_values,
              time_limit
             ):

    # -----------------------
    # 1. OUTPUT VARIABLES
    # -----------------------

    # 1. We create the output variables
    res = ()

    # 1.1. We output the search status
    succeed = -1

    # 1.2. We output the amount of TPs satisfied
    best_value = -1

    # 1.3. We output the amount of vehicles per SEC
    EV_per_SEC = [0] * num_SECs


    # -----------------------
    # 2. MODEL CREATION
    # -----------------------

    # 1. We create the model
    mdl = docplex.mp.model.Model(name='EV_2_SEC_allocation')

    # -----------------------
    # 3. DECISION VARIABLES
    # -----------------------

    # 1. We create a list of boolean variables, specifying if each SEC_i picks or not an specific number of vehicles j
    my_vars = mdl.binary_var_list(num_SECs * (num_EVs + 1), name="my_vars")

    # 2. We create an integer variable, specifying the total number of trips satisfied
    my_opt_var = mdl.integer_var(lb=0, ub=ub_TPs, name="my_opt_var")

    # -----------------------
    # 4. CONSTRAINTS
    # -----------------------

    # 1. We add the constraint ensuring all EVs are allocated to the SECs
    amount_of_EVs = [ index % (num_EVs + 1)  for index in range(num_SECs * (num_EVs + 1)) ]
    mdl.add_constraint(mdl.sum(my_vars[i] * amount_of_EVs[i] for i in range(num_SECs * (num_EVs + 1))) == num_EVs)

    # 2. We add the constraint ensuring each SEC is allocated a given amount of EVs
    for SEC_index in range(num_SECs):
        mdl.add_constraint(mdl.sum(my_vars[i] for i in range(SEC_index * (num_EVs + 1), (SEC_index + 1) * (num_EVs + 1))) == 1)

    # 3. We add the constraint for defining the optimisation function
    mdl.add_constraint(my_opt_var == mdl.sum(my_vars[i] * array_values[i] for i in range(num_SECs * (num_EVs + 1))))


    # ----------------------------
    # 5. OPTIMISATION FUNCTION
    # ----------------------------

    # 1. We maximise the cost of my_opt_var
    mdl.maximize(my_opt_var)

    # ----------------------------
    # 6. SOLVE
    # ----------------------------

    # 1. We try to solve the problem
    mdl.set_time_limit(time_limit)
    if (mdl.solve()):
        # 1.1. We update succeed
        succeed = 0
        if (mdl.solve_details.gap == 0.0):
            succeed = 1

        # 2.2. We update best_value
        best_value = int(my_opt_var.solution_value)

        # 2.3. We update EV_per_SEC
        for SEC_index in range(num_SECs):
            value = 0
            for index in range(SEC_index * (num_EVs + 1), (SEC_index + 1) * (num_EVs + 1)):
                if (my_vars[index].solution_value == 0):
                    value += 1
                else:
                    break
            EV_per_SEC[SEC_index] = value

    # ----------------------------
    # 8. ASSIGN OUTPUT VARIABLES
    # ----------------------------

    # 1. We assign res
    res = (succeed,
           best_value,
           EV_per_SEC
          )

    # 2. We return res
    return res


# ------------------------------------------
# FUNCTION 05 - parse_out_solution
# ------------------------------------------
def parse_out_solution(output_file,
                       best_value,
                       EV_per_SEC,
                       array_values,
                       num_SECs,
                       num_EVs,
                      ):

    # 1. We open the file for writing
    my_output_stream = codecs.open(output_file, "w", encoding="utf-8")

    # 2. We write the optimal number of trips
    my_str = "Total_SECs_" + str(num_SECs) + ";Total_EVs_" + str(num_EVs) + "_Total_TPs_" + str(best_value) + "\n"
    my_output_stream.write(my_str)

    # 3. We traverse the SECs
    for SEC_val in range(num_SECs):
        # 3.1. We write the number of EVs allocated and the number of TPs satisfied
        my_str = "SEC_" + str(SEC_val + 1) + ";EVs_" + str(EV_per_SEC[SEC_val]) + "_TPs_" + str(array_values[ (SEC_val * (num_EVs + 1)) + EV_per_SEC[SEC_val] ]) + "\n"
        my_output_stream.write(my_str)

    # 4. We close the file
    my_output_stream.close()


# ------------------------------------------
# FUNCTION 06 - compute_best_EV_allocation
# ------------------------------------------
def compute_best_EV_allocation(input_file,
                               output_file,
                               time_limit
                              ):

    # 1. We parse the file
    (num_SECs,
     num_EVs,
     ub_TPs,
     array_values
     ) = parse_input_file(input_file)

    # 2. We try to improve the solution using MIP
    succeed = -1

    # 2.1. We run our algorithm
    (succeed,
     best_value,
     EV_per_SEC
     ) = solve_mip(ub_TPs,
                   num_SECs,
                   num_EVs,
                   array_values,
                   time_limit
                  )

    # 2.2. If we found a new solution, we update the result
    if (succeed >= 0):
        parse_out_solution(output_file,
                           best_value,
                           EV_per_SEC,
                           array_values,
                           num_SECs,
                           num_EVs,
                           )


# --------------------------------------------------------
#
# PYTHON PROGRAM EXECUTION
#
# Once our computer has finished processing the PYTHON PROGRAM DEFINITION section its knowledge is set.
# Now it is time to apply this knowledge.
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
    input_file = "../../4_Solutions/Instance_to_solve/sub_problem_solutions.csv"
    output_file = "../../4_Solutions/Instance_to_solve/optimal_EV_2_SEC_allocation.csv"
    time_limit = 60

    if (len(sys.argv) > 1):
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        time_limit = int(sys.argv[3])

    # 2. We call to the function my_main
    compute_best_EV_allocation(input_file,
                               output_file,
                               time_limit
                              )

