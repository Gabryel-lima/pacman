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
    def move(self, key)                 # Processamento de input
    def handle_controller_input(self)   # Input de controles
    def player(self)                    # Lógica do jogador
    def ghost(self)                     # Lógica dos fantasmas
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

### 3. Sistema de Constantes (`src/constants.py`)

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

### 2. Loop Principal
```
run() → event.get() → move() → _set_direction()
     → handle_controller_input() → get_movement_input()
     → update_physics() → render() → display.update()
```

### 3. Sistema de Input
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

### 2. Adicionando Novos Tipos de Entidade
```python
# Em game.py
def new_entity(self):
    # Seguir padrão similar aos fantasmas
    self.entity_pos = [x, y]
    self.entity_direction = [dx, dy]
    # Implementar lógica específica
```

### 3. Modificando o Mapa
```python
# Em constants.py
GAME_MAP = [
    ['#','.','#'],  # Paredes, dots, power pellets
    ['.','o','.'],
    ['#','.','#']
]
```

## Testes e Debug

### 1. Estrutura de Testes (Recomendada)
```
tests/
├── test_game.py          # Testes da lógica principal
├── test_controller.py    # Testes do sistema de controles
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
