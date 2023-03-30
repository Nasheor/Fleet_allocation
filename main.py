import parse_in
import codecs
import Environment
import Community


if __name__ == '__main__':

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

    # Create the communities
    communities = []
    for i in community_numbers:
        community_id = i
        location = community_indices[i-1]
        vehicle_count, _ = community_vehicles_petitions[i-1]
        trips = community_trips[i]
        rebalancing_targets = {neighbor: 0 for neighbor in neighbors[community_id]}
        dispatch_targets = {neighbor: 0 for neighbor in neighbors[community_id]}
        community = Community(community_id, vehicle_count, trips, rebalancing_targets, dispatch_targets, data_logger)
        communities.append(community)