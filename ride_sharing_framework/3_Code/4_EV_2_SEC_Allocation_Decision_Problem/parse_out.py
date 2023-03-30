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

import codecs

# ------------------------------------------
# FUNCTION 01 - parse_out
# ------------------------------------------
# Description:
# We write the instance_solution to a file
# ----------------------------------------------------
# Input Parameters:
# (1) output_file_name. => The name of the file to write our solution to.
# (2) num_trips_satisfied. => The number of trips satisfied.
# (3) EVs. => The info with the schedule of each EV.
# (4) TPs. => The info regarding each TP.
# ----------------------------------------------------
# Output Parameters:
# ----------------------------------------------------
def parse_out(output_file_name,
              num_trips_satisfied,
              EVs,
              TPs,
              TDs
             ):

    # 1. We open the file for writing
    my_output_stream = codecs.open(output_file_name, "w", encoding="utf-8")

    # 2. We get the ids of the TPs and EVs
    TP_IDs = sorted(TPs.keys())
    EV_IDs = sorted(EVs.keys())

    # 3. We compute the percentage of trips satisfied
    num_trips = len(TP_IDs)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)
    my_str = "TPs satisfied = " + str(num_trips_satisfied) + "; Total TPs = " + str(num_trips) + "; Percentage Satisfied + " + str(round(num_trips_satisfied / num_trips , 3) * 100) + "%\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    # 4. We compute the info per EV
    my_str = "\n-------------------------------------------------------------------------\n\n"
    my_output_stream.write(my_str)
    my_str = "EVs" + "\n\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    EV_D = {}
    EV_total_energy = 0

    for ev_id in EV_IDs:
        my_str = "--------------------------------------\n"
        my_output_stream.write(my_str)
        my_str = "EV" + str(ev_id) + "\n"
        my_output_stream.write(my_str)

        # 4.1. We compute the overall statistics
        TP_served_by_EV = {}
        num_TPs_served = 0
        my_EV_schedule = EVs[ ev_id ][1]
        total_energy = my_EV_schedule[0][8] - my_EV_schedule[-1][9]
        EV_total_energy += total_energy

        for item in my_EV_schedule:
            if ((item[10] != 0) and (item[10] != 1000000000)):
                if (abs(item[10]) not in TP_served_by_EV):
                    TP_served_by_EV[ abs(item[10]) ] = True
                    num_TPs_served += 1

        EV_D[ev_id] = total_energy

        my_str = "--------------------------------------\n"
        my_output_stream.write(my_str)
        my_str = "Num TPs served = " + str(num_TPs_served) + "\n"
        my_output_stream.write(my_str)
        my_str = "TPs served = " + " ".join([ str(x) for x in sorted(TP_served_by_EV.keys()) ]) + "\n"
        my_output_stream.write(my_str)
        my_str = "Total energy used = " + str(total_energy) + "\n"
        my_output_stream.write(my_str)
        my_str = "--------------------------------------\n"
        my_output_stream.write(my_str)

        # 4.2. We print the schedule
        my_str = "Schedule:\n"
        my_output_stream.write(my_str)
        for item in my_EV_schedule:
            my_str = " ".join([ str(x) for x in item ]) + "\n"
            my_output_stream.write(my_str)

        my_str = "--------------------------------------\n"
        my_output_stream.write(my_str)

    # 5. We compute the info per TP
    my_str = "\n-------------------------------------------------------------------------\n\n"
    my_output_stream.write(my_str)
    my_str = "TPs" + "\n\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    TP_total_energy = 0
    TP_not_covered_total_energy = 0

    for tp_id in TP_IDs:
        my_str = "\n----------------------\n"
        my_output_stream.write(my_str)
        allocated_to = TPs[tp_id][2]
        if (allocated_to == -1):
            my_str = "TP" + str(tp_id) + " not allocated\n"
            TP_not_covered_total_energy += TDs[tp_id]
        else:
            my_str = "TP" + str(tp_id) + " allocated to " + str(allocated_to) + "\n"
        TP_total_energy += TDs[tp_id]
        my_output_stream.write(my_str)
        my_str = "----------------------\n"
        my_output_stream.write(my_str)

    # 6. We compute the overall Ride-sharing vs. Individual num_vehicles and distance info
    my_str = "\n-------------------------------------------------------------------------\n\n"
    my_output_stream.write(my_str)
    my_str = "Ride-sharing vs Individual Mode - Num Vehicles and Distance Comparisson " + "\n\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    num_EV = len(EVs)
    individuals_not_covered = (num_trips - num_trips_satisfied)
    vehicles_diff = num_EV + individuals_not_covered

    my_str = "Individual Mode = " + str(num_trips) + " vehicles.\n"
    my_output_stream.write(my_str)
    my_str = "Ride-sharing Mode = " + str(vehicles_diff) + " vehicles. The " + str(num_EV) + " ride-sharing vehicles + " + str(individuals_not_covered) + " vehicles of the individuals not served by the ride-sharing service.\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    individual_mode_distance = TP_total_energy
    EV_total_distance = 0
    for ev_id in EV_D:
        EV_total_distance += EV_D[ev_id]
    EV_mode_total_distance = EV_total_distance + TP_not_covered_total_energy

    my_str = "Individual Mode = " + str(individual_mode_distance) + " distance.\n"
    my_output_stream.write(my_str)
    my_str = "Ride-sharing Mode = " + str(EV_mode_total_distance) + " distance. " + str(EV_total_distance) + " from the EV fleet + " + str(TP_not_covered_total_energy) + " from the distance of the trips not covered individuals had to do with their own vehicle.\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    # 7. We close the file
    my_output_stream.close()
    return EV_total_energy
