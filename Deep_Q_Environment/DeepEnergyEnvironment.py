from Q_Environment import EnergyEnvironment
import numpy as np
import random
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential


class DeepEnergyEnvironment(EnergyEnvironment):
    def __init__(self, episodes, num_time_steps, communities, num_evs, petitions_satisfied_energy_consumed,
                 state_size, action_size):
        super().__init__(episodes, num_time_steps, communities, num_evs, petitions_satisfied_energy_consumed)
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.batch_size = 32
        self.learning_rate = 0.001
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.gamma = 0.99
        self.target_update_freq = 100
        self.model = self.build_model()
        self.target_model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(128, input_dim=self.state_size, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        minibatch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                t = self.target_model.predict(next_state)[0]
                target[0][action] = reward + self.gamma * np.amax(t)
            self.model.fit(state, target, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def run(self):
        step_count = 0
        for episode in range(self.episodes):
            self.reset()
            for t in range(self.num_time_steps):
                for i in range(len(self.q_communities)):
                    # Convert the state to an appropriate input for the neural network
                    state = np.reshape(self.get_state_representation(), [1, self.state_size])
                    action = self.act(state)
                    reward, next_state, done = self.step(action, community_index=i)
                    next_state = np.reshape(next_state, [1, self.state_size])

                    self.remember(state, action, reward, next_state, done)
                    state = next_state

                    self.replay()

                    step_count += 1
                    if step_count % self.target_update_freq == 0:
                        self.update_target_model()

    def step(self, action, community_index):
        # Implement the logic for executing the chosen action and returning the next state, reward, and completion status
        done = False

        # Extract the current state information
        from_community_id, from_community_ev, to_community_id, to_community_ev = self.get_state_information(community_index)

        # Perform the action
        if self.actions[action] == 'serve':
            # Update trips satisfied and energy consumed based on the action
            self.serve(from_community_id, from_community_ev)
        elif self.actions[action] == 'rebalance_energy':
            # Rebalance vehicles and update trips satisfied and energy consumed
            self.rebalance_trips(from_community_id, from_community_ev, to_community_id, to_community_ev)

        # Get the next state information
        next_state = self.get_state_representation()

        # Calculate the reward based on the new state
        reward = self.calculate_reward(from_community_id, from_community_ev, to_community_id, to_community_ev, self.actions[action])


        return reward, next_state, done

