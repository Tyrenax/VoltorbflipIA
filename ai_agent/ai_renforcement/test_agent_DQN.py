# test_agent_DQN.py

from voltorb_env import VoltorbEnv
from stable_baselines3 import DQN

def main():
    env = VoltorbEnv()
    model = DQN.load("dqn_voltorb")
    
    num_episodes = 100
    total_rewards = []
    levels_reached = []

    for episode in range(num_episodes):
        obs = env.reset()
        done = False
        total_reward = 0
        level = env.game.level

        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            total_reward += reward
            level = info.get('level', level)

        total_rewards.append(total_reward)
        levels_reached.append(level)

    avg_reward = sum(total_rewards) / num_episodes
    avg_level = sum(levels_reached) / num_episodes
    print(f"Récompense moyenne sur {num_episodes} épisodes : {avg_reward}")
    print(f"Niveau moyen atteint : {avg_level}")

    env.close()

if __name__ == "__main__":
    main()
