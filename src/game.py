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
        self.last_frame_time = 0
    
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
            # Obter diretório base do projeto
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Carregar sprites do Pacman (12 sprites - 4 direções x 3 animações)
            for i in range(1, 13):
                sprite_path = os.path.join(base_dir, "images", f"pacman-{i}.png")
                if os.path.exists(sprite_path):
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, (CELL_SIZE, CELL_SIZE))
                    self.pacman_sprites.append(sprite)
                else:
                    print(f"Sprite não encontrado: {sprite_path}")
                    return False
            
            # Carregar sprites dos fantasmas (24 sprites)
            for i in range(1, 25):
                sprite_path = os.path.join(base_dir, "images", f"phantom-{i}.png")
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
                sprite_path = os.path.join(base_dir, "images", filename)
                if os.path.exists(sprite_path):
                    sprite = pygame.image.load(sprite_path).convert_alpha()
                    sprite = pygame.transform.scale(sprite, (CELL_SIZE, CELL_SIZE))
                    self.scene_sprites.append(sprite)
                else:
                    print(f"Sprite não encontrado: {sprite_path}")
                    return False
            
            # Carregar sprites de interface
            interface_files = [
                ("game-start.png", "game_start_sprite"),
                ("game-over.png", "game_over_sprite"),
                ("you-won.png", "game_won_sprite")
            ]
            
            for filename, attr_name in interface_files:
                filepath = os.path.join(base_dir, "images", filename)
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
        self.last_frame_time = pygame.time.get_ticks()
        
        while self.running:
            # Calcular delta time
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - self.last_frame_time) / 1000.0  # Converter para segundos
            self.last_frame_time = current_time
            
            self._handle_events()
            self._update(delta_time)
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
    
    def _update(self, delta_time: float):
        """Atualiza a lógica do jogo"""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_update > MOVEMENT_DELAY and self.game_mode == PLAYING:
            if self.pacman and self.scene:
                if self.pacman.is_alive():
                    if self.scene.all_coins_collected():
                        self.game_mode = WON
                        # Reiniciar o jogo automaticamente após vitória
                        self._restart_level()
                    else:
                        # Mover Pacman
                        self.pacman.move(self.scene, delta_time)
                        
                        # Mover fantasmas com IA
                        for phantom in self.phantoms:
                            if phantom and phantom.status != DEAD:
                                phantom.move(self.scene, self.pacman.x, self.pacman.y, delta_time)
                                
                                # Verificar colisão com Pacman
                                distance = phantom._calculate_distance_to_pacman(self.pacman.x, self.pacman.y)
                                
                                if distance <= 1.1:  # Colisão próxima
                                    if self.pacman.power > 0:
                                        # Pacman come o fantasma
                                        phantom.status = DEAD
                                        phantom.step = 0
                                        phantom.harmless_mode = False
                                        self.pacman.points += 200
                                        # Reposicionar fantasma morto no centro
                                        phantom.x = 13
                                        phantom.y = 12
                                    else:
                                        # Fantasma mata Pacman
                                        self.pacman.life = 0
                                        self.pacman.end_game = True
                                        self.pacman.sprite_frame = 0
                                        self.pacman.sprite_speed = 1
                        
                        # Atualizar modo dos fantasmas baseado no poder do Pacman
                        for phantom in self.phantoms:
                            if phantom and phantom.status != DEAD:
                                phantom.harmless_mode = (self.pacman.power > 0)
                else:
                    # Verificar se a animação de morte terminou
                    if self.pacman.sprite_frame >= 60:
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
        
        # Desenhar informações do jogo (pontuação, etc.)
        if self.pacman and self.game_mode == PLAYING:
            self._draw_hud()
        
        # Desenhar interface
        if self.game_mode == STARTING and self.game_start_sprite:
            self.screen.blit(self.game_start_sprite, (0, 0))
        elif self.game_mode == FAILED and self.game_over_sprite:
            self.screen.blit(self.game_over_sprite, (0, 0))
        elif self.game_mode == WON and self.game_won_sprite:
            self.screen.blit(self.game_won_sprite, (0, 0))
        
        # Atualizar display
        pygame.display.flip()
    
    def _draw_hud(self):
        """Desenha informações do jogo (HUD)"""
        if not hasattr(self, '_font'):
            # Inicializar fonte se não existir
            self._font = pygame.font.Font(None, 24)
        
        # Desenhar pontuação centralizada
        score_text = self._font.render(f"Score: {self.pacman.points}", True, (255, 255, 255))
        score_x = (WINDOW_SIZE - score_text.get_width()) // 2
        score_y = WINDOW_SIZE - 60
        self.screen.blit(score_text, (score_x, score_y))
        
        # Desenhar vidas
        lives_text = self._font.render(f"Lives: {max(self.pacman.life, 0)}X", True, (255, 255, 255))
        lives_x = (WINDOW_SIZE - lives_text.get_width()) // 2
        lives_y = WINDOW_SIZE - 30
        self.screen.blit(lives_text, (lives_x, lives_y))
        
        # Desenhar status do poder
        if self.pacman.power > 0:
            power_text = self._font.render(f"Power: {self.pacman.power}", True, (255, 255, 0))
            self.screen.blit(power_text, (10, 10))
    
    def _draw_scene(self):
        """Desenha o cenário do jogo"""
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                
                scene_type = SCENES_POSITION[i][j]
                
                # Desenhar fundo vazio primeiro
                self.screen.blit(self.scene_sprites[0], (x, y))  # empty.png
                
                # Desenhar elementos específicos baseado no tipo de cena
                if scene_type == 1:  # Moeda
                    if self.scene.map[i][j] == COIN_WAY:
                        self.screen.blit(self.scene_sprites[1], (x, y))  # coin.png
                elif scene_type == 2:  # Power pellet
                    if self.scene.map[i][j] == POWER_WAY:
                        self.screen.blit(self.scene_sprites[2], (x, y))  # power.png
                elif scene_type == 3:  # Parede vertical
                    self.screen.blit(self.scene_sprites[3], (x, y))  # vertical.png
                elif scene_type == 4:  # Parede horizontal
                    self.screen.blit(self.scene_sprites[4], (x, y))  # horizontal.png
                elif scene_type == 5:  # Curva base esquerda
                    self.screen.blit(self.scene_sprites[5], (x, y))  # curve-base-left.png
                elif scene_type == 6:  # Curva base direita
                    self.screen.blit(self.scene_sprites[6], (x, y))  # curve-base-right.png
                elif scene_type == 7:  # Curva topo esquerda
                    self.screen.blit(self.scene_sprites[7], (x, y))  # curve-top-left.png
                elif scene_type == 8:  # Curva topo direita
                    self.screen.blit(self.scene_sprites[8], (x, y))  # curve-top-right.png
                elif scene_type == 9:  # Final esquerda
                    self.screen.blit(self.scene_sprites[9], (x, y))  # end-left.png
                elif scene_type == 10:  # Final direita
                    self.screen.blit(self.scene_sprites[10], (x, y))  # end-right.png
                elif scene_type == 11:  # Final base
                    self.screen.blit(self.scene_sprites[11], (x, y))  # end-base.png
                elif scene_type == 12:  # Final topo
                    self.screen.blit(self.scene_sprites[12], (x, y))  # end-top.png
    
    def _draw_pacman(self):
        """Desenha o Pacman com animação baseada em frames"""
        # Calcular posição na tela
        screen_x = self.pacman.x * CELL_SIZE
        screen_y = self.pacman.y * CELL_SIZE
        
        # Sistema de animação baseado em frames (como no exemplo)
        if self.pacman.end_game:
            # Animação de morte
            if self.pacman.sprite_frame <= 5:
                sprite_index = 5
            elif self.pacman.sprite_frame <= 10:
                sprite_index = 6
            elif self.pacman.sprite_frame <= 15:
                sprite_index = 7
            elif self.pacman.sprite_frame <= 20:
                sprite_index = 8
            elif self.pacman.sprite_frame <= 25:
                sprite_index = 9
            elif self.pacman.sprite_frame <= 30:
                sprite_index = 10
            elif self.pacman.sprite_frame <= 35:
                sprite_index = 11
            elif self.pacman.sprite_frame <= 40:
                sprite_index = 12
            elif self.pacman.sprite_frame <= 45:
                sprite_index = 13
            elif self.pacman.sprite_frame <= 50:
                sprite_index = 14
            elif self.pacman.sprite_frame <= 55:
                sprite_index = 15
            else:
                sprite_index = 16
        else:
            # Animação normal baseada na direção
            if self.pacman.sprite_frame <= 6:
                sprite_index = self.pacman.direction * 3 + 0
            elif self.pacman.sprite_frame <= 12:
                sprite_index = self.pacman.direction * 3 + 0
            elif self.pacman.sprite_frame <= 18:
                sprite_index = self.pacman.direction * 3 + 1
            elif self.pacman.sprite_frame <= 24:
                sprite_index = self.pacman.direction * 3 + 2
            elif self.pacman.sprite_frame <= 30:
                sprite_index = self.pacman.direction * 3 + 2
            elif self.pacman.sprite_frame <= 36:
                sprite_index = self.pacman.direction * 3 + 2
            elif self.pacman.sprite_frame <= 42:
                sprite_index = self.pacman.direction * 3 + 2
            elif self.pacman.sprite_frame <= 48:
                sprite_index = self.pacman.direction * 3 + 2
            elif self.pacman.sprite_frame <= 54:
                sprite_index = self.pacman.direction * 3 + 1
            else:
                sprite_index = self.pacman.direction * 3 + 0
        
        # Garantir que o índice está dentro dos limites
        sprite_index = min(sprite_index, len(self.pacman_sprites) - 1)
        self.screen.blit(self.pacman_sprites[sprite_index], (screen_x, screen_y))
    
    def _draw_phantom(self, phantom: Phantom):
        """Desenha um fantasma com animação baseada em frames"""
        # Calcular posição na tela
        screen_x = phantom.x * CELL_SIZE
        screen_y = phantom.y * CELL_SIZE
        
        # Sistema de animação baseado em frames (como no exemplo)
        if phantom.harmless_mode:
            # Fantasma em modo fuga - usar sprites azuis
            if phantom.sprite_frame <= 15:
                sprite_index = 16  # Harmless ghost frame 0
            elif phantom.sprite_frame <= 30:
                sprite_index = 17  # Harmless ghost frame 1
            elif phantom.sprite_frame <= 45:
                sprite_index = 16  # Harmless ghost frame 0
            else:
                sprite_index = 17  # Harmless ghost frame 1
        else:
            # Fantasma normal - usar sprites baseados no ID
            if phantom.sprite_frame <= 15:
                sprite_index = phantom.id + 0  # Frame 0
            elif phantom.sprite_frame <= 30:
                sprite_index = phantom.id + 1  # Frame 1
            elif phantom.sprite_frame <= 45:
                sprite_index = phantom.id + 0  # Frame 0
            else:
                sprite_index = phantom.id + 1  # Frame 1
        
        # Garantir que o índice está dentro dos limites
        sprite_index = min(sprite_index, len(self.phantom_sprites) - 1)
        self.screen.blit(self.phantom_sprites[sprite_index], (screen_x, screen_y))
    
    def _start_game(self):
        """Inicia uma nova partida"""
        # Criar cenário
        self.scene = Scene()
        
        # Criar Pacman na posição inicial correta
        self.pacman = Pacman(13, 20)  # Posição mais adequada no mapa
        
        # Criar fantasmas nas posições iniciais corretas
        self.phantoms[0] = Phantom(12, 11, PH_ORANGE, LEFT)
        self.phantoms[1] = Phantom(13, 11, PH_PINK, RIGHT)
        self.phantoms[2] = Phantom(12, 13, PH_CYAN, LEFT)
        self.phantoms[3] = Phantom(13, 13, PH_RED, RIGHT)
        
        # Resetar timer de movimento
        self.last_update = pygame.time.get_ticks()
        self.last_frame_time = pygame.time.get_ticks()
    
    def _restart_level(self):
        """Reinicia o nível após vitória"""
        # Criar novo cenário
        self.scene = Scene()
        
        # Resetar Pacman
        self.pacman.x = 13
        self.pacman.y = 20
        self.pacman.direction = RIGHT
        self.pacman.next_direction = RIGHT
        self.pacman.end_game = False
        self.pacman.sprite_frame = 0
        self.pacman.sprite_speed = 2
        
        # Resetar fantasmas
        self.phantoms[0] = Phantom(12, 11, PH_ORANGE, LEFT)
        self.phantoms[1] = Phantom(13, 11, PH_PINK, RIGHT)
        self.phantoms[2] = Phantom(12, 13, PH_CYAN, LEFT)
        self.phantoms[3] = Phantom(13, 13, PH_RED, RIGHT)
        
        # Resetar timer
        self.last_update = pygame.time.get_ticks()
        self.last_frame_time = pygame.time.get_ticks()
    
    def quit(self):
        """Finaliza o jogo"""
        pygame.quit()
        sys.exit()
