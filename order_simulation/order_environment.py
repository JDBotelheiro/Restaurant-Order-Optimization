import gym
import numpy as np
import time

class OrderEnv(gym.Env):
    def __init__(self, roo):
        super(OrderEnv, self).__init__()
        self.roo = roo
        self.state = self.get_initial_state()

        n_features = 5  # Adjust this as per your requirements

        self.action_space = gym.spaces.Discrete(len(self.roo.orders))
        self.observation_space = gym.spaces.Box(low=0, high=np.inf, shape=(len(self.roo.orders), n_features))

    def step(self, action):
        reward = self.roo.process_order(action)
        self.state = self.get_state()
        done = self.check_if_done()
        return self.state, reward, done, {}

    def reset(self):
        self.roo.reset()
        self.state = self.get_initial_state()
        return self.state

    def render(self, mode='human'):
        print(self.state)

    def get_initial_state(self):
        return np.array([self.get_order_features(order) for order in self.roo.orders])

    def get_order_features(self, order):
        features = []
        features.append(order.total_complexity)
        features.append(order.wait_time)
        features.append(self.encode_source(order.source))
        features.append(len(order.dishes))
        return features

    def encode_source(self, source):
        if source == 'Bolt Foods':
            return 1
        elif source == 'UberEats':
            return 2
        elif source == 'Glovo':
            return 3
        else:  # Assuming the only remaining source is 'In Restaurant'
            return 4

    def get_state(self):
        return np.array([self.get_order_features(order) for order in self.roo.orders if not order.processed])

    def check_if_done(self):
        return all(order.processed for order in self.roo.orders)