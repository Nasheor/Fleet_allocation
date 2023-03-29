class Community:
    def __init__(self, community_id, x_loc, y_loc, initial_vehicle_count, trips, energy, neighbors):
        self.community_id = community_id
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.initial_vehicle_count = initial_vehicle_count
        self.available_vehicles = initial_vehicle_count
        self.initial_trips = trips
        self.energy = energy
        self.neighbors = neighbors
        self.reward = 0
        self.trips_satisfied = 0

    def reset(self):
        self.available_vehicles = self.initial_vehicle_count
        self.trips_satisfied = 0
        self.reward = 0

    def get_state(self):
        # Return the current state of the community
        state = {
            'available_vehicles': self.available_vehicles,
            'trips': self.trips,
            'energy_consumed': self.energy,
            'reward': self.reward
        }
        return state

    def set_state(self, available_vehicles, trips, energy, reward):
        self.available_vehicles = available_vehicles
        self.trips = trips
        self.energy = energy
        self.reward = reward
