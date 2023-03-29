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
import solve_TP_2_EV_allocation

# ------------------------------------------
# FUNCTION 01 - reactive_simulation
# ------------------------------------------
def solve_reactive_simulation(SECs,
                              EVs,
                              TPs
                             ):

    # 1. We create the output variable
    res = 0

    # 2. We get the ids of the TPs and EVs
    TP_IDs = sorted(TPs.keys())
    EV_IDs = sorted(EVs.keys())

    # 3. We traverse each trip, in order to allocate it
    for tp_id in TP_IDs:
        # 3.1. We traverse each vehicle, to try to allocate the trip to it
        for ev_id in EV_IDs:
            # 3.1.1. We setup the algorithm
            (my_EV_static_info, my_EV_schedule) = EVs[ev_id]
            max_passengers = my_EV_static_info[3]
            (my_TP_static_info, my_TP_SEC, my_TP_EV) = TPs[tp_id]
            (sec_x_location, sec_y_location) = SECs[my_EV_static_info[0]]

            # 3.1.2. We run the algorithm
            (is_allocated,
             pick_up_movement_index,
             drop_off_movement_index,
             return_to_sec_movement_index,
             extra_passenger_energy_and_delay_constraints_satisfied,
             my_new_EV_schedule
             ) = solve_TP_2_EV_allocation.ev_trip_allocation_attempt(my_EV_schedule,
                                                                     tp_id,
                                                                     my_TP_static_info,
                                                                     max_passengers,
                                                                     sec_x_location,
                                                                     sec_y_location
                                                                     )

            # 3.1.3. If the vehicle was allocated
            if (is_allocated == True):
                # I. We update the schedule of the EV
                EVs[ev_id][1] = my_new_EV_schedule

                # II. We update the info of TP_allocation
                TPs[tp_id][2] = ev_id

                # III. We increase the number of petitions satisfied
                res += 1

                # IV. We do not try to allocate it to any other EVs
                break

    # 4. We return res
    return res
