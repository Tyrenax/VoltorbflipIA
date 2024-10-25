# test_agent_DQN.py

from voltorb_env import VoltorbEnv
from stable_baselines3 import DQN

def main():
    env = VoltorbEnv()
    model = DQN.load("dqn_voltorb")  # Remplacez par le nom de votre modèle sauvegardé

    obs = env.reset()
    done = False
    total_reward = 0
    step_num = 0

    print("--- Début de la partie ---")
    env.render()  # Afficher le plateau initial

    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        total_reward += reward
        step_num += 1

        print(f"Étape {step_num}")
        env.render()  # Afficher le plateau après l'action
        print(f"Action choisie : {action} (ligne {action // 5}, colonne {action % 5})")
        print(f"Récompense : {reward}")
        print(f"Action invalide : {info.get('invalid_action', False)}")
        print(f"Niveau actuel : {info.get('level', 1)}\n")

    print("--- Fin de la partie ---")
    print(f"Score total : {env.game.current_score}")
    print(f"Récompense totale : {total_reward}")
    print(f"Niveau atteint : {info.get('level', 1)}")
    print(f"Nombre total d'actions invalides : {info.get('invalid_action_count', 0)}")

    env.close()

if __name__ == "__main__":
    main()
