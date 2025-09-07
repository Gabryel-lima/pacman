# Arquitetura do Pac-Man

Este documento descreve a arquitetura técnica do jogo Pac-Man, incluindo design patterns, fluxo de dados e decisões de implementação.

## Visão Geral da Arquitetura

O jogo utiliza uma arquitetura orientada a objetos com separação clara de responsabilidades:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   main.py       │    │   game.py       │    │ controller.py   │
│   (Entry Point) │───▶│   (Game Logic)  │◀───│   (Input Mgmt)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ constants.py    │
                       │ (Configuration) │
                       └─────────────────┘
                                ▲
                                │
                       ┌─────────────────┐
                       │ menu.py         │
                       │ (Menu System)   │
                       └─────────────────┘
                                ▲
                                │
                       ┌─────────────────┐
                       │ ImprovedGhostAI │
                       │ (Advanced AI)   │
                       └─────────────────┘
```

## Componentes Principais

### 1. Classe PacMan (`src/game.py`)

**Responsabilidades:**
- Loop principal do jogo
- Gerenciamento de estado
- Física e colisões
- Renderização
- Coordenação entre sistemas

**Métodos Principais:**
```python
class PacMan:
    def __init__(self, scale)           # Inicialização
    def run(self)                       # Loop principal
    def show_mode_selection(self)       # Menu de seleção
    def _show_start_countdown(self)     # Contagem regressiva
    def move(self, key)                 # Processamento de input
    def handle_controller_input(self)   # Input de controles
    def player(self)                    # Lógica do jogador
    def ghost(self)                     # Lógica dos fantasmas (IA melhorada)
    def enhanced_ghost_intelligence()   # IA avançada dos fantasmas
    def collider(self, position, direction)  # Sistema de colisão
```

**Padrões Utilizados:**
- **State Pattern**: Diferentes estados do jogo (normal, inofensivo, game over)
- **Observer Pattern**: Sistema de eventos para colisões
- **Template Method**: Estrutura comum para diferentes tipos de entidades

### 2. Sistema de Controles (`src/controller.py`)

**Responsabilidades:**
- Detecção automática de controles
- Mapeamento de botões
- Abstração de diferentes tipos de controle
- Gerenciamento de múltiplos controles

**Classes Principais:**
```python
class ControllerManager:
    def _detect_controllers()           # Detecção automática
    def get_movement_input()            # Input de movimento
    def get_special_buttons()           # Botões especiais
    def _identify_controller_type()     # Identificação de tipo

class ControllerType(Enum):             # Tipos suportados
class ControllerButton(Enum):           # Botões mapeados
```

**Padrões Utilizados:**
- **Factory Pattern**: Criação de mapeamentos baseados no tipo
- **Strategy Pattern**: Diferentes estratégias para diferentes controles
- **Singleton Pattern**: Gerenciador único de controles

### 3. Sistema de Menu (`src/menu.py`)

**Responsabilidades:**
- Gerenciamento do menu de seleção
- Navegação entre opções
- Renderização da interface do menu
- Controle de fluxo de seleção

**Classes Principais:**
```python
class MenuSelector:
    def __init__(self, scale)           # Inicialização do menu
    def handle_input(self, key)         # Processamento de input
    def draw(self, window)              # Renderização do menu
    def get_selected_mode(self)         # Obter modo selecionado
    def reset(self)                     # Reset do menu
    def run_menu_loop(self, window)     # Loop principal do menu
```

**Padrões Utilizados:**
- **State Pattern**: Diferentes estados de seleção
- **Template Method**: Estrutura comum para renderização
- **Observer Pattern**: Notificação de mudanças de seleção

### 4. Sistema de IA Avançado (`src/game.py` - Classe ImprovedGhostAI)

**Responsabilidades:**
- Pathfinding inteligente para fantasmas
- Comportamentos distintos por fantasma
- Sistema anti-travamento
- Comportamento cooperativo entre fantasmas
- Predição de movimento do Pacman

**Classes Principais:**
```python
class ImprovedGhostAI:
    def __init__(self, game_instance)           # Inicialização da IA
    def get_manhattan_distance()               # Cálculo de distância Manhattan
    def get_euclidean_distance()               # Cálculo de distância euclidiana
    def find_path_bfs()                        # Algoritmo BFS para pathfinding
    def get_best_direction_a_star()            # Algoritmo A* simplificado
    def get_predicted_pacman_position()        # Predição de movimento
    def get_ambush_target()                    # Cálculo de emboscada
    def update_ghost_behavior()                # Atualização de comportamentos
    def improved_ghost_intelligence()          # IA principal dos fantasmas
    def get_cooperative_behavior()             # Comportamento cooperativo
```

**Padrões Utilizados:**
- **Strategy Pattern**: Diferentes estratégias para cada fantasma
- **State Pattern**: Estados de comportamento (scatter, chase, ambush, aggressive)
- **Observer Pattern**: Monitoramento de posições e comportamentos
- **Template Method**: Estrutura comum para algoritmos de pathfinding

**Algoritmos Implementados:**
- **BFS (Breadth-First Search)**: Para encontrar caminhos ótimos
- **A* Simplificado**: Para decisões direcionais inteligentes
- **Predição de Movimento**: Baseada na direção atual do Pacman
- **Sistema Anti-Travamento**: Detecção e correção de loops infinitos

### 5. Sistema de Constantes (`src/constants.py`)

**Responsabilidades:**
- Configurações centralizadas
- Definição do mapa do jogo
- Valores de pontuação e física

**Estrutura:**
```python
# Configurações de janela
SCALE = 26
WINDOW_WIDTH = SCALE * 27.5
WINDOW_HEIGHT = SCALE * 35
FPS = 60

# Estados do jogo
STARTING = 0
PLAYING = 1
FAILED = 2
WON = 3

# Mapa do jogo (matriz 2D)
GAME_MAP = [...]
```

## Fluxo de Dados

### 1. Inicialização
```
main.py → PacMan.__init__() → ControllerManager.__init__()
```

### 2. Menu e Seleção
```
run() → show_mode_selection() → MenuSelector.run_menu_loop()
     → handle_input() → get_selected_mode()
     → _show_start_countdown()
```

### 3. Loop Principal
```
run() → event.get() → move() → _set_direction()
     → handle_controller_input() → get_movement_input()
     → update_physics() → render() → display.update()
```

### 4. Sistema de Input
```
Teclado: event.key → move() → _set_direction()
Controle: get_movement_input() → _set_direction()
```

## Decisões de Design

### 1. Sistema de Escala
**Decisão**: Usar um fator de escala único para todos os elementos
**Justificativa**: Facilita redimensionamento e mantém proporções

```python
# Todos os elementos são multiplicados pelo scale
window_width = scale * 27.5
pac_man_pos = [scale * 13.1, scale * 22.6]
```

### 2. Sistema de Direções
**Decisão**: Usar vetores [x, y] para direções
**Justificativa**: Facilita cálculos matemáticos e rotações

```python
# Direções como vetores
self.pac_man_direction = [scale/16, 0]  # Direita
self.pac_man_direction = [0, -scale/16] # Cima
```

### 3. Sistema de Colisão
**Decisão**: Detecção por proximidade com zonas de colisão
**Justificativa**: Mais eficiente que pixel-perfect para este tipo de jogo

```python
def collider(self, position, direction):
    # Verifica colisão com paredes usando bounding boxes
    if x_agent >= x_wall and x_agent <= x_wall + wall_size:
        # Colisão detectada
```

### 4. Sistema de Controles
**Decisão**: Abstração completa com mapeamento automático
**Justificativa**: Suporte universal a diferentes tipos de controle

```python
# Mapeamento baseado no tipo de controle
button_mappings = {
    ControllerType.XBOX: {...},
    ControllerType.GENERIC: {...}
}
```

### 5. Sistema de Menu
**Decisão**: Menu separado e independente do jogo principal
**Justificativa**: Separação de responsabilidades e reutilização

```python
# Menu como componente independente
class MenuSelector:
    def run_menu_loop(self, window):
        # Loop próprio do menu
        # Retorna seleção ou 'quit'
```

**Características:**
- **Modular**: Pode ser reutilizado em outros jogos
- **Responsivo**: Atualiza em tempo real
- **Extensível**: Fácil adição de novas opções

### 6. Sistema de IA Avançado
**Decisão**: IA separada e especializada para cada fantasma
**Justificativa**: Comportamentos distintos e pathfinding inteligente

```python
# IA como componente especializado
class ImprovedGhostAI:
    def __init__(self, game_instance):
        # Estados específicos para cada fantasma
        self.ghost_states = {
            'blue': {'mode': 'scatter', 'mode_timer': 0},
            'orange': {'mode': 'chase', 'mode_timer': 60},
            'pink': {'mode': 'ambush', 'mode_timer': 120},
            'red': {'mode': 'aggressive', 'mode_timer': 180}
        }
```

**Características:**
- **Modular**: IA independente e reutilizável
- **Inteligente**: Algoritmos de pathfinding avançados
- **Adaptativo**: Comportamentos que mudam dinamicamente
- **Performático**: Limitação de iterações para evitar lag

## Padrões de Performance

### 1. Otimização de Renderização
- **Sprites pré-carregados**: Todos os sprites são carregados na inicialização
- **Redimensionamento único**: Sprites são redimensionados uma vez
- **Renderização condicional**: Apenas elementos visíveis são renderizados

### 2. Otimização de Física
- **Cálculos em tempo real**: Física calculada a cada frame
- **Cache de distâncias**: Distâncias entre entidades são cacheadas
- **Zona morta**: Analógicos têm zona morta para reduzir processamento

### 3. Gerenciamento de Memória
- **Limpeza automática**: Recursos são limpos ao sair
- **Reutilização de objetos**: Mesmos objetos para diferentes estados
- **Garbage collection**: Python gerencia automaticamente

## Extensibilidade

### 1. Adicionando Novos Tipos de Controle
```python
# Em controller.py
class ControllerType(Enum):
    XBOX = "xbox"
    GENERIC = "generic"
    PLAYSTATION = "playstation"  # Novo tipo

# Adicionar mapeamento
button_mappings[ControllerType.PLAYSTATION] = {...}
```

### 2. Adicionando Novas Opções de Menu
```python
# Em menu.py
class MenuSelector:
    def __init__(self, scale):
        self.modes = ["Player 1", "Player 2", "Player 3", "Multiplayer"]  # Nova opção
        
    def handle_input(self, key):
        # Lógica existente funciona automaticamente
```

### 3. Adicionando Novos Tipos de Entidade
```python
# Em game.py
def new_entity(self):
    # Seguir padrão similar aos fantasmas
    self.entity_pos = [x, y]
    self.entity_direction = [dx, dy]
    # Implementar lógica específica
```

### 4. Modificando o Mapa
```python
# Em constants.py
GAME_MAP = [
    ['#','.','#'],  # Paredes, dots, power pellets
    ['.','o','.'],
    ['#','.','#']
]
```

### 5. Adicionando Novos Comportamentos de IA
```python
# Em game.py - ImprovedGhostAI
class ImprovedGhostAI:
    def get_ghost_target(self, ghost_color):
        # Adicionar novo modo
        elif state['mode'] == 'patrol':
            return self.get_patrol_target(ghost_color)
    
    def get_patrol_target(self, ghost_color):
        # Implementar novo comportamento
        return patrol_points[ghost_color]
```

### 6. Modificando Algoritmos de Pathfinding
```python
# Em game.py - ImprovedGhostAI
def get_best_direction_a_star(self, ghost_pos, target_pos, current_direction):
    # Modificar heurística
    distance = self.get_euclidean_distance(test_pos, target_pos)  # Usar euclidiana
    # Adicionar novos fatores
    danger_factor = self.calculate_danger_level(test_pos)
    total_score = distance + direction_change_penalty + danger_factor
```

## Testes e Debug

### 1. Estrutura de Testes (Recomendada)
```
tests/
├── test_game.py          # Testes da lógica principal
├── test_controller.py    # Testes do sistema de controles
├── test_menu.py          # Testes do sistema de menu
├── test_collision.py     # Testes de colisão
└── test_physics.py       # Testes de física
```

### 2. Debug Visual
- **Status de controles**: Mostrado na tela
- **Posições**: Podem ser logadas temporariamente
- **FPS**: Monitorado pelo pygame

### 3. Configurações de Debug
```python
# Em constants.py
DEBUG_MODE = False  # Ativar logs detalhados
SHOW_COLLISION_BOXES = False  # Mostrar caixas de colisão
```

## Considerações de Segurança

### 1. Validação de Input
- **Controles**: Validação de índices e tipos
- **Teclado**: Filtragem de teclas válidas
- **Arquivos**: Verificação de existência de sprites

### 2. Tratamento de Erros
- **Controles desconectados**: Fallback para teclado
- **Sprites ausentes**: Placeholders automáticos
- **Erros de inicialização**: Graceful degradation

---

Esta arquitetura foi projetada para ser:
- **Modular**: Componentes independentes
- **Extensível**: Fácil adição de recursos
- **Manutenível**: Código limpo e documentado
- **Performática**: Otimizada para jogos 2D
