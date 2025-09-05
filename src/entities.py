"""
Classes das entidades do jogo Pac-Man
Conversão de C++/SDL2 para Python/pygame-ce
"""

from typing import List, Optional, Tuple
import random
from .constants import *

class Scene:
    """Classe que representa o cenário do jogo"""
    
    def __init__(self):
        """Inicializa o cenário"""
        self.map: List[List[int]] = []
        self.coins = 0
        self._generate_map()
    
    def _generate_map(self):
        """Gera o mapa lógico baseado no layout de cenas"""
        self.map = [[0 for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
        self.coins = 0
        
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                scene_type = SCENES_POSITION[i][j]
                
                if scene_type == 0:  # Espaço vazio
                    self.map[i][j] = FREE_WAY
                elif scene_type == 1:  # Moeda
                    self.map[i][j] = COIN_WAY
                    self.coins += 1
                elif scene_type == 2:  # Power pellet
                    self.map[i][j] = POWER_WAY
                    self.coins += 1
                else:  # Parede/obstáculo
                    self.map[i][j] = OBSTACLE
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Verifica se uma posição é válida (não é obstáculo)"""
        # Aplicar wraparound horizontal
        if x < 0:
            x = MAP_SIZE - 1
        elif x >= MAP_SIZE:
            x = 0
        
        # Verificar limites verticais
        if y < 0 or y >= MAP_SIZE:
            return False
        
        return self.map[y][x] != OBSTACLE
    
    def all_coins_collected(self) -> bool:
        """Verifica se todas as moedas foram coletadas"""
        return self.coins <= 0
    
    def collect_item(self, x: int, y: int) -> int:
        """Coleta um item na posição especificada e retorna os pontos"""
        # Aplicar wraparound horizontal
        if x < 0:
            x = MAP_SIZE - 1
        elif x >= MAP_SIZE:
            x = 0
        
        if 0 <= y < MAP_SIZE:
            if self.map[y][x] == COIN_WAY:
                self.map[y][x] = FREE_WAY
                self.coins -= 1
                return 10
            elif self.map[y][x] == POWER_WAY:
                self.map[y][x] = FREE_WAY
                self.coins -= 1
                return 50
        
        return 0

class Pacman:
    """Classe que representa o Pacman"""
    
    def __init__(self, x: int, y: int):
        """Inicializa o Pacman"""
        self.x = x
        self.y = y
        self.xl = x  # posição anterior x
        self.yl = y  # posição anterior y
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.step = 0
        self.partial = 0
        self.points = 0
        self.power = 0
        self.life = 1
    
    def set_next_direction(self, direction: int):
        """Define a próxima direção desejada"""
        self.next_direction = direction
    
    def move(self, scene: Scene):
        """Move o Pacman"""
        self.partial += 1
        
        if self.partial >= 5:  # Movimento completo
            # Aplicar a próxima direção se possível
            if self._can_move_in_direction(self.next_direction, scene):
                self.direction = self.next_direction
            
            self.partial = 0
            self.xl = self.x
            self.yl = self.y
            
            # Calcular nova posição
            dx, dy = DIRECTIONS[self.direction]
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Aplicar wraparound horizontal
            if new_x < 0:
                new_x = MAP_SIZE - 1
            elif new_x >= MAP_SIZE:
                new_x = 0
            
            # Verificar se pode mover
            if scene.is_valid_position(new_x, new_y):
                self.x = new_x
                self.y = new_y
                
                # Coletar item
                points = scene.collect_item(new_x, new_y)
                self.points += points
                
                if points == 50:  # Power pellet
                    self.power = 100
            
            self.step += 1
        
        # Decrementar poder
        if self.power > 0:
            self.power -= 1
    
    def _can_move_in_direction(self, direction: int, scene: Scene) -> bool:
        """Verifica se pode mover em uma direção específica"""
        dx, dy = DIRECTIONS[direction]
        new_x = self.x + dx
        new_y = self.y + dy
        
        return scene.is_valid_position(new_x, new_y)
    
    def get_screen_position(self) -> Tuple[int, int]:
        """Retorna a posição na tela com interpolação suave"""
        base_x = self.x * CELL_SIZE
        base_y = self.y * CELL_SIZE
        
        if self.partial > 0:
            dx, dy = DIRECTIONS[self.direction]
            offset = self.partial * CELL_SIZE // 5
            base_x += dx * offset
            base_y += dy * offset
        
        return base_x, base_y
    
    def is_alive(self) -> bool:
        """Verifica se o Pacman está vivo"""
        return self.life > 0

class Phantom:
    """Classe que representa um fantasma"""
    
    def __init__(self, x: int, y: int, phantom_id: int, direction: int):
        """Inicializa o fantasma"""
        self.x = x
        self.y = y
        self.xl = x  # posição anterior x
        self.yl = y  # posição anterior y
        self.direction = direction
        self.step = 0
        self.partial = 0
        self.status = CAPTURE
        self.life = 1
        self.id = phantom_id
    
    def move(self, scene: Scene):
        """Move o fantasma"""
        self.partial += 1
        
        if self.partial >= 5:  # Movimento completo
            self.partial = 0
            self.xl = self.x
            self.yl = self.y
            
            # Calcular nova posição na direção atual
            dx, dy = DIRECTIONS[self.direction]
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Aplicar wraparound horizontal
            if new_x < 0:
                new_x = MAP_SIZE - 1
            elif new_x >= MAP_SIZE:
                new_x = 0
            
            # Verificar se pode mover na direção atual
            if scene.is_valid_position(new_x, new_y):
                self.x = new_x
                self.y = new_y
            else:
                # Se não pode mover, escolher nova direção aleatória
                self._choose_new_direction(scene)
            
            self.step += 1
    
    def _choose_new_direction(self, scene: Scene):
        """Escolhe uma nova direção válida"""
        valid_directions = []
        
        for direction in range(4):
            dx, dy = DIRECTIONS[direction]
            test_x = self.x + dx
            test_y = self.y + dy
            
            # Aplicar wraparound horizontal
            if test_x < 0:
                test_x = MAP_SIZE - 1
            elif test_x >= MAP_SIZE:
                test_x = 0
            
            if scene.is_valid_position(test_x, test_y):
                valid_directions.append(direction)
        
        if valid_directions:
            self.direction = random.choice(valid_directions)
            
            # Mover na nova direção
            dx, dy = DIRECTIONS[self.direction]
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Aplicar wraparound horizontal
            if new_x < 0:
                new_x = MAP_SIZE - 1
            elif new_x >= MAP_SIZE:
                new_x = 0
            
            self.x = new_x
            self.y = new_y
    
    def get_screen_position(self) -> Tuple[int, int]:
        """Retorna a posição na tela com interpolação suave"""
        base_x = self.x * CELL_SIZE
        base_y = self.y * CELL_SIZE
        
        if self.partial > 0:
            dx, dy = DIRECTIONS[self.direction]
            offset = self.partial * CELL_SIZE // 5
            base_x += dx * offset
            base_y += dy * offset
        
        return base_x, base_y
