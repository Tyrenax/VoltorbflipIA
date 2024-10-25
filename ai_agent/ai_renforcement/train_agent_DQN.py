from voltorb_env import VoltorbEnv
import gym
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CallbackList, EvalCallback
from datetime import datetime

def main():
    env = VoltorbEnv()
    eval_env = VoltorbEnv()

    # Obtenir le timestamp actuel
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Chemins pour les sauvegardes et les logs
    best_model_path = f'./logs/{timestamp}/'
    tensorboard_log_path = f'./voltorb_tensorboard/{timestamp}/'

    # Callbacks
    eval_callback = EvalCallback(eval_env, best_model_save_path=best_model_path,
                                 log_path=best_model_path, eval_freq=5000,
                                 deterministic=True, render=False)
    
    # Ajouter EvalCallback à la liste des callbacks
    callbacks = CallbackList([eval_callback])

    # Créer le modèle DQN avec logging pour TensorBoard
    model = DQN('MlpPolicy', env, verbose=1, tensorboard_log=tensorboard_log_path)

    # Entraîner le modèle avec les callbacks
    model.learn(total_timesteps=100000, callback=callbacks)

    # Sauvegarder le modèle avec timestamp
    model.save(f"dqn_voltorb_{timestamp}")
    env.close()

if __name__ == "__main__":
    main()
