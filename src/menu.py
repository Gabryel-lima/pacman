"""
Menu de seleção de modo do jogo Pac-Man
"""

import pygame as pg
from .constants import *


class MenuSelector:
    """Classe para gerenciar o menu de seleção de modo"""
    
    def __init__(self, scale):
        """Inicializa o menu com o fator de escala especificado"""
        self.scale = scale
        self.white = WHITE
        self.black = BLACK
        self.blue = BLUE
        
        # Configurar fonte
        pg.font.init()
        self.title_font = pg.font.SysFont("Courier New", int(scale * 3), bold=True)
        self.menu_font = pg.font.SysFont("Courier New", int(scale * 2), bold=True)
        self.instruction_font = pg.font.SysFont("Courier New", int(scale * 1.5), bold=True)
        
        # Opções do menu
        self.modes = ["Player 1", "Player 2", "Player 3"]
        self.selected_mode = 0
        self.selected = False
        
        # Cores para destacar seleção
        self.selected_color = (255, 255, 0)  # Amarelo
        self.normal_color = self.white
        
    def handle_input(self, key):
        """Processa entrada do teclado para navegação no menu"""
        if key == 'w' or key == 'up':
            self.selected_mode = (self.selected_mode - 1) % len(self.modes)
        elif key == 's' or key == 'down':
            self.selected_mode = (self.selected_mode + 1) % len(self.modes)
        elif key == 'return' or key == 'enter':
            self.selected = True
        elif key == 'escape':
            return 'quit'
        return None
    
    def draw(self, window):
        """Desenha o menu na janela"""
        window_width = window.get_width()
        window_height = window.get_height()
        
        # Limpar janela
        window.fill(self.black)
        
        # Desenhar título
        title_text = self.title_font.render("PAC-MAN", 1, self.white)
        title_x = (window_width / 2) - (title_text.get_width() / 2)
        title_y = window_height * 0.2
        window.blit(title_text, (title_x, title_y))
        
        # Desenhar subtítulo
        subtitle_text = self.menu_font.render("Select Game Mode", 1, self.white)
        subtitle_x = (window_width / 2) - (subtitle_text.get_width() / 2)
        subtitle_y = title_y + self.scale * 4
        window.blit(subtitle_text, (subtitle_x, subtitle_y))
        
        # Desenhar opções do menu
        menu_start_y = window_height * 0.4
        for i, mode in enumerate(self.modes):
            # Escolher cor baseada na seleção
            color = self.selected_color if i == self.selected_mode else self.normal_color
            
            # Desenhar texto do modo
            mode_text = self.menu_font.render(mode, 1, color)
            mode_x = (window_width / 2) - (mode_text.get_width() / 2)
            mode_y = menu_start_y + (i * self.scale * 3)
            window.blit(mode_text, (mode_x, mode_y))
            
            # Desenhar indicador de seleção (seta)
            if i == self.selected_mode:
                arrow_text = self.menu_font.render(">", 1, self.selected_color)
                arrow_x = mode_x - self.scale * 2
                window.blit(arrow_text, (arrow_x, mode_y))
                
                arrow_text2 = self.menu_font.render("<", 1, self.selected_color)
                arrow_x2 = mode_x + mode_text.get_width() + self.scale * 0.5
                window.blit(arrow_text2, (arrow_x2, mode_y))
        
        # Desenhar instruções de navegação
        instruction_text = self.instruction_font.render("Use UP/DOWN arrows to navigate", 1, self.white)
        instruction_x = (window_width / 2) - (instruction_text.get_width() / 2)
        instruction_y = window_height * 0.7
        window.blit(instruction_text, (instruction_x, instruction_y))
        
        enter_text = self.instruction_font.render("Press ENTER to select", 1, self.white)
        enter_x = (window_width / 2) - (enter_text.get_width() / 2)
        enter_y = instruction_y + self.scale * 1.5
        window.blit(enter_text, (enter_x, enter_y))
        
        # Desenhar controles de teclado
        controls_title = self.instruction_font.render("Game Controls:", 1, self.white)
        controls_x = (window_width / 2) - (controls_title.get_width() / 2)
        controls_y = enter_y + self.scale * 1.5
        window.blit(controls_title, (controls_x, controls_y))
        
        # Container para controles (linha separadora)
        separator_y = controls_y + self.scale * 1.5
        separator_text = self.instruction_font.render("─" * 25, 1, self.white)
        separator_x = (window_width / 2) - (separator_text.get_width() / 2)
        window.blit(separator_text, (separator_x, separator_y))
        
        # Player 1
        p1_text = self.instruction_font.render("Player 1: WASD", 1, self.white)
        p1_x = (window_width / 2) - (p1_text.get_width() / 2)
        p1_y = separator_y + self.scale * 1.5
        window.blit(p1_text, (p1_x, p1_y))
        
        # Player 2
        p2_text = self.instruction_font.render("Player 2: Arrow Keys", 1, self.white)
        p2_x = (window_width / 2) - (p2_text.get_width() / 2)
        p2_y = p1_y + self.scale * 1.3
        window.blit(p2_text, (p2_x, p2_y))
        
        # Player 3
        p3_text = self.instruction_font.render("Player 3: IJKL", 1, self.white)
        p3_x = (window_width / 2) - (p3_text.get_width() / 2)
        p3_y = p2_y + self.scale * 1.3
        window.blit(p3_text, (p3_x, p3_y))
    
    def get_selected_mode(self):
        """Retorna o modo selecionado"""
        if self.selected:
            return self.modes[self.selected_mode]
        return None
    
    def reset(self):
        """Reseta o menu para o estado inicial"""
        self.selected_mode = 0
        self.selected = False
    
    def run_menu_loop(self, window):
        """Executa o loop principal do menu"""
        clock = pg.time.Clock()
        running = True
        
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'quit'
                if event.type == pg.KEYDOWN:
                    result = self.handle_input(pg.key.name(event.key))
                    if result == 'quit':
                        return 'quit'
                    if self.selected:
                        return self.get_selected_mode()
            
            # Desenhar menu
            self.draw(window)
            pg.display.update()
            clock.tick(FPS)
        
        return 'quit'
