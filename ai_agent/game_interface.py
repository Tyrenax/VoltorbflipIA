
from voltorb_flip.game import VoltorbFlip, GameState, CellState

class GameInterface:
    def __init__(self):
        self.game = VoltorbFlip()
    
    def get_game_state(self):
        # Récupère l'état actuel du jeu à transmettre à l'IA
        return {
            'board': self.game.board,
            'cell_states': self.game.cell_states,
            'level': self.game.level,
            'current_score': self.game.current_score,
            'state': self.game.state,
            'maximum_points': self.game.maximum_points,
            'horizontal_points': self.game.horizontal_points,
            'horizontal_bombs': self.game.horizontal_bombs,
            'vertical_points': self.game.vertical_points,
            'vertical_bombs': self.game.vertical_bombs,
        }
    
    def execute_action(self, action):
        # Exécute l'action retournée par l'IA
        if action['type'] == 'flip':
            row, col = action['position']
            try:
                self.game.flip(row, col)
                return True
            except Exception as e:
                print(f"Erreur lors du retournement de la case ({row}, {col}): {e}")
                return False
        else:
            print(f"Action inconnue : {action}")
            return False
    
    def is_game_over(self):
        return self.game.state != GameState.IN_PROGRESS
    
    def get_game_result(self):
        return self.game.state
