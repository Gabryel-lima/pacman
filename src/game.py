"""
Classe principal do jogo Pac-Man
Baseada na lógica do arquivo Pac_Man.py
"""

import pygame as pg
import random
import os
from .constants import *
from .controller import ControllerManager, ControllerType


class PacMan:
    """Classe principal do jogo Pac-Man baseada no arquivo de referência"""
    
    def __init__(self, scale):
        """Inicializa o jogo com o fator de escala especificado"""
        self.white = WHITE
        self.black = BLACK
        self.blue = BLUE
        
        # Calcular dimensões da janela baseado no parâmetro scale
        window_width = scale * 27.5
        window_height = scale * 35
        
        # Configurar janela
        self.window = pg.display.set_mode((window_width, window_height))
        pg.display.set_caption("Pac-Man")
        
        # Configurar fonte
        pg.font.init()
        self.font = pg.font.SysFont("Courier New", scale * 2, bold=True)
        
        # Configurar clock
        self.clock = pg.time.Clock()
        
        # Variáveis do jogo
        self.scale = scale
        self.sprite_frame = 0
        self.sprite_speed = SPRITE_SPEED
        
        # Estado do jogo
        self.score = 0
        self.lives = 5
        self.end_game = False
        self.harmless_mode = False
        self.harmless_mode_timer = 0
        self.harmless_mode_ghost_blue = False
        self.harmless_mode_ghost_orange = False
        self.harmless_mode_ghost_pink = False
        self.harmless_mode_ghost_red = False
        
        # Posições e direções do Pacman (calculadas dinamicamente)
        self.pac_man_pos = [scale * 13.1, scale * 22.6]
        self.pac_man_direction = [scale/16, 0]
        self.pac_man_next_direction = [scale/16, 0]
        
        # Posições e direções dos fantasmas (calculadas dinamicamente)
        self.ghost_blue_pos = [scale * 12, scale * 13]
        self.ghost_orange_pos = [scale * 12, scale * 14.5]
        self.ghost_pink_pos = [scale * 14, scale * 13]
        self.ghost_red_pos = [scale * 14, scale * 14.5]
        
        self.ghost_blue_direction = [0, 0]
        self.ghost_orange_direction = [0, 0]
        self.ghost_pink_direction = [0, 0]
        self.ghost_red_direction = [0, 0]
        
        self.ghost_blue_next_direction = [0, 0]
        self.ghost_orange_next_direction = [0, 0]
        self.ghost_pink_next_direction = [0, 0]
        self.ghost_red_next_direction = [0, 0]
        
        # Distâncias dos fantasmas ao Pacman
        self.distance_ghost_blue_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_blue_pos)
        self.distance_ghost_orange_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_orange_pos)
        self.distance_ghost_pink_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_pink_pos)
        self.distance_ghost_red_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_red_pos)
        
        # Carregar sprites do Pacman
        self._load_pacman_sprites()
        
        # Carregar sprites dos fantasmas
        self._load_ghost_sprites()
        
        # Mapa do jogo
        self.map = [row[:] for row in GAME_MAP]  # Cópia do mapa
        
        # Sistema de controles
        self.controller_manager = ControllerManager()
        self.controller_connected = self.controller_manager.get_controller_count() > 0
        self.controller_index = 0  # Usar o primeiro controle conectado
    
    def _load_pacman_sprites(self):
        """Carrega os sprites do Pacman"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_dir = os.path.join(base_dir, "img")
        
        # Lista de sprites do Pacman (17 frames)
        pacman_sprites = []
        for i in range(1, 18):
            sprite_path = os.path.join(img_dir, f"Pac_Man_{i}.png")
            if os.path.exists(sprite_path):
                sprite = pg.image.load(sprite_path)
                scaled_sprite = pg.transform.scale(sprite, (self.scale * 1.3, self.scale * 1.3))
                pacman_sprites.append(scaled_sprite)
            else:
                # Criar sprite placeholder se não existir
                placeholder = pg.Surface((self.scale * 1.3, self.scale * 1.3))
                placeholder.fill((255, 255, 0))  # Amarelo
                pacman_sprites.append(placeholder)
        
        # Atribuir sprites às variáveis
        for i, sprite in enumerate(pacman_sprites):
            setattr(self, f"pac_man_{i+1}", sprite)
    
    def _load_ghost_sprites(self):
        """Carrega os sprites dos fantasmas"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_dir = os.path.join(base_dir, "img")
        
        # Cores dos fantasmas
        ghost_colors = ['Blue', 'Orange', 'Pink', 'Red']
        
        for color in ghost_colors:
            # Carregar sprites de movimento normal
            for frame in range(2):
                sprite_path = os.path.join(img_dir, f"{color}_Ghost_Down_Right_{frame}.png")
                if os.path.exists(sprite_path):
                    sprite = pg.image.load(sprite_path)
                    scaled_sprite = pg.transform.scale(sprite, (self.scale * 1.3, self.scale * 1.3))
                    setattr(self, f"ghost_{color.lower()}_down_right_{frame}", scaled_sprite)
                else:
                    # Criar placeholder
                    placeholder = pg.Surface((self.scale * 1.3, self.scale * 1.3))
                    if color == 'Blue':
                        placeholder.fill((0, 100, 255))
                    elif color == 'Orange':
                        placeholder.fill((255, 165, 0))
                    elif color == 'Pink':
                        placeholder.fill((255, 192, 203))
                    else:  # Red
                        placeholder.fill((255, 0, 0))
                    setattr(self, f"ghost_{color.lower()}_down_right_{frame}", placeholder)
        
        # Carregar sprites de fantasma inofensivo
        for frame in range(2):
            sprite_path = os.path.join(img_dir, f"Harmless_Ghost_{frame}.png")
            if os.path.exists(sprite_path):
                sprite = pg.image.load(sprite_path)
                scaled_sprite = pg.transform.scale(sprite, (self.scale * 1.3, self.scale * 1.3))
                setattr(self, f"ghost_harmless_{frame}", scaled_sprite)
            else:
                # Criar placeholder azul
                placeholder = pg.Surface((self.scale * 1.3, self.scale * 1.3))
                placeholder.fill((100, 100, 255))
                setattr(self, f"ghost_harmless_{frame}", placeholder)
    
    def clear_window(self):
        """Limpa a janela com a cor de fundo"""
        pg.draw.rect(self.window, self.black, (0, 0, self.window.get_width(), self.window.get_height()))
    
    def move(self, key):
        """Processa entrada do teclado para movimento do Pacman"""
        if key == 'r':
            self.restart()
        elif key == 'w' or key == 'up':
            self._set_direction('up')
        elif key == 'a' or key == 'left':
            self._set_direction('left')
        elif key == 's' or key == 'down':
            self._set_direction('down')
        elif key == 'd' or key == 'right':
            self._set_direction('right')
    
    def _set_direction(self, direction):
        """Define a direção do Pacman baseada no input"""
        if direction == 'up':
            if self.pac_man_direction[0] == 0 and self.pac_man_direction[1] > 0:
                self.pac_man_direction[0] = 0
                self.pac_man_direction[1] = -self.scale/16
                self.pac_man_next_direction[0] = 0
                self.pac_man_next_direction[1] = -self.scale/16
            elif self.pac_man_direction[0] != 0 and self.pac_man_direction[1] == 0:
                self.pac_man_next_direction[0] = 0
                self.pac_man_next_direction[1] = -self.scale/16
        elif direction == 'left':
            if self.pac_man_direction[0] > 0 and self.pac_man_direction[1] == 0:
                self.pac_man_direction[0] = -self.scale/16
                self.pac_man_direction[1] = 0
                self.pac_man_next_direction[0] = -self.scale/16
                self.pac_man_next_direction[1] = 0
            elif self.pac_man_direction[0] == 0 and self.pac_man_direction[1] != 0:
                self.pac_man_next_direction[0] = -self.scale/16
                self.pac_man_next_direction[1] = 0
        elif direction == 'down':
            if self.pac_man_direction[0] == 0 and self.pac_man_direction[1] < 0:
                self.pac_man_direction[0] = 0
                self.pac_man_direction[1] = self.scale/16
                self.pac_man_next_direction[0] = 0
                self.pac_man_next_direction[1] = self.scale/16
            elif self.pac_man_direction[0] != 0 and self.pac_man_direction[1] == 0:
                self.pac_man_next_direction[0] = 0
                self.pac_man_next_direction[1] = self.scale/16
        elif direction == 'right':
            if self.pac_man_direction[0] < 0 and self.pac_man_direction[1] == 0:
                self.pac_man_direction[0] = self.scale/16
                self.pac_man_direction[1] = 0
                self.pac_man_next_direction[0] = self.scale/16
                self.pac_man_next_direction[1] = 0
            elif self.pac_man_direction[0] == 0 and self.pac_man_direction[1] != 0:
                self.pac_man_next_direction[0] = self.scale/16
                self.pac_man_next_direction[1] = 0
    
    def handle_controller_input(self):
        """Processa entrada dos controles"""
        if not self.controller_connected:
            return
        
        # Atualizar estado dos controles
        self.controller_manager.update()
        
        # Verificar se ainda há controles conectados
        if self.controller_manager.get_controller_count() == 0:
            self.controller_connected = False
            return
        
        # Obter input de movimento do controle
        direction, has_input = self.controller_manager.get_movement_input(self.controller_index)
        if has_input:
            self._set_direction(direction)
        
        # Obter botões especiais
        special_buttons = self.controller_manager.get_special_buttons(self.controller_index)
        if special_buttons.get('restart', False):
            self.restart()
    
    def board(self):
        """Desenha o tabuleiro do jogo"""
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == WALL:
                    pg.draw.rect(self.window, self.blue, (x * self.scale, y * self.scale, self.scale, self.scale))
                if self.map[y][x] == TUNNEL:
                    pg.draw.rect(self.window, self.white, (x * self.scale, y * self.scale, self.scale, self.scale))
                if self.map[y][x] == EMPTY or self.map[y][x] == DOT or self.map[y][x] == POWER_PELLET:
                    pg.draw.rect(self.window, self.black, ((x * self.scale) - (self.scale / 2), (y * self.scale) - (self.scale / 2), self.scale * 1.5, self.scale * 1.5))
        
        # Desenhar pontos e power pellets
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == DOT:
                    pg.draw.circle(self.window, self.white, ((x * self.scale) + (self.scale / 4), (y * self.scale) + (self.scale / 4)), self.scale / 5)
                if self.map[y][x] == POWER_PELLET:
                    pg.draw.circle(self.window, self.white, ((x * self.scale) + (self.scale / 4), (y * self.scale) + (self.scale / 4)), self.scale / 2)
    
    def animation_step(self):
        """Atualiza o frame de animação"""
        if self.sprite_frame == 60:
            self.sprite_frame = 0
        else:
            self.sprite_frame += self.sprite_speed
    
    def player_rotation(self, image):
        """Rotaciona a imagem do Pacman baseada na direção"""
        x_dir = self.pac_man_direction[0]
        y_dir = self.pac_man_direction[1]
        if x_dir > 0 and y_dir == 0:
            return image
        elif x_dir == 0 and y_dir > 0:
            return pg.transform.rotate(image, -90)
        elif x_dir < 0 and y_dir == 0:
            return pg.transform.flip(image, True, False)
        elif x_dir == 0 and y_dir < 0:
            return pg.transform.rotate(image, 90)
        return image
    
    def collider(self, position, direction):
        """Verifica colisões com paredes"""
        if self.end_game == False:
            position[0] += direction[0]
            position[1] += direction[1]
            for y in range(len(self.map)):
                for x in range(len(self.map[0])):
                    if self.map[y][x] == WALL or self.map[y][x] == TUNNEL:
                        x_wall = (x * self.scale) - (self.scale * 0.65)
                        y_wall = (y * self.scale) - (self.scale * 0.65)
                        wall_size = self.scale * 1.85
                        x_agent = position[0] + (self.scale * 0.65)
                        y_agent = position[1] + (self.scale * 0.65)
                        
                        if x_agent >= x_wall and x_agent <= x_wall + wall_size and y_agent >= y_wall and y_agent <= y_wall + wall_size:
                            position[0] -= direction[0]
                            position[1] -= direction[1]
        return position
    
    def turning_corner(self, position, direction, next_direction):
        """Sistema de curvas para mudança de direção"""
        turned_corner = True
        position[0] += next_direction[0] * 16
        position[1] += next_direction[1] * 16
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == WALL or self.map[y][x] == TUNNEL:
                    x_wall = (x * self.scale) - (self.scale * 0.65)
                    y_wall = (y * self.scale) - (self.scale * 0.65)
                    wall_size = self.scale * 1.85
                    x_agent = position[0] + (self.scale * 0.65)
                    y_agent = position[1] + (self.scale * 0.65)
                    if x_agent >= x_wall and x_agent <= x_wall + wall_size and y_agent >= y_wall and y_agent <= y_wall + wall_size:
                        turned_corner = False
        position[0] -= next_direction[0] * 16
        position[1] -= next_direction[1] * 16
        if turned_corner:
            direction[0] = next_direction[0]
            direction[1] = next_direction[1]
        return direction, next_direction
    
    def collect_dots(self):
        """Coleta pontos e power pellets"""
        x_pac_man = self.pac_man_pos[0] + (self.scale * 0.65)
        y_pac_man = self.pac_man_pos[1] + (self.scale * 0.65)
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == DOT:
                    x_dot = (x * self.scale) + (self.scale / 4)
                    y_dot = (y * self.scale) + (self.scale / 4)
                    radius = self.scale / 5
                    if x_pac_man >= x_dot - radius and x_pac_man <= x_dot + radius and y_pac_man >= y_dot - radius and y_pac_man <= y_dot + radius:
                        self.map[y][x] = EMPTY
                        self.score += DOT_POINTS
                if self.map[y][x] == POWER_PELLET:
                    x_dot = (x * self.scale) + (self.scale / 4)
                    y_dot = (y * self.scale) + (self.scale / 4)
                    radius = self.scale / 2
                    if x_pac_man >= x_dot - radius and x_pac_man <= x_dot + radius and y_pac_man >= y_dot - radius and y_pac_man <= y_dot + radius:
                        self.map[y][x] = EMPTY
                        self.score += POWER_PELLET_POINTS
                        self.harmless_mode = True
                        self.harmless_mode_ghost_blue = True
                        self.harmless_mode_ghost_orange = True
                        self.harmless_mode_ghost_pink = True
                        self.harmless_mode_ghost_red = True
    
    def pacman_tunnel(self, position):
        """Implementa túneis laterais"""
        x_pos = position[0]
        y_pos = position[1]
        if position[0] >= self.scale * 27.5:
            x_pos = 0 - (self.scale * 1.3)
        elif position[0] <= -(self.scale * 1.3):
            x_pos = self.scale * 27.5
        return [x_pos, y_pos]
    
    def player(self):
        """Desenha e atualiza o Pacman"""
        self.pac_man_direction, self.pac_man_next_direction = self.turning_corner(self.pac_man_pos, self.pac_man_direction, self.pac_man_next_direction)
        self.pac_man_pos = self.collider(self.pac_man_pos, self.pac_man_direction)
        self.pac_man_pos = self.pacman_tunnel(self.pac_man_pos)
        x = self.pac_man_pos[0]
        y = self.pac_man_pos[1]
        
        if self.end_game:
            # Animação de morte
            if self.sprite_frame <= 5:
                self.window.blit(self.player_rotation(self.pac_man_6), (x, y))
            elif self.sprite_frame <= 10:
                self.window.blit(self.player_rotation(self.pac_man_7), (x, y))
            elif self.sprite_frame <= 15:
                self.window.blit(self.player_rotation(self.pac_man_8), (x, y))
            elif self.sprite_frame <= 20:
                self.window.blit(self.player_rotation(self.pac_man_9), (x, y))
            elif self.sprite_frame <= 25:
                self.window.blit(self.player_rotation(self.pac_man_10), (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.player_rotation(self.pac_man_11), (x, y))
            elif self.sprite_frame <= 35:
                self.window.blit(self.player_rotation(self.pac_man_12), (x, y))
            elif self.sprite_frame <= 40:
                self.window.blit(self.player_rotation(self.pac_man_13), (x, y))
            elif self.sprite_frame <= 45:
                self.window.blit(self.player_rotation(self.pac_man_14), (x, y))
            elif self.sprite_frame <= 50:
                self.window.blit(self.player_rotation(self.pac_man_15), (x, y))
            elif self.sprite_frame <= 55:
                self.window.blit(self.player_rotation(self.pac_man_16), (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.player_rotation(self.pac_man_17), (x, y))
        else:
            # Animação normal
            if self.sprite_frame <= 6:
                self.window.blit(self.player_rotation(self.pac_man_1), (x, y))
            elif self.sprite_frame <= 12:
                self.window.blit(self.player_rotation(self.pac_man_1), (x, y))
            elif self.sprite_frame <= 18:
                self.window.blit(self.player_rotation(self.pac_man_2), (x, y))
            elif self.sprite_frame <= 24:
                self.window.blit(self.player_rotation(self.pac_man_3), (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.player_rotation(self.pac_man_4), (x, y))
            elif self.sprite_frame <= 36:
                self.window.blit(self.player_rotation(self.pac_man_5), (x, y))
            elif self.sprite_frame <= 42:
                self.window.blit(self.player_rotation(self.pac_man_4), (x, y))
            elif self.sprite_frame <= 48:
                self.window.blit(self.player_rotation(self.pac_man_3), (x, y))
            elif self.sprite_frame <= 54:
                self.window.blit(self.player_rotation(self.pac_man_2), (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.player_rotation(self.pac_man_1), (x, y))
    
    def distance_ghost_to_pac_man(self, ghost_pos):
        """Calcula distância entre fantasma e Pacman"""
        ghost_x = ghost_pos[0] + (self.scale * 0.65)
        ghost_y = ghost_pos[1] + (self.scale * 0.65)
        pac_man_x = self.pac_man_pos[0] + (self.scale * 0.65)
        pac_man_y = self.pac_man_pos[1] + (self.scale * 0.65)
        delta_x = (ghost_x - pac_man_x) ** 2
        delta_y = (ghost_y - pac_man_y) ** 2
        distance = (delta_x + delta_y) ** (1 / 2)
        return distance
    
    def ghost_render(self, color, position):
        """Desenha um fantasma baseado na cor e posição"""
        x = position[0]
        y = position[1]
        if color == 'blue':
            if self.sprite_frame <= 15:
                self.window.blit(self.ghost_blue_down_right_0, (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.ghost_blue_down_right_1, (x, y))
            elif self.sprite_frame <= 45:
                self.window.blit(self.ghost_blue_down_right_0, (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.ghost_blue_down_right_1, (x, y))
        elif color == 'orange':
            if self.sprite_frame <= 15:
                self.window.blit(self.ghost_orange_down_right_0, (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.ghost_orange_down_right_1, (x, y))
            elif self.sprite_frame <= 45:
                self.window.blit(self.ghost_orange_down_right_0, (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.ghost_orange_down_right_1, (x, y))
        elif color == 'pink':
            if self.sprite_frame <= 15:
                self.window.blit(self.ghost_pink_down_right_0, (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.ghost_pink_down_right_1, (x, y))
            elif self.sprite_frame <= 45:
                self.window.blit(self.ghost_pink_down_right_0, (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.ghost_pink_down_right_1, (x, y))
        elif color == 'red':
            if self.sprite_frame <= 15:
                self.window.blit(self.ghost_red_down_right_0, (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.ghost_red_down_right_1, (x, y))
            elif self.sprite_frame <= 45:
                self.window.blit(self.ghost_red_down_right_0, (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.ghost_red_down_right_1, (x, y))
        elif color == 'harmless':
            if self.sprite_frame <= 15:
                self.window.blit(self.ghost_harmless_0, (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.ghost_harmless_1, (x, y))
            elif self.sprite_frame <= 45:
                self.window.blit(self.ghost_harmless_0, (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.ghost_harmless_1, (x, y))
    
    def random_direction_for_ghost(self):
        """Gera direção aleatória para fantasma"""
        move_up_or_sideways = random.randint(0, 1)
        x_direction = random.randint(0, 1)
        y_direction = random.randint(0, 1)
        direction = []
        if move_up_or_sideways == 0:
            if x_direction == 0:
                direction = [-self.scale/16, 0]
            else:
                direction = [self.scale/16, 0]
        else:
            if y_direction == 0:
                direction = [0, -self.scale/16]
            else:
                direction = [0, self.scale/16]
        return direction
    
    def random_next_direction_for_ghost(self, direction):
        """Gera próxima direção aleatória para fantasma"""
        new_direction = [0, 0]
        if direction[0] != 0:
            if random.randint(0, 1) == 0:
                new_direction[1] = -self.scale/16
            else:
                new_direction[1] = self.scale/16
        elif direction[1] != 0:
            if random.randint(0, 1) == 0:
                new_direction[0] = -self.scale/16
            else:
                new_direction[0] = self.scale/16
        return new_direction
    
    def direction_ghost_to_pac_man(self, position, direction):
        """Calcula direção para fantasma perseguir Pacman"""
        new_direction = [0, 0]
        ghost_x = position[0]
        ghost_y = position[1]
        pac_man_x = self.pac_man_pos[0]
        pac_man_y = self.pac_man_pos[1]
        delta_x = ghost_x - pac_man_x
        delta_y = ghost_y - pac_man_y
        if direction[1] != 0:
            if delta_x <= 0:
                new_direction[0] = self.scale/16
            else:
                new_direction[0] = -self.scale/16
        if direction[0] != 0:
            if delta_y <= 0:
                new_direction[1] = self.scale/16
            else:
                new_direction[1] = -self.scale/16
        return new_direction
    
    def direction_harmless_ghost_to_pac_man(self, position, direction):
        """Calcula direção para fantasma fugir do Pacman"""
        new_direction = [0, 0]
        ghost_x = position[0]
        ghost_y = position[1]
        pac_man_x = self.pac_man_pos[0]
        pac_man_y = self.pac_man_pos[1]
        delta_x = ghost_x - pac_man_x
        delta_y = ghost_y - pac_man_y
        if direction[1] != 0:
            if delta_x <= 0:
                new_direction[0] = -self.scale/16
            else:
                new_direction[0] = self.scale/16
        if direction[0] != 0:
            if delta_y <= 0:
                new_direction[1] = -self.scale/16
            else:
                new_direction[1] = self.scale/16
        return new_direction
    
    def new_random_direction_for_ghost(self, position, direction):
        """Gera nova direção aleatória para fantasma quando está preso"""
        new_direction = [0, 0]
        pos = [0, 0]
        pos[0] = position[0]
        pos[1] = position[1]
        
        if direction[0] != 0:
            if random.randint(0, 1) == 0:
                new_direction[1] = -self.scale/8
            else:
                new_direction[1] = self.scale/8
        elif direction[1] != 0:
            if random.randint(0, 1) == 0:
                new_direction[0] = -self.scale/8
            else:
                new_direction[0] = self.scale/8
        
        new_position = self.collider(pos, new_direction)
        
        if position == new_position:
            new_direction[0] *= -1
            new_direction[1] *= -1
            new_position = self.collider(pos, new_direction)
        
        new_direction[0] /= 2
        new_direction[1] /= 2
        
        return new_position, new_direction
    
    def ghost_intelligence(self, ghost_pos, ghost_direction, ghost_next_direction, distance_ghost_to_pac_man, harmless_ghost_mode):
        """IA do fantasma - decide movimento baseado na distância e modo"""
        ghost_blue_pos = [0, 0]
        ghost_blue_pos[0] = ghost_pos[0]
        ghost_blue_pos[1] = ghost_pos[1]
        distance_ghost_to_pac_man = self.distance_ghost_to_pac_man(ghost_pos)
        if distance_ghost_to_pac_man <= self.scale * 10:
            if harmless_ghost_mode:
                ghost_next_direction = self.direction_harmless_ghost_to_pac_man(ghost_pos, ghost_direction)
            else:
                ghost_next_direction = self.direction_ghost_to_pac_man(ghost_pos, ghost_direction)
            ghost_direction, ghost_next_direction = self.turning_corner(ghost_pos, ghost_direction, ghost_next_direction)
        if ghost_direction == ghost_next_direction:
            if harmless_ghost_mode:
                ghost_next_direction = self.direction_harmless_ghost_to_pac_man(ghost_pos, ghost_direction)
            else:
                ghost_next_direction = self.direction_ghost_to_pac_man(ghost_pos, ghost_direction)
            ghost_pos = self.collider(ghost_pos, ghost_direction)
        ghost_pos = self.pacman_tunnel(ghost_pos)
        ghost_pos = self.collider(ghost_pos, ghost_direction)
        if ghost_blue_pos == ghost_pos:
            ghost_pos, ghost_direction = self.new_random_direction_for_ghost(ghost_pos, ghost_direction)
        return ghost_pos, ghost_direction, ghost_next_direction, distance_ghost_to_pac_man
    
    def ghost(self):
        """Atualiza e move todos os fantasmas"""
        # Fantasma azul
        if self.ghost_blue_pos != [self.scale * 12, self.scale * 13]:
            input_1 = self.ghost_blue_pos
            input_2 = self.ghost_blue_direction
            input_3 = self.ghost_blue_next_direction
            input_4 = self.distance_ghost_blue_to_pac_man
            input_5 = self.harmless_mode_ghost_blue
            output_1, output_2, output_3, output_4 = self.ghost_intelligence(input_1, input_2, input_3, input_4, input_5)
            self.ghost_blue_pos = output_1
            self.ghost_blue_direction = output_2
            self.ghost_blue_next_direction = output_3
            self.distance_ghost_blue_to_pac_man = output_4
        
        # Fantasma laranja
        if self.ghost_orange_pos != [self.scale * 12, self.scale * 14.5]:
            input_1 = self.ghost_orange_pos
            input_2 = self.ghost_orange_direction
            input_3 = self.ghost_orange_next_direction
            input_4 = self.distance_ghost_orange_to_pac_man
            input_5 = self.harmless_mode_ghost_orange
            output_1, output_2, output_3, output_4 = self.ghost_intelligence(input_1, input_2, input_3, input_4, input_5)
            self.ghost_orange_pos = output_1
            self.ghost_orange_direction = output_2
            self.ghost_orange_next_direction = output_3
            self.distance_ghost_orange_to_pac_man = output_4
        
        # Fantasma rosa
        if self.ghost_pink_pos != [self.scale * 14, self.scale * 13]:
            input_1 = self.ghost_pink_pos
            input_2 = self.ghost_pink_direction
            input_3 = self.ghost_pink_next_direction
            input_4 = self.distance_ghost_pink_to_pac_man
            input_5 = self.harmless_mode_ghost_pink
            output_1, output_2, output_3, output_4 = self.ghost_intelligence(input_1, input_2, input_3, input_4, input_5)
            self.ghost_pink_pos = output_1
            self.ghost_pink_direction = output_2
            self.ghost_pink_next_direction = output_3
            self.distance_ghost_pink_to_pac_man = output_4
        
        # Fantasma vermelho
        if self.ghost_red_pos != [self.scale * 14, self.scale * 14.5]:
            input_1 = self.ghost_red_pos
            input_2 = self.ghost_red_direction
            input_3 = self.ghost_red_next_direction
            input_4 = self.distance_ghost_red_to_pac_man
            input_5 = self.harmless_mode_ghost_red
            output_1, output_2, output_3, output_4 = self.ghost_intelligence(input_1, input_2, input_3, input_4, input_5)
            self.ghost_red_pos = output_1
            self.ghost_red_direction = output_2
            self.ghost_red_next_direction = output_3
            self.distance_ghost_red_to_pac_man = output_4
    
    def moving_ghost_into_the_game(self, color):
        """Move fantasma para o jogo quando sai da posição inicial"""
        if color == 'blue':
            self.ghost_blue_pos = [self.scale * 13.1, self.scale * 10.6]
            self.ghost_blue_direction = self.random_direction_for_ghost()
            self.ghost_blue_next_direction = self.random_next_direction_for_ghost(self.ghost_blue_direction)
        elif color == 'orange':
            self.ghost_orange_pos = [self.scale * 13.1, self.scale * 10.6]
            self.ghost_orange_direction = self.random_direction_for_ghost()
            self.ghost_orange_next_direction = self.random_next_direction_for_ghost(self.ghost_orange_direction)
        elif color == 'pink':
            self.ghost_pink_pos = [self.scale * 13.1, self.scale * 10.6]
            self.ghost_pink_direction = self.random_direction_for_ghost()
            self.ghost_pink_next_direction = self.random_next_direction_for_ghost(self.ghost_pink_direction)
        elif color == 'red':
            self.ghost_red_pos = [self.scale * 13.1, self.scale * 10.6]
            self.ghost_red_direction = self.random_direction_for_ghost()
            self.ghost_red_next_direction = self.random_next_direction_for_ghost(self.ghost_red_direction)
    
    def ghost_manager(self):
        """Gerencia o estado dos fantasmas e modo inofensivo"""
        if self.harmless_mode:
            if self.sprite_frame == 60:
                self.harmless_mode_timer += 1
            if self.harmless_mode_timer == HARMLESS_MODE_DURATION:
                self.harmless_mode = False
                self.harmless_mode_ghost_blue = False
                self.harmless_mode_ghost_orange = False
                self.harmless_mode_ghost_pink = False
                self.harmless_mode_ghost_red = False
                self.harmless_mode_timer = 0
        
        # Renderizar fantasmas
        if self.harmless_mode_ghost_blue:
            self.ghost_render('harmless', self.ghost_blue_pos)
        else:
            self.ghost_render('blue', self.ghost_blue_pos)
        
        if self.harmless_mode_ghost_orange:
            self.ghost_render('harmless', self.ghost_orange_pos)
        else:
            self.ghost_render('orange', self.ghost_orange_pos)
        
        if self.harmless_mode_ghost_pink:
            self.ghost_render('harmless', self.ghost_pink_pos)
        else:
            self.ghost_render('pink', self.ghost_pink_pos)
        
        if self.harmless_mode_ghost_red:
            self.ghost_render('harmless', self.ghost_red_pos)
        else:
            self.ghost_render('red', self.ghost_red_pos)
        
        # Mover fantasmas para o jogo quando necessário
        if self.sprite_frame == 60:
            if self.ghost_blue_pos == [self.scale * 12, self.scale * 13]:
                self.moving_ghost_into_the_game('blue')
            elif self.ghost_orange_pos == [self.scale * 12, self.scale * 14.5]:
                self.moving_ghost_into_the_game('orange')
            elif self.ghost_pink_pos == [self.scale * 14, self.scale * 13]:
                self.moving_ghost_into_the_game('pink')
            elif self.ghost_red_pos == [self.scale * 14, self.scale * 14.5]:
                self.moving_ghost_into_the_game('red')
    
    def ghost_and_pacman_collider(self):
        """Verifica colisões entre Pacman e fantasmas"""
        # Colisão com fantasma azul
        if self.distance_ghost_blue_to_pac_man <= COLLISION_DISTANCE:
            if self.harmless_mode_ghost_blue:
                self.ghost_blue_pos = [self.scale * 12, self.scale * 13]
                self.harmless_mode_ghost_blue = False
                self.distance_ghost_blue_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_blue_pos)
                self.score += GHOST_POINTS
            else:
                if self.end_game == False:
                    self.sprite_frame = 0
                    self.sprite_speed = 1
                    self.lives -= 1
                self.end_game = True
        
        # Colisão com fantasma laranja
        elif self.distance_ghost_orange_to_pac_man <= COLLISION_DISTANCE:
            if self.harmless_mode_ghost_orange:
                self.ghost_orange_pos = [self.scale * 12, self.scale * 14.5]
                self.harmless_mode_ghost_orange = False
                self.distance_ghost_orange_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_orange_pos)
                self.score += GHOST_POINTS
            else:
                if self.end_game == False:
                    self.sprite_frame = 0
                    self.sprite_speed = 1
                    self.lives -= 1
                self.end_game = True
        
        # Colisão com fantasma rosa
        elif self.distance_ghost_pink_to_pac_man <= COLLISION_DISTANCE:
            if self.harmless_mode_ghost_pink:
                self.ghost_pink_pos = [self.scale * 14, self.scale * 13]
                self.harmless_mode_ghost_pink = False
                self.distance_ghost_pink_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_pink_pos)
                self.score += GHOST_POINTS
            else:
                if self.end_game == False:
                    self.sprite_frame = 0
                    self.sprite_speed = 1
                    self.lives -= 1
                self.end_game = True
        
        # Colisão com fantasma vermelho
        elif self.distance_ghost_red_to_pac_man <= COLLISION_DISTANCE:
            if self.harmless_mode_ghost_red:
                self.ghost_red_pos = [self.scale * 14, self.scale * 14.5]
                self.harmless_mode_ghost_red = False
                self.distance_ghost_red_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_red_pos)
                self.score += GHOST_POINTS
            else:
                if self.end_game == False:
                    self.sprite_frame = 0
                    self.sprite_speed = 1
                    self.lives -= 1
                self.end_game = True
    
    def restart_ghost_collision(self):
        """Reinicia após colisão com fantasma"""
        if self.sprite_frame == 60 and self.end_game == True and self.lives > -1:
            self.end_game = False
            self.harmless_mode = False
            self.harmless_mode_timer = 0
            self.harmless_mode_ghost_blue = False
            self.harmless_mode_ghost_orange = False
            self.harmless_mode_ghost_pink = False
            self.harmless_mode_ghost_red = False
            self.pac_man_pos = [self.scale * 13.1, self.scale * 22.6]
            self.pac_man_direction = [self.scale/16, 0]
            self.pac_man_next_direction = [self.scale/16, 0]
            self.ghost_blue_pos = [self.scale * 12, self.scale * 13]
            self.ghost_orange_pos = [self.scale * 12, self.scale * 14.5]
            self.ghost_pink_pos = [self.scale * 14, self.scale * 13]
            self.ghost_red_pos = [self.scale * 14, self.scale * 14.5]
            self.distance_ghost_blue_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_blue_pos)
            self.distance_ghost_orange_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_orange_pos)
            self.distance_ghost_pink_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_pink_pos)
            self.distance_ghost_red_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_red_pos)
            self.sprite_speed = SPRITE_SPEED
            self.end_game = False
    
    def collect_all_dots(self):
        """Verifica se todos os pontos foram coletados"""
        count = 0
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == DOT or self.map[y][x] == POWER_PELLET:
                    count += 1
        if count == 0:
            self.end_game = False
            self.harmless_mode = False
            self.harmless_mode_timer = 0
            self.harmless_mode_ghost_blue = False
            self.harmless_mode_ghost_orange = False
            self.harmless_mode_ghost_pink = False
            self.harmless_mode_ghost_red = False
            self.pac_man_pos = [self.scale * 13.1, self.scale * 22.6]
            self.pac_man_direction = [self.scale/16, 0]
            self.pac_man_next_direction = [self.scale/16, 0]
            self.ghost_blue_pos = [self.scale * 12, self.scale * 13]
            self.ghost_orange_pos = [self.scale * 12, self.scale * 14.5]
            self.ghost_pink_pos = [self.scale * 14, self.scale * 13]
            self.ghost_red_pos = [self.scale * 14, self.scale * 14.5]
            self.distance_ghost_blue_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_blue_pos)
            self.distance_ghost_orange_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_orange_pos)
            self.distance_ghost_pink_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_pink_pos)
            self.distance_ghost_red_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_red_pos)
            self.sprite_speed = SPRITE_SPEED
            self.end_game = False
            self.map = [row[:] for row in GAME_MAP]
    
    def scoreboard(self):
        """Desenha a pontuação e vidas"""
        score_text = self.font.render(f'Score: {str(self.score)}', 1, self.white)
        lives_text = self.font.render(f'Lives: {str(max(self.lives, 0))}X', 1, self.white)
        x_score_pos = (self.window.get_width() / 2) - (score_text.get_width() / 2)
        y_score_pos = self.scale * 30.75
        x_lives_pos = (self.window.get_width() / 2) - (lives_text.get_width() / 2)
        y_lives_pos = self.scale * 33
        self.window.blit(score_text, (x_score_pos, y_score_pos))
        self.window.blit(lives_text, (x_lives_pos, y_lives_pos))
        
        # Mostrar status do controle
        self._draw_controller_status()
        
        if self.lives == -1:
            end_text = self.font.render('game', 1, self.white)
            game_text = self.font.render('over', 1, self.white)
            x_end_pos = (self.window.get_width() / 2) - (end_text.get_width() / 2)
            y_end_pos = self.scale * 12.25
            x_game_pos = (self.window.get_width() / 2) - (game_text.get_width() / 2)
            y_game_pos = self.scale * 13.75
            self.window.blit(end_text, (x_end_pos, y_end_pos))
            self.window.blit(game_text, (x_game_pos, y_game_pos))
    
    def _draw_controller_status(self):
        """Desenha o status dos controles conectados"""
        # Método vazio - controles funcionam sem feedback visual
        pass
    
    def _show_start_countdown(self):
        """Mostra contagem regressiva de 2 segundos antes de iniciar o jogo"""
        import time
        
        # Criar fonte maior para a contagem regressiva
        countdown_font = pg.font.SysFont("Courier New", self.scale * 4, bold=True)
        
        for i in range(3, 0, -1):
            # Limpar a tela
            self.clear_window()
            
            # Desenhar o tabuleiro
            self.board()
            
            # Desenhar texto da contagem regressiva
            countdown_text = countdown_font.render(str(i), 1, self.white)
            x_pos = (self.window.get_width() / 2) - (countdown_text.get_width() / 2)
            y_pos = (self.window.get_height() / 2) - (countdown_text.get_height() / 2)
            self.window.blit(countdown_text, (x_pos, y_pos))
            
            # Atualizar a tela
            pg.display.update()
            
            # Pausar por 1 segundo
            time.sleep(1)
        
        # Mostrar "GO!" por 0.5 segundos
        go_text = countdown_font.render("GO!", 1, self.white)
        x_pos = (self.window.get_width() / 2) - (go_text.get_width() / 2)
        y_pos = (self.window.get_height() / 2) - (go_text.get_height() / 2)
        
        self.clear_window()
        self.board()
        self.window.blit(go_text, (x_pos, y_pos))
        pg.display.update()
        time.sleep(0.5)
    
    def restart(self):
        """Reinicia o jogo"""
        self.sprite_frame = 0
        self.sprite_speed = SPRITE_SPEED
        self.score = 0
        self.lives = 5
        self.end_game = False
        self.harmless_mode = False
        self.harmless_mode_timer = 0
        self.harmless_mode_ghost_blue = False
        self.harmless_mode_ghost_orange = False
        self.harmless_mode_ghost_pink = False
        self.harmless_mode_ghost_red = False
        self.pac_man_pos = [self.scale * 13.1, self.scale * 22.6]
        self.pac_man_direction = [self.scale/16, 0]
        self.pac_man_next_direction = [self.scale/16, 0]
        self.ghost_blue_pos = [self.scale * 12, self.scale * 13]
        self.ghost_orange_pos = [self.scale * 12, self.scale * 14.5]
        self.ghost_pink_pos = [self.scale * 14, self.scale * 13]
        self.ghost_red_pos = [self.scale * 14, self.scale * 14.5]
        self.ghost_blue_direction = [0, 0]
        self.ghost_orange_direction = [0, 0]
        self.ghost_pink_direction = [0, 0]
        self.ghost_red_direction = [0, 0]
        self.ghost_blue_next_direction = [0, 0]
        self.ghost_orange_next_direction = [0, 0]
        self.ghost_pink_next_direction = [0, 0]
        self.ghost_red_next_direction = [0, 0]
        self.distance_ghost_blue_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_blue_pos)
        self.distance_ghost_orange_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_orange_pos)
        self.distance_ghost_pink_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_pink_pos)
        self.distance_ghost_red_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_red_pos)
        self.map = [row[:] for row in GAME_MAP]
    
    def run(self):
        """Loop principal do jogo"""
        # Pausa inicial de 2 segundos com contagem regressiva
        self._show_start_countdown()
        
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    self.move(pg.key.name(event.key))
                    if pg.key.name(event.key) == 'escape':
                        running = False
            
            # Atualizar jogo
            self.clock.tick(FPS)
            self.clear_window()
            self.board()
            self.animation_step()
            self.player()
            self.ghost()
            self.collect_dots()
            self.ghost_manager()
            self.ghost_and_pacman_collider()
            self.scoreboard()
            self.restart_ghost_collision()
            self.collect_all_dots()
            
            # Processar entrada dos controles
            self.handle_controller_input()
            
            pg.display.update()
        
        # Limpar recursos dos controles
        self.controller_manager.cleanup()
        
        pg.quit()
        quit()
