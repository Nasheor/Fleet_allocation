import numpy as np
from agents import Community
from Environment import Grid

class Environment:
    def __init__(self, grid, num_time_steps, neighbors, community_trips):
        self.grid = grid
        self.num_time_steps = num_time_steps
        self.current_time_step = 0
        self.neighbor_map = neighbors
        self.community_trips = community_trips

    def step(self):
        # Generate trip requests
        trip_requests = self.community_trips

        # Loop over each community and update its state
        for community_id, community in self.grid.communities.items():
            # Get the community's state vector
            state_vector = self._get_state_vector(community, trip_requests[community_id])

            # Use the community's policy to select an action
            action = community.select_action(state_vector)

            # Execute the action
            if action == 'serve':
                community.serve_requests(trip_requests)
            elif action == 'rebalance':
                neighbor = community.select_dispatch_target()
                community.rebalance_to(neighbor)

        # Compute rewards for each community
        for community in self.grid.communities.values():
            self._compute_reward(community)

        # Update the current time step
        self.current_time_step += 1

        # Check if the simulation is done
        done = self.done()

        return state_vector, community.reward, done

    def reset(self):
        self.current_time_step = 0
        for community in self.grid.communities.values():
            community.reset()

    def done(self):
        return self.current_time_step >= self.num_time_steps

    def _get_state_vector(self, community, trip_requests):
        state_elements = [
            np.array([
                community.vehicle_count,
                community.trips[0],
                community.trips[1],
                community.rebalancing_targets[community.id],
                community.dispatch_targets[community.id]
            ])
        ]

        # Add neighbor rebalancing targets and trip requests to state vector
        for neighbor_id in self.neighbor_map[community.id]:
            neighbor = self.grid.get_community(neighbor_id)
            state_elements.append(np.array(list(neighbor.rebalancing_targets.values())))
            state_elements.append(np.array(neighbor.trips))

        state_elements.append(trip_requests)
        return np.concatenate(state_elements)

    def _compute_reward(self, community):
        net_vehicle_change = community.available_vehicles - community.previous_available_vehicles
        neighbor_vehicle_change = 0
        for neighbor_id in self.neighbor_map[community.id]:
            neighbor = self.grid.get_community(neighbor_id)
            neighbor_vehicle_change += neighbor.available_vehicles - neighbor.previous_available_vehicles
        community.reward = net_vehicle_change + neighbor_vehicle_change
