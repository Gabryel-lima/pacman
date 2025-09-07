# Changelog - Pac-Man

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [1.4.0] - 2024-12-19

### 🍒 Sistema de Frutas Coletáveis - Melhorias Completas

#### ✨ Adicionado
- **Sistema de raridade para frutas**
  - 🍒 **Cherry** (100 pts) - 30% probabilidade - Comum
  - 🍓 **Strawberry** (200 pts) - 25% probabilidade - Comum  
  - 🍊 **Orange** (300 pts) - 20% probabilidade - Incomum
  - 🍎 **Apple** (400 pts) - 15% probabilidade - Incomum
  - 🔔 **Bell** (500 pts) - 5% probabilidade - Raro
  - 🗝️ **Key** (700 pts) - 3% probabilidade - Raro
  - 🥥 **Coconut** (1000 pts) - 1.5% probabilidade - Muito Raro
  - 🌸 **Flower** (2000 pts) - 0.5% probabilidade - Lendário

- **Sistema de spawn inteligente**
  - Contador de frames separado para frutas (`fruit_frame_counter`)
  - Spawn automático a cada 10 segundos (600 frames)
  - Máximo de 2 frutas ativas simultaneamente
  - Duração de 10 segundos por fruta

- **Sistema de posicionamento seguro**
  - Verificação automática de conflitos com spawn de fantasmas
  - Método `_is_ghost_spawn_position()` para evitar sobreposições
  - Posições centralizadas nos corredores para melhor visibilidade

#### 🔧 Melhorado
- **Carregamento de sprites**
  - Todas as 8 sprites de frutas carregadas automaticamente
  - Sistema de fallback com placeholders para sprites ausentes
  - Sprites 20% maiores (1.2x o tamanho original) para melhor visibilidade

- **Renderização otimizada**
  - Centralização automática das frutas no grid
  - Cálculo de offset para sprites maiores
  - Renderização suave e bem posicionada

- **Posicionamento das frutas**
  - Posições centralizadas nos corredores
  - Evita conflitos com spawn de fantasmas
  - 8 posições estratégicas no mapa

#### 🐛 Corrigido
- **Problema de timing**
  - Corrigido sistema de contagem de frames para frutas
  - Eliminado conflito com `sprite_frame` que era resetado
  - Spawn consistente e previsível

- **Conflitos de posicionamento**
  - Removidas posições (13, 11) e (13, 15) que conflitavam com spawn de fantasmas
  - Sistema de verificação automática de posições seguras

#### 📊 Detalhes Técnicos
- **Métodos adicionados**:
  - `_initialize_fruits()` - Inicialização do sistema de frutas
  - `_load_fruit_sprites()` - Carregamento das sprites
  - `_spawn_fruit()` - Spawn inteligente de frutas
  - `_update_fruits()` - Atualização do estado das frutas
  - `_select_fruit_by_rarity()` - Seleção baseada em probabilidades
  - `_is_ghost_spawn_position()` - Verificação de conflitos
  - `_get_fruit_sprite()` - Retorno da sprite correspondente
  - `_get_fruit_points()` - Retorno dos pontos da fruta

- **Constantes atualizadas**:
  - `FRUIT_POSITIONS` - Posições centralizadas e seguras
  - Sistema de raridade com probabilidades balanceadas

## [1.3.0] - 2024-12-19

### ✨ Adicionado
- **Sistema de IA avançado para fantasmas**
  - Classe `ImprovedGhostAI` com pathfinding inteligente
  - Algoritmo BFS (Breadth-First Search) para encontrar caminhos ótimos
  - Algoritmo A* simplificado para decisões direcionais mais inteligentes
  - Sistema de predição de movimento do Pacman
  - Comportamentos distintos para cada fantasma:
    - 🔵 **Fantasma Azul**: Modo scatter (vai para cantos específicos)
    - 🟠 **Fantasma Laranja**: Modo chase com distância inteligente
    - 🩷 **Fantasma Rosa**: Modo ambush (intercepta o Pacman)
    - 🔴 **Fantasma Vermelho**: Modo aggressive (perseguição direta)

- **Sistema anti-travamento**
  - Detecção automática de fantasmas presos
  - Sistema de recuperação com direção aleatória forçada
  - Histórico de posições para análise de movimento

- **Comportamento cooperativo**
  - Evita agrupamento excessivo entre fantasmas
  - Sistema de distância mínima entre fantasmas
  - Comportamento mais realista e desafiador

- **Ciclos dinâmicos de comportamento**
  - Alternância automática entre modos scatter e chase
  - Timing personalizado para cada fantasma
  - Comportamento mais próximo ao Pac-Man original

### 🔧 Melhorado
- **Inteligência dos fantasmas**
  - Evita reversões desnecessárias de direção
  - Pathfinding mais eficiente e inteligente
  - Comportamento mais desafiador para o jogador
  - Melhor integração com o sistema existente

- **Performance**
  - Limitação de iterações para evitar lag
  - Otimização de algoritmos de pathfinding
  - Sistema de cache para posições anteriores

### 🏗️ Arquitetura
- **Nova classe `ImprovedGhostAI`**
  - Separação clara de responsabilidades
  - Métodos especializados para diferentes funcionalidades
  - Integração perfeita com o sistema existente

- **Método `enhanced_ghost_intelligence`**
  - Substitui o sistema de IA original
  - Mantém compatibilidade total com funcionalidades existentes
  - Suporte completo a múltiplos jogadores

### 📚 Documentação
- **README.md atualizado**
  - Nova seção sobre sistema de IA avançado
  - Documentação dos comportamentos de cada fantasma
  - Explicação das melhorias implementadas

## [1.2.0] - 2024-12-19

### ✨ Adicionado
- **Sistema de menu e seleção de modo**
  - Menu interativo para seleção de modo de jogo
  - Suporte a múltiplos jogadores (Player 1, 2, 3)
  - Contagem regressiva visual antes do início do jogo
  - Navegação intuitiva com setas e Enter
  - Controles específicos para cada modo de jogo

- **Melhorias na experiência do usuário**
  - Contagem regressiva de 2 segundos antes de iniciar
  - Feedback visual melhorado no menu
  - Instruções de controles exibidas no menu
  - Sistema de reset automático do menu

## [1.1.0] - 2024-12-19

### ✨ Adicionado
- **Sistema completo de controles Xbox e genéricos**
  - Detecção automática de controles conectados
  - Suporte para Xbox 360/One/Series X|S
  - Suporte para PlayStation 3/4/5
  - Suporte para controles genéricos USB/Bluetooth
  - Mapeamento inteligente de botões
  - Zona morta configurável para analógicos

- **Feedback visual de controles**
  - Indicador de controle conectado na tela
  - Instruções de controles exibidas dinamicamente
  - Status do tipo de controle (Xbox/Genérico)

- **Documentação completa**
  - Guia de controles detalhado
  - Guia de instalação para diferentes sistemas
  - Documentação técnica da arquitetura
  - Índice de documentação

### 🔧 Melhorado
- **Sistema de input unificado**
  - Processamento simultâneo de teclado e controles
  - Método `_set_direction()` para centralizar lógica de movimento
  - Tratamento robusto de erros de controle

- **Estrutura do projeto**
  - Organização da documentação em pasta `docs/`
  - Separação clara de responsabilidades
  - Código mais limpo e manutenível
  - Adicionado arquivo `menu.py` para sistema de menu

### 🐛 Corrigido
- **Remoção de logs desnecessários**
  - Removidos prints de debug do sistema de controles
  - Tratamento silencioso de erros de inicialização
  - Código mais limpo para produção

### 📚 Documentação
- **README.md atualizado**
  - Seção de controles expandida
  - Links para documentação completa
  - Lista de controles suportados
  - Documentação do sistema de menu

- **Nova documentação**
  - `docs/README.md` - Documentação principal
  - `docs/controles.md` - Guia de controles
  - `docs/instalacao.md` - Guia de instalação
  - `docs/arquitetura.md` - Documentação técnica
  - `docs/index.md` - Índice da documentação

## [1.0.0] - 2024-12-19

### ✨ Adicionado
- **Jogo Pac-Man completo**
  - Lógica de jogo baseada no original
  - Sistema de pontuação e vidas
  - IA dos fantasmas com diferentes comportamentos
  - Modo inofensivo (power pellets)
  - Animações fluidas dos personagens

- **Sistema de controles básico**
  - Suporte a teclado (WASD/Setas)
  - Controles básicos (R para reiniciar, ESC para sair)

- **Sistema de sprites**
  - Sprites do Pac-Man (17 frames de animação)
  - Sprites dos fantasmas (4 cores, 2 frames cada)
  - Sprites de fantasma inofensivo
  - Sistema de rotação baseado na direção

- **Física e colisões**
  - Sistema de colisão com paredes
  - Sistema de túneis laterais
  - Colisão entre Pac-Man e fantasmas
  - Sistema de curvas para mudança de direção

### 🏗️ Arquitetura
- **Estrutura orientada a objetos**
  - Classe `PacMan` principal
  - Sistema de constantes centralizado
  - Separação clara de responsabilidades

- **Sistema de escala**
  - Fator de escala configurável
  - Redimensionamento automático de elementos
  - Compatibilidade com diferentes resoluções

### 📁 Estrutura do Projeto
```
pacman/
├── src/
│   ├── game.py         # Lógica principal
│   ├── constants.py    # Configurações
│   └── __init__.py     # Pacote Python
├── img/                # Sprites e imagens
├── main.py             # Ponto de entrada
├── requirements.txt    # Dependências
└── README.md           # Documentação básica
```

---

## Formato do Changelog

Este projeto segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) e usa [Semantic Versioning](https://semver.org/lang/pt-BR/).

### Tipos de Mudanças
- **✨ Adicionado** - para novas funcionalidades
- **🔧 Melhorado** - para mudanças em funcionalidades existentes
- **🐛 Corrigido** - para correções de bugs
- **📚 Documentação** - para mudanças na documentação
- **🏗️ Arquitetura** - para mudanças na estrutura do projeto
- **📁 Estrutura** - para mudanças na organização de arquivos
