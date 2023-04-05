import numpy as np
from tqdm import tqdm
import time


class Q_Environment:
    def __init__(self,episodes, num_time_steps, communities, num_evs, petitions_satisfied_energy_consumed):
        self.episodes = episodes
        self.num_time_steps = num_time_steps
        self.current_time_step = 0
        self.communities = communities
        self.num_evs = num_evs
        self.petitions_satisfied_energy_consumed = petitions_satisfied_energy_consumed
        # Rebalance and compute reward based on trips
        self.q_communities = communities
        self.actions = ['serve', 'rebalance_trips']
        self.states = []
        self.rewards = {}
        self.q_table = []

    def compute_initial_states_and_rewards(self):
        for community in self.communities:
            from_community_id = community.get_state()['id']
            for neighbor in community.get_state()['neighbors']:
                to_community_id = self.communities[neighbor-1].get_state()['id']
                print(f"{to_community_id}")
                for from_community_ev in range(1, self.num_evs+1):
                    for to_community_ev in range(1, self.num_evs+1):
                        if from_community_ev + to_community_ev > self.num_evs:
                            continue
                        for action in self.actions:
                            self.states.append((from_community_id, from_community_ev,
                                                to_community_id, to_community_ev, action))
        print(f"Checking if the states are valid")
        for state in self.states:
            from_community_id, from_community_ev, to_community_id, to_community_ev, action = state
            from_community_key = 'SEC_' + str(from_community_id) + "_num_EVs_" + str(from_community_ev)
            to_community_key = 'SEC_' + str(to_community_id) + "_num_EVs_" + str(to_community_ev)
            from_community_petitions, from_community_energy = self.petitions_satisfied_energy_consumed[from_community_key]
            to_community_petitions, to_community_energy = self.petitions_satisfied_energy_consumed[to_community_key]
            if action == 'serve':
                self.rewards[state] = from_community_petitions
            else:
                reward = (from_community_petitions+to_community_petitions)/2

        self.q_table = [np.random.rand(len(self.states), len(self.actions))
                        for _ in range(len(self.communities))]
        print(f"{self.q_table}")

    def target_policy(self, community):
        print(f"Target Policy")
        neighbors = community.get_state()['neighbors']
        commumity_key = 'SEC_' + str(community.get_state()['id']) + "_num_EVs_" + str(community.get_state()['available_vehicles'])
        serve_reward = self.petitions_satisfied_energy_consumed[commumity_key][0]
        rebalance_reward_tracker = {}
        for neighbor in neighbors:
            to_community_id = self.q_communities[neighbor-1].get_state()['id']
            to_community_ev = self.q_communities[neighbor-1].get_state()['available_vehicles']




    def exploratory_policy(self):
        print(f"Exploratory Policy")

    def run(self):
        # Q-learning loop
        alpha = 0.1
        gamma = 0.99
        petitions_tracker = 0
        for episode in tqdm(range(self.episodes)):
            done = False
            t = 0
            while t < self.num_time_steps and not done:
                for i in range(len(self.q_communities)):
                    np.random.seed(time.time())
                    sec_id, vehicle_count, action_state = current_states[i]
                    # Choose an action using an epsilon-greedy strategy
                    epsilon = 0.1
                    if np.random.uniform(0, 1) < epsilon:
                        action = exploratory_policy()
                    else:
                        action = target_policy(current_states[i], i)
                    if action == 'serve':
                        next_state = current_states[i]
                    else:
                        if vehicle_count == 1 or vehicle_count == 2:
                            next_state = current_states[i]
                        else:
                            rebalanced_vehicles = int(0.2 * vehicle_count)
                            neighbor = random.choice(neighbors[sec_id])
                            tmp = list(current_states[neighbor - 1])
                            tmp[1] = tmp[1] + rebalanced_vehicles
                            current_states[neighbor - 1] = tuple(tmp)
                            next_state = (current_states[i][0], current_states[i][1] - rebalanced_vehicles, action)
                    reward = rewards[next_state]
                    petitions_tracker += 1
                    # Update the Q-value for the current state-action pair
                    discounted_reward = q_table[i][states.index(current_states[i]), actions.index(action)] + \
                                        alpha * (reward + gamma * np.max(q_table[i][states.index(next_state)])
                                                 - q_table[i][states.index(current_states[i]), actions.index(action)])
                    q_table[i][states.index(current_states[i]), actions.index(action)] = discounted_reward

                    # Update the state
                    current_states[i] = next_state
                    # Check if all the communities have no idle vehicles and no passengers
                    # if all([state[2] == 0 and state[3] == 0 for state in states]):
                    #     done = True
                    #     break
                t += 1
        # print(f"Total Petitions Satisfied: {petitions_tracker}")



