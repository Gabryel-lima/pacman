"""
Classe principal do jogo Pac-Man
Baseada na lógica do arquivo Pac_Man.py
"""

import pygame as pg
import random
import os
from .constants import *
from .controller import ControllerManager, ControllerType
from .menu import MenuSelector


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
        
        # Modo de jogo selecionado
        self.game_mode = "Player 1"
        
        # Posições e direções do Pacman (calculadas dinamicamente)
        self.pac_man_pos = [scale * 13.1, scale * 22.6]
        self.pac_man_direction = [scale/16, 0]
        self.pac_man_next_direction = [scale/16, 0]
        
        # Posições e direções para múltiplos jogadores
        self.pac_man_2_pos = [scale * 12.1, scale * 22.6]  # Player 2 - à esquerda
        self.pac_man_2_direction = [0, 0]
        self.pac_man_2_next_direction = [0, 0]
        
        self.pac_man_3_pos = [scale * 14.1, scale * 22.6]  # Player 3 - à direita
        self.pac_man_3_direction = [0, 0]
        self.pac_man_3_next_direction = [0, 0]
        
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
        
        # Mapeamento de controles para jogadores
        self.player_controllers = {
            1: 0,  # Player 1 usa controle 0
            2: 1,  # Player 2 usa controle 1 (se disponível)
            3: 2   # Player 3 usa controle 2 (se disponível)
        }
    
    def _load_pacman_sprites(self):
        """Carrega os sprites do Pacman para todos os players"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_dir = os.path.join(base_dir, "img")
        
        # Cores dos players
        player_colors = {
            1: PLAYER_1_COLOR,  # Amarelo
            2: PLAYER_2_COLOR,  # Verde
            3: PLAYER_3_COLOR   # Rosa
        }
        
        # Carregar sprites para cada player
        for player_num in range(1, 4):
            pacman_sprites = []
            for i in range(1, 18):
                sprite_path = os.path.join(img_dir, f"Pac_Man_{i}.png")
                if os.path.exists(sprite_path):
                    sprite = pg.image.load(sprite_path)
                    scaled_sprite = pg.transform.scale(sprite, (self.scale * 1.3, self.scale * 1.3))
                    
                    # Aplicar cor do player ao sprite
                    colored_sprite = self._colorize_sprite(scaled_sprite, player_colors[player_num])
                    pacman_sprites.append(colored_sprite)
                else:
                    # Criar sprite placeholder com cor do player
                    placeholder = pg.Surface((self.scale * 1.3, self.scale * 1.3))
                    placeholder.fill(player_colors[player_num])
                    pacman_sprites.append(placeholder)
            
            # Atribuir sprites às variáveis específicas do player
            for i, sprite in enumerate(pacman_sprites):
                setattr(self, f"pac_man_{player_num}_{i+1}", sprite)
    
    def _colorize_sprite(self, sprite, color):
        """Aplica uma cor a um sprite mantendo a transparência"""
        # Criar uma cópia do sprite
        colored_sprite = sprite.copy()
        
        # Converter para formato com alpha se necessário
        if colored_sprite.get_flags() & pg.SRCALPHA:
            # Sprite já tem canal alpha
            pass
        else:
            # Converter para formato com alpha
            colored_sprite = colored_sprite.convert_alpha()
        
        # Aplicar a cor pixel por pixel
        for x in range(colored_sprite.get_width()):
            for y in range(colored_sprite.get_height()):
                pixel = colored_sprite.get_at((x, y))
                if pixel[3] > 0:  # Se o pixel não é transparente
                    # Aplicar a cor mantendo a intensidade original
                    new_pixel = (
                        int(pixel[0] * color[0] / 255),
                        int(pixel[1] * color[1] / 255),
                        int(pixel[2] * color[2] / 255),
                        pixel[3]  # Manter alpha
                    )
                    colored_sprite.set_at((x, y), new_pixel)
        
        return colored_sprite
    
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
        """Processa entrada do teclado para movimento dos Pacmans"""
        if key == 'r':
            self.restart()
        # Player 1 (WASD)
        elif key == 'w':
            self._set_direction('up', 1)
        elif key == 'a':
            self._set_direction('left', 1)
        elif key == 's':
            self._set_direction('down', 1)
        elif key == 'd':
            self._set_direction('right', 1)
        # Player 2 (Arrow Keys)
        elif key == 'up':
            self._set_direction('up', 2)
        elif key == 'left':
            self._set_direction('left', 2)
        elif key == 'down':
            self._set_direction('down', 2)
        elif key == 'right':
            self._set_direction('right', 2)
        # Player 3 (IJKL)
        elif key == 'i':
            self._set_direction('up', 3)
        elif key == 'j':
            self._set_direction('left', 3)
        elif key == 'k':
            self._set_direction('down', 3)
        elif key == 'l':
            self._set_direction('right', 3)
    
    def _set_direction(self, direction, player_num=1):
        """Define a direção do Pacman baseada no input"""
        # Selecionar variáveis baseadas no jogador
        if player_num == 1:
            current_dir = self.pac_man_direction
            next_dir = self.pac_man_next_direction
        elif player_num == 2:
            current_dir = self.pac_man_2_direction
            next_dir = self.pac_man_2_next_direction
        elif player_num == 3:
            current_dir = self.pac_man_3_direction
            next_dir = self.pac_man_3_next_direction
        else:
            return
        
        if direction == 'up':
            if current_dir[0] == 0 and current_dir[1] > 0:
                current_dir[0] = 0
                current_dir[1] = -self.scale/16
                next_dir[0] = 0
                next_dir[1] = -self.scale/16
            elif current_dir[0] != 0 and current_dir[1] == 0:
                next_dir[0] = 0
                next_dir[1] = -self.scale/16
            elif current_dir[0] == 0 and current_dir[1] == 0:  # Se parado, pode começar a se mover
                current_dir[0] = 0
                current_dir[1] = -self.scale/16
                next_dir[0] = 0
                next_dir[1] = -self.scale/16
        elif direction == 'left':
            if current_dir[0] > 0 and current_dir[1] == 0:
                current_dir[0] = -self.scale/16
                current_dir[1] = 0
                next_dir[0] = -self.scale/16
                next_dir[1] = 0
            elif current_dir[0] == 0 and current_dir[1] != 0:
                next_dir[0] = -self.scale/16
                next_dir[1] = 0
            elif current_dir[0] == 0 and current_dir[1] == 0:  # Se parado, pode começar a se mover
                current_dir[0] = -self.scale/16
                current_dir[1] = 0
                next_dir[0] = -self.scale/16
                next_dir[1] = 0
        elif direction == 'down':
            if current_dir[0] == 0 and current_dir[1] < 0:
                current_dir[0] = 0
                current_dir[1] = self.scale/16
                next_dir[0] = 0
                next_dir[1] = self.scale/16
            elif current_dir[0] != 0 and current_dir[1] == 0:
                next_dir[0] = 0
                next_dir[1] = self.scale/16
            elif current_dir[0] == 0 and current_dir[1] == 0:  # Se parado, pode começar a se mover
                current_dir[0] = 0
                current_dir[1] = self.scale/16
                next_dir[0] = 0
                next_dir[1] = self.scale/16
        elif direction == 'right':
            if current_dir[0] < 0 and current_dir[1] == 0:
                current_dir[0] = self.scale/16
                current_dir[1] = 0
                next_dir[0] = self.scale/16
                next_dir[1] = 0
            elif current_dir[0] == 0 and current_dir[1] != 0:
                next_dir[0] = self.scale/16
                next_dir[1] = 0
            elif current_dir[0] == 0 and current_dir[1] == 0:  # Se parado, pode começar a se mover
                current_dir[0] = self.scale/16
                current_dir[1] = 0
                next_dir[0] = self.scale/16
                next_dir[1] = 0
    
    def handle_controller_input(self):
        """Processa entrada dos controles para todos os jogadores ativos"""
        if not self.controller_connected:
            return
        
        # Atualizar estado dos controles
        self.controller_manager.update()
        
        # Verificar se ainda há controles conectados
        if self.controller_manager.get_controller_count() == 0:
            self.controller_connected = False
            return
        
        # Player 1 (sempre ativo)
        controller_1 = self.player_controllers[1]
        if self.controller_manager.is_controller_connected(controller_1):
            direction, has_input = self.controller_manager.get_movement_input(controller_1)
            if has_input:
                self._set_direction(direction, 1)
            
            special_buttons = self.controller_manager.get_special_buttons(controller_1)
            if special_buttons.get('restart', False):
                self.restart()
        
        # Player 2 (se modo Player 2 ou Player 3)
        if self.game_mode in ["Player 2", "Player 3"]:
            controller_2 = self.player_controllers[2]
            if self.controller_manager.is_controller_connected(controller_2):
                direction, has_input = self.controller_manager.get_movement_input(controller_2)
                if has_input:
                    self._set_direction(direction, 2)
        
        # Player 3 (se modo Player 3)
        if self.game_mode == "Player 3":
            controller_3 = self.player_controllers[3]
            if self.controller_manager.is_controller_connected(controller_3):
                direction, has_input = self.controller_manager.get_movement_input(controller_3)
                if has_input:
                    self._set_direction(direction, 3)
    
    def board(self):
        """Desenha o tabuleiro do jogo"""
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == WALL:
                    pg.draw.rect(self.window, self.blue, (x * self.scale, y * self.scale, self.scale, self.scale))
                #if self.map[y][x] == TUNNEL:
                #    pg.draw.rect(self.window, self.white, (x * self.scale, y * self.scale, self.scale, self.scale))
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
    
    def player_rotation(self, image, direction=None):
        """Rotaciona a imagem do Pacman baseada na direção"""
        if direction is None:
            direction = self.pac_man_direction
            
        x_dir = direction[0]
        y_dir = direction[1]
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
        """Coleta pontos e power pellets para todos os jogadores ativos"""
        # Lista de posições dos jogadores ativos
        active_players = [self.pac_man_pos]  # Player 1 sempre ativo
        
        # Adicionar Player 2 se estiver ativo
        if self.game_mode in ["Player 2", "Player 3"]:
            active_players.append(self.pac_man_2_pos)
        
        # Adicionar Player 3 se estiver ativo
        if self.game_mode == "Player 3":
            active_players.append(self.pac_man_3_pos)
        
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == DOT:
                    x_dot = (x * self.scale) + (self.scale / 4)
                    y_dot = (y * self.scale) + (self.scale / 4)
                    radius = self.scale / 5
                    
                    # Verificar colisão com todos os jogadores ativos
                    for player_pos in active_players:
                        x_pac_man = player_pos[0] + (self.scale * 0.65)
                        y_pac_man = player_pos[1] + (self.scale * 0.65)
                        if x_pac_man >= x_dot - radius and x_pac_man <= x_dot + radius and y_pac_man >= y_dot - radius and y_pac_man <= y_dot + radius:
                            self.map[y][x] = EMPTY
                            self.score += DOT_POINTS
                            break  # Sair do loop de jogadores se coletou o ponto
                
                if self.map[y][x] == POWER_PELLET:
                    x_dot = (x * self.scale) + (self.scale / 4)
                    y_dot = (y * self.scale) + (self.scale / 4)
                    radius = self.scale / 2
                    
                    # Verificar colisão com todos os jogadores ativos
                    for player_pos in active_players:
                        x_pac_man = player_pos[0] + (self.scale * 0.65)
                        y_pac_man = player_pos[1] + (self.scale * 0.65)
                        if x_pac_man >= x_dot - radius and x_pac_man <= x_dot + radius and y_pac_man >= y_dot - radius and y_pac_man <= y_dot + radius:
                            self.map[y][x] = EMPTY
                            self.score += POWER_PELLET_POINTS
                            self.harmless_mode = True
                            self.harmless_mode_ghost_blue = True
                            self.harmless_mode_ghost_orange = True
                            self.harmless_mode_ghost_pink = True
                            self.harmless_mode_ghost_red = True
                            break  # Sair do loop de jogadores se coletou o power pellet
    
    def pacman_tunnel(self, position):
        """Implementa túneis laterais"""
        x_pos = position[0]
        y_pos = position[1]
        if position[0] >= self.scale * 27.5:
            x_pos = 0 - (self.scale * 1.3)
        elif position[0] <= -(self.scale * 1.3):
            x_pos = self.scale * 27.5
        return [x_pos, y_pos]
    
    def _render_pacman(self, pos, direction, is_dead=False, player_num=1):
        """Renderiza um Pacman individual com cor específica do player"""
        x = pos[0]
        y = pos[1]
        
        if is_dead:
            # Animação de morte
            if self.sprite_frame <= 5:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_6"), direction), (x, y))
            elif self.sprite_frame <= 10:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_7"), direction), (x, y))
            elif self.sprite_frame <= 15:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_8"), direction), (x, y))
            elif self.sprite_frame <= 20:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_9"), direction), (x, y))
            elif self.sprite_frame <= 25:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_10"), direction), (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_11"), direction), (x, y))
            elif self.sprite_frame <= 35:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_12"), direction), (x, y))
            elif self.sprite_frame <= 40:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_13"), direction), (x, y))
            elif self.sprite_frame <= 45:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_14"), direction), (x, y))
            elif self.sprite_frame <= 50:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_15"), direction), (x, y))
            elif self.sprite_frame <= 55:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_16"), direction), (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_17"), direction), (x, y))
        else:
            # Animação normal
            if self.sprite_frame <= 6:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_1"), direction), (x, y))
            elif self.sprite_frame <= 12:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_1"), direction), (x, y))
            elif self.sprite_frame <= 18:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_2"), direction), (x, y))
            elif self.sprite_frame <= 24:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_3"), direction), (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_4"), direction), (x, y))
            elif self.sprite_frame <= 36:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_5"), direction), (x, y))
            elif self.sprite_frame <= 42:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_4"), direction), (x, y))
            elif self.sprite_frame <= 48:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_3"), direction), (x, y))
            elif self.sprite_frame <= 54:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_2"), direction), (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.player_rotation(getattr(self, f"pac_man_{player_num}_1"), direction), (x, y))

    def player(self):
        """Desenha e atualiza os Pacmans baseado no modo de jogo"""
        # Player 1 (sempre ativo)
        self.pac_man_direction, self.pac_man_next_direction = self.turning_corner(self.pac_man_pos, self.pac_man_direction, self.pac_man_next_direction)
        self.pac_man_pos = self.collider(self.pac_man_pos, self.pac_man_direction)
        self.pac_man_pos = self.pacman_tunnel(self.pac_man_pos)
        self._render_pacman(self.pac_man_pos, self.pac_man_direction, self.end_game, 1)
        
        # Player 2 (se modo Player 2 ou Player 3)
        if self.game_mode in ["Player 2", "Player 3"]:
            self.pac_man_2_direction, self.pac_man_2_next_direction = self.turning_corner(self.pac_man_2_pos, self.pac_man_2_direction, self.pac_man_2_next_direction)
            self.pac_man_2_pos = self.collider(self.pac_man_2_pos, self.pac_man_2_direction)
            self.pac_man_2_pos = self.pacman_tunnel(self.pac_man_2_pos)
            self._render_pacman(self.pac_man_2_pos, self.pac_man_2_direction, False, 2)
        
        # Player 3 (se modo Player 3)
        if self.game_mode == "Player 3":
            self.pac_man_3_direction, self.pac_man_3_next_direction = self.turning_corner(self.pac_man_3_pos, self.pac_man_3_direction, self.pac_man_3_next_direction)
            self.pac_man_3_pos = self.collider(self.pac_man_3_pos, self.pac_man_3_direction)
            self.pac_man_3_pos = self.pacman_tunnel(self.pac_man_3_pos)
            self._render_pacman(self.pac_man_3_pos, self.pac_man_3_direction, False, 3)
    
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
    
    def check_rectangular_collision(self, pacman_pos, ghost_pos):
        """Verifica colisão retangular mais precisa entre Pacman e fantasma"""
        # Área de colisão reduzida para maior precisão
        collision_margin = self.scale * 0.4  # Margem menor para colisão mais precisa
        
        # Posições centrais dos sprites
        pacman_center_x = pacman_pos[0] + (self.scale * 0.65)
        pacman_center_y = pacman_pos[1] + (self.scale * 0.65)
        ghost_center_x = ghost_pos[0] + (self.scale * 0.65)
        ghost_center_y = ghost_pos[1] + (self.scale * 0.65)
        
        # Verificar se as áreas de colisão se sobrepõem
        pacman_left = pacman_center_x - collision_margin
        pacman_right = pacman_center_x + collision_margin
        pacman_top = pacman_center_y - collision_margin
        pacman_bottom = pacman_center_y + collision_margin
        
        ghost_left = ghost_center_x - collision_margin
        ghost_right = ghost_center_x + collision_margin
        ghost_top = ghost_center_y - collision_margin
        ghost_bottom = ghost_center_y + collision_margin
        
        # Verificar sobreposição retangular
        return (pacman_left < ghost_right and 
                pacman_right > ghost_left and 
                pacman_top < ghost_bottom and 
                pacman_bottom > ghost_top)

    def _check_pacman_ghost_collision(self, pacman_pos):
        """Verifica colisão entre um Pacman específico e todos os fantasmas"""
        # Colisão com fantasma azul
        if self.check_rectangular_collision(pacman_pos, self.ghost_blue_pos):
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
            return True
        
        # Colisão com fantasma laranja
        elif self.check_rectangular_collision(pacman_pos, self.ghost_orange_pos):
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
            return True
        
        # Colisão com fantasma rosa
        elif self.check_rectangular_collision(pacman_pos, self.ghost_pink_pos):
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
            return True
        
        # Colisão com fantasma vermelho
        elif self.check_rectangular_collision(pacman_pos, self.ghost_red_pos):
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
            return True
        
        return False

    def ghost_and_pacman_collider(self):
        """Verifica colisões entre todos os Pacmans ativos e fantasmas"""
        # Player 1 (sempre ativo)
        if self._check_pacman_ghost_collision(self.pac_man_pos):
            return
        
        # Player 2 (se modo Player 2 ou Player 3)
        if self.game_mode in ["Player 2", "Player 3"]:
            if self._check_pacman_ghost_collision(self.pac_man_2_pos):
                return
        
        # Player 3 (se modo Player 3)
        if self.game_mode == "Player 3":
            if self._check_pacman_ghost_collision(self.pac_man_3_pos):
                return
    
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
        """Desenha a pontuação, vidas e modo de jogo"""
        score_text = self.font.render(f'Score: {str(self.score)}', 1, self.white)
        lives_text = self.font.render(f'Lives: {str(max(self.lives, 0))}X', 1, self.white)
        mode_text = self.font.render(f'Mode: {self.game_mode}', 1, self.white)
        
        x_score_pos = (self.window.get_width() / 2) - (score_text.get_width() / 2)
        y_score_pos = self.scale * 30.75
        x_lives_pos = (self.window.get_width() / 2) - (lives_text.get_width() / 2)
        y_lives_pos = self.scale * 33
        x_mode_pos = (self.window.get_width() / 2) - (mode_text.get_width() / 2)
        y_mode_pos = self.scale * 35.25
        
        self.window.blit(score_text, (x_score_pos, y_score_pos))
        self.window.blit(lives_text, (x_lives_pos, y_lives_pos))
        self.window.blit(mode_text, (x_mode_pos, y_mode_pos))
        
        # Mostrar status dos controles
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
        """Desenha o status dos controles e teclas para jogadores ativos"""
        controller_count = self.controller_manager.get_controller_count()
        
        # Mostrar instruções de teclado para jogadores ativos
        y_offset = self.scale * 37
        
        # Player 1 (sempre ativo)
        player1_text = "P1: WASD"
        player1_display = self.font.render(player1_text, 1, self.white)
        player1_x = (self.window.get_width() / 2) - (player1_display.get_width() / 2)
        self.window.blit(player1_display, (player1_x, y_offset))
        y_offset += self.scale * 0.8
        
        # Player 2 (se modo Player 2 ou Player 3)
        if self.game_mode in ["Player 2", "Player 3"]:
            player2_text = "P2: Arrow Keys"
            player2_display = self.font.render(player2_text, 1, self.white)
            player2_x = (self.window.get_width() / 2) - (player2_display.get_width() / 2)
            self.window.blit(player2_display, (player2_x, y_offset))
            y_offset += self.scale * 0.8
        
        # Player 3 (se modo Player 3)
        if self.game_mode == "Player 3":
            player3_text = "P3: IJKL"
            player3_display = self.font.render(player3_text, 1, self.white)
            player3_x = (self.window.get_width() / 2) - (player3_display.get_width() / 2)
            self.window.blit(player3_display, (player3_x, y_offset))
            y_offset += self.scale * 0.8
        
        # Mostrar controles USB se conectados
        if controller_count > 0:
            controllers_text = f"Controllers: {controller_count}"
            controller_display = self.font.render(controllers_text, 1, (0, 255, 255))  # Cor ciano para destacar
            controller_x = (self.window.get_width() / 2) - (controller_display.get_width() / 2)
            y_offset += self.scale * 0.4  # Espaço extra antes dos controles
            
            self.window.blit(controller_display, (controller_x, y_offset))
            y_offset += self.scale * 0.8
            
            # Mostrar mapeamento de controles para jogadores ativos
            for player_num in [1, 2, 3]:
                # Verificar se o jogador está ativo no modo atual
                is_active = False
                if player_num == 1:
                    is_active = True
                elif player_num == 2 and self.game_mode in ["Player 2", "Player 3"]:
                    is_active = True
                elif player_num == 3 and self.game_mode == "Player 3":
                    is_active = True
                
                if is_active:
                    controller_index = self.player_controllers[player_num]
                    if self.controller_manager.is_controller_connected(controller_index):
                        controller_name = self.controller_manager.get_controller_name(controller_index)
                        # Truncar nome se muito longo
                        if len(controller_name) > 15:
                            controller_name = controller_name[:12] + "..."
                        
                        player_text = f"P{player_num} Controller: {controller_name}"
                        player_display = self.font.render(player_text, 1, (0, 255, 255))
                        player_x = (self.window.get_width() / 2) - (player_display.get_width() / 2)
                        player_y = y_offset
                        
                        self.window.blit(player_display, (player_x, player_y))
                        y_offset += self.scale * 0.8
    
    def show_mode_selection(self):
        """Mostra o menu de seleção de modo"""
        menu = MenuSelector(self.scale)
        selected_mode = menu.run_menu_loop(self.window)
        
        if selected_mode == 'quit':
            return False
        else:
            self.game_mode = selected_mode
            return True
    
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
        go_text = countdown_font.render("GO", 1, self.white)
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
        self.pac_man_2_pos = [self.scale * 12.1, self.scale * 22.6]
        self.pac_man_2_direction = [0, 0]
        self.pac_man_2_next_direction = [0, 0]
        self.pac_man_3_pos = [self.scale * 14.1, self.scale * 22.6]
        self.pac_man_3_direction = [0, 0]
        self.pac_man_3_next_direction = [0, 0]
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
        self.game_mode = "Player 1"  # Reset para modo padrão
    
    def run(self):
        """Loop principal do jogo"""
        # Mostrar menu de seleção de modo
        if not self.show_mode_selection():
            return
        
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
