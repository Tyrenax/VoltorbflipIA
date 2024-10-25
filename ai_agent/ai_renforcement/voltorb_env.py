
import gym
from gym import spaces
import numpy as np
from voltorb_flip.game import VoltorbFlip, GameState, CellState

class VoltorbEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        super(VoltorbEnv, self).__init__()
        
        self.game = VoltorbFlip()
        
        # Définition de l'espace d'action
        # 25 cases possibles (5x5)
        self.action_space = spaces.Discrete(25)
        
         # Définition de l'espace d'observation
        # 25 éléments pour l'état des cases
        # + 10 élements pours les colones car 5 informations sur les voltorbs + 5 information sur les points et même chose pour les lignes donc +10
        # Total : 45 éléments
        self.observation_space = spaces.Box(low=0, high=3, shape=(45,), dtype=np.int32)
        
    def reset(self):
        if self.game.state == GameState.WON:
            self.game.bump_level()
        else:
            self.game.reset_level()
        return self._get_observation()
    
    def step(self, action):
        row = action // 5
        col = action % 5
        
        # Vérifier si l'action est valide
        if self.game.cell_states[row][col] != CellState.COVERED:
            # Action invalide, forte pénalité
            reward = -50
            done = True
            return self._get_observation(), reward, done, {}
        
        # Effectuer l'action
        try:
            self.game.flip(row, col)
            # Calculer la récompense
            cell_value = self.game.board[row][col]
            if cell_value == 0:
                # Voltorbe, grosse pénalité
                reward = -100
                done = True
            else:
                # Récompense proportionnelle à la valeur découverte
                reward = cell_value*10
                done = False
        except Exception as e:
            # En cas d'erreur, pénalité
            reward = -50
            done = True
        
        # Vérifier si la partie est gagnée
        if self.game.state == GameState.WON:
            reward = 200
            done = True
        elif self.game.state == GameState.LOST:
            reward = -100
            done = True
        info = {'level': self.game.level}
        
        return self._get_observation(), reward, done, info
    
    def render(self, mode='human'):
        # Optionnel : Afficher le plateau de jeu
        print("Plateau actuel :")
        for row in self.game.cell_states:
            print(' '.join([self._cell_to_str(cell) for cell in row]))
        print("\n")
    
    def _get_observation(self):
        # Construire l'observation sous forme de vecteur
        # Exemple : état des cases + indices des lignes et colonnes
        obs = []
        for row in self.game.cell_states:
            for cell in row:
                if cell == CellState.COVERED:
                    obs.append(0)
                elif cell == CellState.UNCOVERED:
                    obs.append(1)
                else:
                    obs.append(-1)  # Marquée
                
        # Ajouter les indices des lignes et colonnes
        obs.extend(self.game.horizontal_points)
        obs.extend(self.game.horizontal_bombs)
        obs.extend(self.game.vertical_points)
        obs.extend(self.game.vertical_bombs)
        
        return np.array(obs, dtype=int)

    
    def _cell_to_str(self, cell_state):
        if cell_state == CellState.COVERED:
            return '?'
        elif cell_state == CellState.UNCOVERED:
            return 'U'
        elif cell_state == CellState.MARKED_0:
            return 'M'
        else:
            return '?'
    
    def close(self):
        pass
