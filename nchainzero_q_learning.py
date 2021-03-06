import gym 
import numpy as np
from keras.models import Sequential
from keras.layers import InputLayer, Dense
from tqdm import trange


model = Sequential()
model.add(InputLayer(batch_input_shape=(1, 5)))
model.add(Dense(10, activation='sigmoid'))
model.add(Dense(2, activation='linear'))
model.compile(loss='mse', optimizer='adam', metrics=['mae'])


def eps_q_learn_nn_train(env, num_episodes=500):
    # now execute the q learning
    y = 0.95
    eps = 0.5
    decay_factor = 0.999
    r_avg_list = []
    for _ in trange(num_episodes):
        s = env.reset()
        eps *= decay_factor
        done = False
        r_sum = 0
        while not done:
            if np.random.random() < eps:
                a = np.random.randint(0, 2)
            else:
                a = np.argmax(model.predict(np.identity(5)[s:s + 1]))
            new_s, r, done, _ = env.step(a)
            target = r + y * np.max(model.predict(np.identity(5)[new_s:new_s + 1]))
            target_vec = model.predict(np.identity(5)[s:s + 1])[0]
            target_vec[a] = target
            model.fit(np.identity(5)[s:s + 1], target_vec.reshape(-1, 2), epochs=1, verbose=0)
            s = new_s
            r_sum += r
        r_avg_list.append(r_sum / 1000)

def display_q_table():
    for s in range(5):
        print(model.predict(np.identity(5)[s:s + 1])[0])

if __name__=='__main__':
    env = gym.make('NChain-v0')
    env.reset()
    eps_q_learn_nn_train(env)
    print("Training complete")
    display_q_table()