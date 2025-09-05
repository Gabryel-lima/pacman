"""
Sistema de gerenciamento de controles para o jogo Pac-Man
Suporta controles Xbox e controles genéricos
"""

import pygame as pg
from enum import Enum
from typing import Optional, Dict, List, Tuple


class ControllerType(Enum):
    """Tipos de controles suportados"""
    XBOX = "xbox"
    GENERIC = "generic"
    UNKNOWN = "unknown"


class ControllerButton(Enum):
    """Botões do controle mapeados"""
    # Botões principais
    A = "a"
    B = "b"
    X = "x"
    Y = "y"
    
    # Botões de ombro
    LEFT_SHOULDER = "left_shoulder"
    RIGHT_SHOULDER = "right_shoulder"
    
    # Botões de menu
    START = "start"
    SELECT = "select"
    
    # Analógicos
    LEFT_STICK = "left_stick"
    RIGHT_STICK = "right_stick"
    
    # D-pad
    DPAD_UP = "dpad_up"
    DPAD_DOWN = "dpad_down"
    DPAD_LEFT = "dpad_left"
    DPAD_RIGHT = "dpad_right"


class ControllerManager:
    """Gerenciador de controles para o jogo Pac-Man"""
    
    def __init__(self):
        """Inicializa o gerenciador de controles"""
        self.controllers: List[pg.joystick.Joystick] = []
        self.controller_types: List[ControllerType] = []
        self.deadzone = 0.3  # Zona morta para analógicos
        self.button_mappings = self._create_button_mappings()
        
        # Inicializar pygame.joystick
        pg.joystick.init()
        
        # Detectar controles conectados
        self._detect_controllers()
    
    def _create_button_mappings(self) -> Dict[ControllerType, Dict[str, int]]:
        """Cria mapeamentos de botões para diferentes tipos de controles"""
        return {
            ControllerType.XBOX: {
                # Botões principais (Xbox)
                'a': 0,      # A
                'b': 1,      # B
                'x': 2,      # X
                'y': 3,      # Y
                'left_shoulder': 4,   # LB
                'right_shoulder': 5,  # RB
                'select': 6,          # Back
                'start': 7,           # Start
                'left_stick': 8,      # Left stick click
                'right_stick': 9,     # Right stick click
                
                # D-pad (hat)
                'dpad_up': (0, 1),
                'dpad_down': (0, -1),
                'dpad_left': (0, -1),
                'dpad_right': (0, 1),
                
                # Analógicos
                'left_stick_x': 0,
                'left_stick_y': 1,
                'right_stick_x': 2,
                'right_stick_y': 3,
                'left_trigger': 4,
                'right_trigger': 5
            },
            ControllerType.GENERIC: {
                # Mapeamento genérico (assume layout similar ao Xbox)
                'a': 0,
                'b': 1,
                'x': 2,
                'y': 3,
                'left_shoulder': 4,
                'right_shoulder': 5,
                'select': 6,
                'start': 7,
                'left_stick': 8,
                'right_stick': 9,
                
                # D-pad
                'dpad_up': (0, 1),
                'dpad_down': (0, -1),
                'dpad_left': (0, -1),
                'dpad_right': (0, 1),
                
                # Analógicos
                'left_stick_x': 0,
                'left_stick_y': 1,
                'right_stick_x': 2,
                'right_stick_y': 3,
                'left_trigger': 4,
                'right_trigger': 5
            }
        }
    
    def _detect_controllers(self):
        """Detecta controles conectados e identifica seus tipos"""
        self.controllers.clear()
        self.controller_types.clear()
        
        num_joysticks = pg.joystick.get_count()
        
        for i in range(num_joysticks):
            try:
                controller = pg.joystick.Joystick(i)
                controller.init()
                self.controllers.append(controller)
                
                # Identificar tipo do controle
                controller_type = self._identify_controller_type(controller)
                self.controller_types.append(controller_type)
                
                # Controle detectado e inicializado
                
            except Exception:
                # Erro ao inicializar controle - continuar com outros
                pass
    
    def _identify_controller_type(self, controller: pg.joystick.Joystick) -> ControllerType:
        """Identifica o tipo do controle baseado no nome"""
        name = controller.get_name().lower()
        
        # Detectar controles Xbox
        xbox_keywords = ['xbox', 'microsoft', 'xinput']
        if any(keyword in name for keyword in xbox_keywords):
            return ControllerType.XBOX
        
        # Detectar outros controles conhecidos
        if 'playstation' in name or 'sony' in name:
            return ControllerType.GENERIC
        
        # Controle genérico para outros
        return ControllerType.GENERIC
    
    def get_controller_count(self) -> int:
        """Retorna o número de controles conectados"""
        return len(self.controllers)
    
    def is_controller_connected(self, index: int = 0) -> bool:
        """Verifica se um controle específico está conectado"""
        return 0 <= index < len(self.controllers)
    
    def get_controller_name(self, index: int = 0) -> str:
        """Retorna o nome do controle"""
        if self.is_controller_connected(index):
            return self.controllers[index].get_name()
        return "Nenhum controle conectado"
    
    def get_controller_type(self, index: int = 0) -> ControllerType:
        """Retorna o tipo do controle"""
        if self.is_controller_connected(index):
            return self.controller_types[index]
        return ControllerType.UNKNOWN
    
    def get_button_pressed(self, button: ControllerButton, controller_index: int = 0) -> bool:
        """Verifica se um botão específico está pressionado"""
        if not self.is_controller_connected(controller_index):
            return False
        
        controller = self.controllers[controller_index]
        controller_type = self.controller_types[controller_index]
        
        try:
            if button.value in ['dpad_up', 'dpad_down', 'dpad_left', 'dpad_right']:
                # D-pad
                hat_value = controller.get_hat(0)
                dpad_mapping = self.button_mappings[controller_type][button.value]
                return hat_value == dpad_mapping
            else:
                # Botões normais
                button_id = self.button_mappings[controller_type][button.value]
                return controller.get_button(button_id)
        except (IndexError, KeyError):
            return False
    
    def get_analog_input(self, axis: str, controller_index: int = 0) -> float:
        """Retorna o valor do analógico (entre -1.0 e 1.0)"""
        if not self.is_controller_connected(controller_index):
            return 0.0
        
        controller = self.controllers[controller_index]
        controller_type = self.controller_types[controller_index]
        
        try:
            axis_id = self.button_mappings[controller_type][axis]
            value = controller.get_axis(axis_id)
            
            # Aplicar zona morta
            if abs(value) < self.deadzone:
                return 0.0
            
            return value
        except (IndexError, KeyError):
            return 0.0
    
    def get_movement_input(self, controller_index: int = 0) -> Tuple[str, bool]:
        """
        Retorna o input de movimento do controle
        Retorna: (direção, se há input)
        """
        if not self.is_controller_connected(controller_index):
            return "", False
        
        # Verificar D-pad primeiro
        if self.get_button_pressed(ControllerButton.DPAD_UP, controller_index):
            return "up", True
        elif self.get_button_pressed(ControllerButton.DPAD_DOWN, controller_index):
            return "down", True
        elif self.get_button_pressed(ControllerButton.DPAD_LEFT, controller_index):
            return "left", True
        elif self.get_button_pressed(ControllerButton.DPAD_RIGHT, controller_index):
            return "right", True
        
        # Verificar analógico esquerdo
        left_x = self.get_analog_input('left_stick_x', controller_index)
        left_y = self.get_analog_input('left_stick_y', controller_index)
        
        # Determinar direção baseada no analógico
        if abs(left_x) > abs(left_y):
            if left_x > 0.5:
                return "right", True
            elif left_x < -0.5:
                return "left", True
        else:
            if left_y > 0.5:
                return "down", True
            elif left_y < -0.5:
                return "up", True
        
        return "", False
    
    def get_special_buttons(self, controller_index: int = 0) -> Dict[str, bool]:
        """Retorna o estado dos botões especiais"""
        if not self.is_controller_connected(controller_index):
            return {}
        
        return {
            'restart': self.get_button_pressed(ControllerButton.START, controller_index),
            'pause': self.get_button_pressed(ControllerButton.SELECT, controller_index),
            'action': self.get_button_pressed(ControllerButton.A, controller_index)
        }
    
    def update(self):
        """Atualiza o estado dos controles (chamar a cada frame)"""
        # Verificar se novos controles foram conectados
        current_count = pg.joystick.get_count()
        if current_count != len(self.controllers):
            self._detect_controllers()
    
    def cleanup(self):
        """Limpa recursos dos controles"""
        for controller in self.controllers:
            try:
                controller.quit()
            except:
                pass
        self.controllers.clear()
        self.controller_types.clear()
        pg.joystick.quit()
