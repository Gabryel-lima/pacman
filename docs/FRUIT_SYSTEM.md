# Sistema de Frutas Coletáveis - Pacman

## Visão Geral

O sistema de frutas coletáveis foi completamente implementado e otimizado para proporcionar uma experiência de jogo mais rica e envolvente. O sistema inclui raridade, spawn inteligente e posicionamento seguro.

## Características Principais

### 🍒 Sistema de Raridade

As frutas são categorizadas por raridade, onde frutas mais valiosas são mais raras:

| Fruta | Pontos | Probabilidade | Raridade | Emoji |
|-------|--------|---------------|----------|-------|
| Cherry | 100 | 30% | Comum | 🍒 |
| Strawberry | 200 | 25% | Comum | 🍓 |
| Orange | 300 | 20% | Incomum | 🍊 |
| Apple | 400 | 15% | Incomum | 🍎 |
| Bell | 500 | 5% | Raro | 🔔 |
| Key | 700 | 3% | Raro | 🗝️ |
| Coconut | 1000 | 1.5% | Muito Raro | 🥥 |
| Flower | 2000 | 0.5% | Lendário | 🌸 |

### ⏰ Sistema de Timing

- **Spawn**: A cada 10 segundos (600 frames a 60 FPS)
- **Duração**: 10 segundos por fruta
- **Máximo**: 2 frutas ativas simultaneamente
- **Contador**: Sistema independente de frames (`fruit_frame_counter`)

### 📍 Posicionamento Inteligente

#### Posições Seguras
As frutas aparecem em 8 posições estratégicas:

```
(3, 3)    (24, 3)    # Corredor superior
(7, 11)   (19, 11)   # Corredor central
(7, 15)   (19, 15)   # Corredor inferior
(3, 23)   (24, 23)   # Corredor inferior
```

#### Proteções Implementadas
- ✅ Verificação automática de conflitos com spawn de fantasmas
- ✅ Posições centralizadas nos corredores
- ✅ Evita sobreposição com paredes
- ✅ Sistema de fallback para posições indisponíveis

### 🎨 Sistema Visual

#### Sprites Otimizadas
- **Tamanho**: 20% maiores que o tamanho original (1.2x)
- **Carregamento**: Automático de todas as 8 sprites
- **Fallback**: Placeholders para sprites ausentes
- **Centralização**: Posicionamento automático no centro do grid

#### Renderização
- Cálculo automático de offset para centralização
- Renderização suave e bem posicionada
- Compatibilidade com sistema de animação existente

## Implementação Técnica

### Métodos Principais

#### `_initialize_fruits()`
Inicializa o sistema de frutas com:
- Dicionário de frutas ativas
- Sistema de raridade com probabilidades
- Contadores de timing
- Configurações de spawn

#### `_load_fruit_sprites()`
Carrega todas as sprites das frutas:
- Verificação de existência de arquivos
- Redimensionamento automático (1.2x)
- Sistema de fallback com placeholders
- Armazenamento em atributos dinâmicos

#### `_spawn_fruit()`
Spawna uma nova fruta:
- Seleção de posição segura
- Verificação de conflitos
- Aplicação do sistema de raridade
- Configuração de timing

#### `_select_fruit_by_rarity()`
Seleciona fruta baseada em probabilidades:
- Uso de `random.choices()` com pesos
- Sistema probabilístico balanceado
- Retorno da fruta selecionada

#### `_is_ghost_spawn_position()`
Verifica conflitos com spawn de fantasmas:
- Lista de posições proibidas
- Verificação de área de spawn
- Proteção contra sobreposições

#### `_update_fruits()`
Atualiza o estado das frutas:
- Incremento do contador de frames
- Spawn de novas frutas
- Remoção de frutas expiradas
- Gerenciamento do ciclo de vida

### Constantes e Configurações

#### `FRUIT_POSITIONS`
Posições seguras para spawn de frutas:
```python
FRUIT_POSITIONS = [
    (3, 3), (24, 3),    # Superior
    (7, 11), (19, 11),  # Central
    (7, 15), (19, 15),  # Inferior
    (3, 23), (24, 23)   # Inferior
]
```

#### Sistema de Raridade
```python
fruit_rarity = {
    FRUIT_CHERRY: 30,      # 30% - Comum
    FRUIT_STRAWBERRY: 25,  # 25% - Comum
    FRUIT_ORANGE: 20,      # 20% - Incomum
    FRUIT_APPLE: 15,       # 15% - Incomum
    FRUIT_BELL: 5,         # 5% - Raro
    FRUIT_KEY: 3,          # 3% - Raro
    FRUIT_COCONUT: 1.5,    # 1.5% - Muito Raro
    FRUIT_FLOWER: 0.5      # 0.5% - Lendário
}
```

## Integração com o Jogo

### Loop Principal
O sistema de frutas é integrado ao loop principal do jogo:
1. **Atualização**: `_update_fruits()` chamado a cada frame
2. **Renderização**: Frutas desenhadas no método `board()`
3. **Colisão**: Coleta de frutas no método `collect_fruits()`

### Compatibilidade
- ✅ Sistema de pontuação existente
- ✅ Sistema de animação
- ✅ Sistema de colisão
- ✅ Sistema de IA dos fantasmas

## Benefícios do Sistema

### Para o Jogador
- 🎯 **Variedade**: 8 tipos diferentes de frutas
- 🎲 **Emoção**: Sistema de raridade cria expectativa
- 🏆 **Recompensa**: Frutas raras valem mais pontos
- 👀 **Visibilidade**: Sprites maiores e bem posicionadas

### Para o Gameplay
- ⚖️ **Balanceamento**: Probabilidades cuidadosamente ajustadas
- 🛡️ **Estabilidade**: Sistema robusto sem conflitos
- 🎮 **Fluidez**: Integração suave com mecânicas existentes
- 🔄 **Dinâmico**: Spawn automático mantém o jogo ativo

## Manutenção e Extensibilidade

### Adicionar Novas Frutas
1. Adicionar sprite no diretório `img/`
2. Definir constante em `constants.py`
3. Adicionar pontos em `constants.py`
4. Incluir no dicionário `fruit_sprites` em `_load_fruit_sprites()`
5. Adicionar probabilidade em `fruit_rarity`

### Ajustar Raridade
Modificar as probabilidades em `fruit_rarity` mantendo a soma em 100%.

### Alterar Timing
Ajustar `fruit_spawn_delay` e `fruit_duration` conforme necessário.

---

**Versão**: 1.4.0  
**Data**: 2024-12-19  
**Status**: ✅ Implementado e Testado
