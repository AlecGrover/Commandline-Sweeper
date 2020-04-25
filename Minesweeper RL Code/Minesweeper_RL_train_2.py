from collections import deque
import tensorflow as tf
import numpy as np
import gym
import MinesweeperEnv as MsE
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, Activation
import random

EPISODES = 5000
SHOW_EVERY = 500
HEIGHT = 10
WIDTH = 10
MINES = 10
env = MsE.CustomEnv(size_x=WIDTH, size_y=HEIGHT, num_mines=MINES)

DISCOUNT = 0.98
epsilon = 0.8
EPSILON_DECAY = 0.9998
BASE_EPSILON = 0.001
SAMPLE_SET_SIZE = 64
HISTORY_SIZE = 8196
MIN_HISTORY = 512


class Player:
    def __init__(self):
        self.model = self.new_model()

        self.target_model = self.new_model()
        self.target_model.set_weights(self.model.get_weights())

        self.history = deque(maxlen=HISTORY_SIZE)

        self.weight_update_scheduler = 0

    def new_model(self):
        model = Sequential()
        model.add(Conv2D(512, (1, 3), input_shape=(WIDTH, HEIGHT, 1)))
        model.add(Activation('relu'))
        model.add(Dropout(0.2))

        model.add(Dense(WIDTH * HEIGHT, input_dim=WIDTH * HEIGHT, activation='relu'))
        model.add(Dropout(0.2))

        model.add(Flatten())
        model.add(Dense(WIDTH * HEIGHT))

        model.add(Dense(WIDTH * HEIGHT, activation='linear'))
        model.compile(
            optimizer=tf.keras.optimizers.Adam(lr=0.001),
            loss='mse',
            metrics=['accuracy']
        )
        return model

    def write_history(self, transition):
        self.history.append(transition)

    def train(self, done):

        if SAMPLE_SET_SIZE > len(self.history):
            return
        sample_set = random.sample(self.history, SAMPLE_SET_SIZE)

        existing_states = np.array([transition[0] for transition in sample_set])
        existing_q_vals = self.model.predict(existing_states)

        new_states = np.array([transition[3] for transition in sample_set])
        new_q_vals = self.target_model.predict(new_states)

        X = []
        Y = []

        for i, (s, a, r, n_s, done) in enumerate(sample_set):
            if not done:
                best_new_q = np.max(new_q_vals[i])
                best_q = r + DISCOUNT * best_new_q
            else:
                best_q = r

            existing_q = existing_q_vals[i]
            existing_q[a] = best_q

            X.append(s)
            Y.append(existing_q)

        self.model.fit(np.array(X), np.array(Y), batch_size=SAMPLE_SET_SIZE, shuffle=False, verbose=False)

        if done:
            self.weight_update_scheduler += 1

        if self.weight_update_scheduler > 5:
            self.target_model.set_weights(self.model.get_weights())
            self.weight_update_scheduler = 0

    def get_predictions(self, s):
        return self.model.predict(np.array(state).reshape(-1, *s.shape))[0]


player = Player()


rewards = []

# gradients_to_apply = model.trainable_variables
# for i, gradient in enumerate(gradients_to_apply):
#     gradients_to_apply[i] = gradient * 0
# trainable_variables = model.trainable_variables

for episode in range(EPISODES + 1):
    state = env.reset()
    state = state[:, :, np.newaxis]
    # print(state.shape)

    sequence = []
    episode_reward = 0
    done = 0
    random.seed()
    while not done:
        if random.random() > epsilon:
            action = np.array(np.unravel_index(np.argmax(player.get_predictions(state)), (WIDTH, HEIGHT)))
            # print("Chose the best action")
        else:
            random_x = random.randint(0, WIDTH - 1)
            random_y = random.randint(0, HEIGHT - 1)
            action = np.array([random_x, random_y])
            # print("Chose a random action")

        next_state, r, done, _ = env.step(action)
        next_state = next_state[:, :, np.newaxis]

        episode_reward += r

        player.write_history((state, np.ravel_multi_index(action, (WIDTH, HEIGHT)), r, next_state, done))
        # print("Made History")
        player.train(done)
        # print("Did some training")

        # print(done)

        state = next_state

    rewards.append(episode_reward)
    # print("Finished an Episode")
    if not episode % 25:
        print(episode)
    if not episode % 100:
        print("Episode {0} finished with code {1} and reward {2}. Current Epsilon: {3}".format(episode, done,
                                                                                               episode_reward, epsilon))
        avg_r = sum(rewards[-100:])/len(rewards[-100:])
        min_r = min(rewards[-100:])
        max_r = max(rewards[-100:])
        if avg_r > 0:
            player.model.save(r"models\average-{0}-best-{1}-worst-{2}-episode-{3}.model".format(avg_r, max_r, min_r, episode))

    if not episode % SHOW_EVERY:
        env.render()
        if done == 2:
            print("WIN")
        else:
            print("LOSS")

    if epsilon > BASE_EPSILON:
        epsilon *= EPSILON_DECAY
        if epsilon < BASE_EPSILON:
            epsilon = BASE_EPSILON

