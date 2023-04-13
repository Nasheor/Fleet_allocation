import parse_in
import codecs
from Q_Environment import TripsEnvironment, EnergyEnvironment
from Deep_Q_Environment import DeepTripsEnvironment, DeepEnergyEnvironment
from Ccmomarl_Environment import CCMOMARLEnvironment
from Community import Community
import os
import shutil

def parse_initial_data():

    # Read the Input file
    file = 'ride_sharing_framework/2_Instances/Instance_to_solve/d_metropolis.in'
    (city, SECs, EVs, TPs, TDs) = parse_in.parse_in(file)
    print(f"City Dimensions: {city[0]}X{city[1]}")
    # Getting the number of Vehicles and TPs for each SEC at the start of the simulation
    community_trips = {}
    for id in SECs.keys():
        v_count = 0
        t_count = 0
        community_trips[id] = []
        for e_id in EVs.keys():
            if EVs[e_id][0][0] == id:
                v_count += 1
        for t_id in TPs.keys():
            if TPs[t_id][1] == id:
                community_trips[id].append(t_id)
                t_count+=1
        SECs[id] = SECs[id] + (v_count, t_count,)
    print(f"SEC IDS: {list(SECs.keys())} ")

    # Computing the neighbors of of each community using Moore neighborhood method
    community_numbers = list(SECs.keys())
    community_indices = [(SECs[community_number][0], SECs[community_number][1])
                         for community_number in community_numbers]
    print(f"SEC Locations: {community_indices}")
    community_vehicles_petitions = [(SECs[community_number][2], SECs[community_number][3])
                         for community_number in community_numbers]
    print(f"SEC Vehicles and Petitions: {community_vehicles_petitions}")
    neighbors = {}
    # Loop over each community and define its neighbors as the community ahead and the immediate predecessor
    for i, community in enumerate(community_numbers):
        # Initialize a list to store the neighbors of the current community
        neighbors[community] = []

        # Add the immediate predecessor to the neighbors list if it exists
        if i > 0:
            neighbors[community].append(community_numbers[i - 1])

        # Add the community ahead to the neighbors list if it exists
        if i < len(community_numbers) - 1:
            neighbors[community].append(community_numbers[i + 1])
    print(f"Neighbors: {neighbors}")

    # Create the Commmumities
    communities = []
    for index in range(len(community_numbers)):
        id = community_numbers[index]
        x_loc, y_loc = community_indices[index]
        initial_vehicle_count, initial_trips = community_vehicles_petitions[index]
        community_neighbors = neighbors[index+1]
        action = 'serve'
        c = Community(id, x_loc, y_loc, initial_vehicle_count, initial_trips,
                                     community_neighbors)
        communities.append(c)

    # Reading the solutions file for getting the number of trips satisfied and energy consumed
    solutions_file = './ride_sharing_framework/4_Solutions/Instance_to_solve/sub_problem_solutions.csv'
    requests_satisfied_data = {}
    with codecs.open(solutions_file, "r", encoding='utf-8') as f:
        data = f.readlines()
        for line in data:
            path, trips_satisfied, energy_consumed = line.strip().split(';')
            requests_satisfied_data[path.split('/')[5].split('.')[0]] = (int(trips_satisfied), float(energy_consumed))

    num_evs = len(EVs.keys())
    return communities, num_evs, requests_satisfied_data, community_vehicles_petitions


if __name__ == '__main__':
    # Run the Q Environment
    communities, num_evs, requests_satisfied_data, community_vehicle_petitions = parse_initial_data()
    total_trips = 0
    total_energy = 0
    for item in community_vehicle_petitions:
        (ev, trips) = item
        total_trips += trips
        total_energy += (ev * 100)

    # episodes = [1, 5, 10, 15]
    # num_days = [5, 10, 15, 20]
    episodes = [5]
    num_days = [10]
    paths = ['./output/trips_environment/',
             './output/energy_environment/',
             './output/deep_trips_environment/',
             './output/deep_energy_environment/',
             './output/ccmomarl_environment']

    for path in paths:
        if os.path.exists(path):
            os.chmod(path, 0o777)
            shutil.rmtree(path)
        os.mkdir(path)

    print('Reached here')

    for episode in episodes:
        for num_day in num_days:
            file_name = str(episode)+'_episode_'+str(num_day)+'_days.txt'
            #
            # path = paths[0]+file_name
            # trips_env = TripsEnvironment(episode, num_day, communities, num_evs,
            #                              requests_satisfied_data, total_trips, total_energy)
            # trips_env.compute_initial_states_and_rewards()
            # trips_env.compute_initial_trips_satisfied()
            # trips_env.run()
            # trips_env.print_results(path)
            #
            # path = paths[1]+file_name
            # energy_env = EnergyEnvironment(episode, num_day, communities, num_evs,
            #                                requests_satisfied_data, total_trips, total_energy)
            # energy_env.compute_initial_states_and_rewards()
            # energy_env.compute_initial_trips_satisfied()
            # energy_env.run()
            # energy_env.print_results(path)
            #
            # path = paths[2]+file_name
            # state_size = len(communities) * 4
            # action_size = 2
            # deep_trips_env = DeepTripsEnvironment(episode, num_day, communities, num_evs,
            #                                       requests_satisfied_data,
            #                                       state_size, action_size)
            # deep_trips_env.run()
            # deep_trips_env.print_results(path)
            #
            # path = paths[3]+file_name
            # state_size = len(communities) * 4
            # action_size = 2
            # deep_energy_env = DeepEnergyEnvironment(episode, num_day, communities, num_evs,
            #                                       requests_satisfied_data,
            #                                       state_size, action_size)
            # deep_energy_env.run()
            # deep_energy_env.print_results(path)

            path = path[4]+file_name
            ccmomarl_env = CCMOMARLEnvironment(episode, num_day, communities, num_evs,
                                           requests_satisfied_data, total_trips, total_energy, path)
            ccmomarl_env.run()




