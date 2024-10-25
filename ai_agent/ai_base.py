from abc import ABC, abstractmethod

class AIBase(ABC):
    @abstractmethod
    def decide_action(self, game_state):
        """
        Cette méthode doit être implémentée par chaque IA.
        Elle prend en entrée l'état actuel du jeu et renvoie l'action à effectuer.
        """
        pass
    
