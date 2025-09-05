"""
Classe principal do jogo Pac-Man
Conversão de C++/SDL2 para Python/pygame-ce
"""

import pygame
import os
import sys
from typing import List, Optional, Tuple
from .entities import Scene, Pacman, Phantom
from .constants import *

class Game:
    """Classe principal que gerencia o jogo Pac-Man"""
    
    def __init__(self):
        """Inicializa o jogo"""
        self.screen: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.running = False
        self.game_mode = STARTING
        
        # Sprites/texturas
        self.pacman_sprites: List[pygame.Surface] = []
        self.phantom_sprites: List[pygame.Surface] = []
        self.scene_sprites: List[pygame.Surface] = []
        self.game_start_sprite: Optional[pygame.Surface] = None
        self.game_over_sprite: Optional[pygame.Surface] = None
        self.game_won_sprite: Optional[pygame.Surface] = None
        
        # Objetos do jogo
        self.scene: Optional[Scene] = None
        self.pacman: Optional[Pacman] = None
        self.phantoms: List[Optional[Phantom]] = [None, None, None, None]
        
        # Controle de tempo para movimento
        self.last_update = 0
    
    def init(self) -> bool:
        """Inicializa pygame e carrega recursos"""
        try:
            pygame.init()
            
            # Criar janela
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("PACMAN - pygame-ce")
            
            # Criar clock para controle de FPS
            self.clock = pygame.time.Clock()
            
            # Carregar sprites
            if not self._load_sprites():
                return False
            
            return True
            
        except Exception as e:
            print(f"Erro ao inicializar pygame: {e}")
            return False
    
    def _load_sprites(self) -> bool:
        """Carrega todos os sprites do jogo"""
        try:
            # Carregar sprites do Pacman (12 sprites - 4 direções x 3 animações)
            for i in range(1, 13):
                sprite_path = f"images/pacman-{i}.png"
                if os.path.exists(sprite_path):
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, (CELL_SIZE, CELL_SIZE))
                    self.pacman_sprites.append(sprite)
                else:
                    print(f"Sprite não encontrado: {sprite_path}")
                    return False
            
            # Carregar sprites dos fantasmas (24 sprites)
            for i in range(1, 25):
                sprite_path = f"images/phantom-{i}.png"
                if os.path.exists(sprite_path):
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, (CELL_SIZE, CELL_SIZE))
                    self.phantom_sprites.append(sprite)
                else:
                    print(f"Sprite não encontrado: {sprite_path}")
                    return False
            
            # Carregar sprites do cenário
            scene_files = [
                "empty.png", "coin.png", "power.png", "vertical.png", "horizontal.png",
                "curve-base-left.png", "curve-base-right.png", "curve-top-left.png", 
                "curve-top-right.png", "end-left.png", "end-right.png", "end-base.png", "end-top.png"
            ]
            
            for filename in scene_files:
                sprite_path = f"images/{filename}"
                if os.path.exists(sprite_path):
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, (CELL_SIZE, CELL_SIZE))
                    self.scene_sprites.append(sprite)
                else:
                    print(f"Sprite não encontrado: {sprite_path}")
                    return False
            
            # Carregar sprites de interface
            interface_files = [
                ("images/game-start.png", "game_start_sprite"),
                ("images/game-over.png", "game_over_sprite"),
                ("images/you-won.png", "game_won_sprite")
            ]
            
            for filepath, attr_name in interface_files:
                if os.path.exists(filepath):
                    sprite = pygame.image.load(filepath).convert_alpha()
                    sprite = pygame.transform.scale(sprite, (WINDOW_SIZE, WINDOW_SIZE))
                    setattr(self, attr_name, sprite)
                else:
                    print(f"Sprite não encontrado: {filepath}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"Erro ao carregar sprites: {e}")
            return False
    
    def run(self):
        """Loop principal do jogo"""
        self.running = True
        
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(FPS)
    
    def _handle_events(self):
        """Processa eventos do pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.game_mode in [STARTING, FAILED, WON]:
                        if self.game_mode == STARTING:
                            self.game_mode = PLAYING
                            self._start_game()
                        else:
                            self.game_mode = STARTING
                
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                
                elif self.pacman and self.game_mode == PLAYING:
                    if event.key == pygame.K_RIGHT:
                        self.pacman.set_next_direction(RIGHT)
                    elif event.key == pygame.K_LEFT:
                        self.pacman.set_next_direction(LEFT)
                    elif event.key == pygame.K_UP:
                        self.pacman.set_next_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.set_next_direction(DOWN)
    
    def _update(self):
        """Atualiza a lógica do jogo"""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_update > MOVEMENT_DELAY and self.game_mode == PLAYING:
            if self.pacman and self.scene:
                if self.pacman.is_alive():
                    if self.scene.all_coins_collected():
                        self.game_mode = WON
                    else:
                        # Mover Pacman
                        self.pacman.move(self.scene)
                        
                        # Mover fantasmas
                        for phantom in self.phantoms:
                            if phantom:
                                phantom.move(self.scene)
                                
                                # Verificar colisão com Pacman
                                if phantom.x == self.pacman.x and phantom.y == self.pacman.y:
                                    if self.pacman.power > 0:
                                        # Pacman come o fantasma
                                        phantom.status = DEAD
                                        self.pacman.points += 200
                                    else:
                                        # Fantasma mata Pacman
                                        self.pacman.life = 0
                else:
                    self.game_mode = FAILED
            
            self.last_update = current_time
    
    def _render(self):
        """Renderiza o jogo na tela"""
        # Limpar tela
        self.screen.fill((0, 0, 0))
        
        # Desenhar cenário
        if self.scene:
            self._draw_scene()
        
        # Desenhar Pacman
        if self.pacman:
            self._draw_pacman()
        
        # Desenhar fantasmas
        for phantom in self.phantoms:
            if phantom:
                self._draw_phantom(phantom)
        
        # Desenhar interface
        if self.game_mode == STARTING and self.game_start_sprite:
            self.screen.blit(self.game_start_sprite, (0, 0))
        elif self.game_mode == FAILED and self.game_over_sprite:
            self.screen.blit(self.game_over_sprite, (0, 0))
        elif self.game_mode == WON and self.game_won_sprite:
            self.screen.blit(self.game_won_sprite, (0, 0))
        
        # Atualizar display
        pygame.display.flip()
    
    def _draw_scene(self):
        """Desenha o cenário do jogo"""
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                
                scene_type = SCENES_POSITION[i][j]
                
                # Desenhar fundo vazio primeiro
                self.screen.blit(self.scene_sprites[0], (x, y))
                
                # Desenhar elementos específicos
                if scene_type >= 1 and scene_type < len(self.scene_sprites):
                    # Se é uma moeda ou power pellet, verificar se ainda não foi coletada
                    if ((scene_type == 1 and self.scene.map[i][j] == COIN_WAY) or
                        (scene_type == 2 and self.scene.map[i][j] == POWER_WAY)):
                        self.screen.blit(self.scene_sprites[scene_type], (x, y))
                    elif scene_type > 2:  # Paredes e outros elementos
                        self.screen.blit(self.scene_sprites[scene_type], (x, y))
    
    def _draw_pacman(self):
        """Desenha o Pacman"""
        # Calcular posição na tela com interpolação suave
        screen_x, screen_y = self.pacman.get_screen_position()
        
        # Selecionar sprite baseado na direção e animação
        sprite_index = self.pacman.direction * 3 + (self.pacman.step % 3)
        if sprite_index < len(self.pacman_sprites):
            self.screen.blit(self.pacman_sprites[sprite_index], (screen_x, screen_y))
    
    def _draw_phantom(self, phantom: Phantom):
        """Desenha um fantasma"""
        # Calcular posição na tela com interpolação suave
        screen_x, screen_y = phantom.get_screen_position()
        
        # Selecionar sprite baseado no ID e status
        sprite_index = phantom.id
        if phantom.status == ESCAPE:
            sprite_index += 16  # Sprites de fuga
        
        if sprite_index < len(self.phantom_sprites):
            self.screen.blit(self.phantom_sprites[sprite_index], (screen_x, screen_y))
    
    def _start_game(self):
        """Inicia uma nova partida"""
        # Criar cenário
        self.scene = Scene()
        
        # Criar Pacman
        self.pacman = Pacman(12, 5)
        
        # Criar fantasmas
        self.phantoms[0] = Phantom(11, 10, PH_ORANGE, LEFT)
        self.phantoms[1] = Phantom(14, 10, PH_PINK, RIGHT)
        self.phantoms[2] = Phantom(11, 14, PH_CYAN, LEFT)
        self.phantoms[3] = Phantom(14, 14, PH_RED, RIGHT)
    
    def quit(self):
        """Finaliza o jogo"""
        pygame.quit()
        sys.exit()
