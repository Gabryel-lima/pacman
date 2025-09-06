# Pac-Man pygame-ce

Este projeto é uma replicação do famoso jogo Pac-Man utilizando Python e a biblioteca pygame-ce.
O jogo foi convertido de C++/SDL2 para Python para ser mais acessível e fácil de modificar.

## Tecnologias utilizadas

* **Python 3.7+**: Linguagem de programação principal
* **pygame-ce**: Biblioteca gráfica moderna para jogos em Python
* **Type hints**: Para melhor documentação e desenvolvimento

## Características

* Interface gráfica moderna com pygame-ce
* Movimento suave dos personagens
* Sistema de pontuação
* Power pellets que permitem comer fantasmas
* Detecção de colisão
* Estados de jogo (início, jogando, game over, vitória)
* **🎮 Suporte completo a controles Xbox e genéricos**
* **🔧 Detecção automática de controles**
* **📱 Feedback visual de controles conectados**
* **🎯 Sistema de seleção de modo de jogo**
* **⏱️ Contagem regressiva antes do início**
* **👥 Suporte a múltiplos jogadores (Player 1, 2, 3)**
* Código Python orientado a objetos e bem estruturado

## Pré-requisitos

Para executar o jogo, você precisa ter instalado:

* Python 3.7 ou superior
* pygame-ce (instalado automaticamente via pip)

### Instalação das dependências

```bash
pip install -r requirements.txt
```

Ou instalar diretamente:

```bash
pip install pygame-ce
```

## Como executar

### Método rápido
```bash
git clone https://github.com/gabryel-lima/pacman.git
cd pacman
pip install -r requirements.txt
python main.py
```

### Passo a passo

1. Clone este repositório:
```bash
git clone https://github.com/gabryel-lima/pacman.git
cd pacman
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o jogo:
```bash
python main.py
```

## Controles do jogo

### Teclado
* **WASD** ou **Setas direcionais**: Movem o Pac-Man pela tela
* **R**: Reinicia o jogo
* **ESC**: Sair do jogo
* **ENTER**: Confirmar seleção no menu

### Controles Xbox/Genéricos
* **D-pad** ou **Analógico esquerdo**: Movem o Pac-Man
* **Botão Start**: Reinicia o jogo
* **ESC** (teclado): Sair do jogo

### Modos de Jogo
* **Player 1**: Controles WASD
* **Player 2**: Setas direcionais
* **Player 3**: Teclas IJKL

> 📖 **[Documentação completa de controles](docs/controles.md)**

### Controles Suportados
- ✅ **Xbox 360/One/Series X|S** (USB e Bluetooth)
- ✅ **PlayStation 3/4/5**
- ✅ **Controles genéricos USB/Bluetooth**
- ✅ **Detecção automática**
- ✅ **Múltiplos controles simultâneos**

## Estrutura do projeto

```
pacman/
├── src/
│   ├── __init__.py     # Pacote Python
│   ├── game.py         # Classe principal do jogo
│   ├── controller.py   # Sistema de controles
│   ├── menu.py         # Sistema de menu e seleção de modo
│   └── constants.py    # Constantes e configurações do jogo
├── img/                # Sprites e imagens do jogo
├── docs/               # Documentação completa
│   ├── README.md       # Documentação principal
│   ├── index.md        # Índice da documentação
│   ├── controles.md    # Guia de controles
│   ├── instalacao.md   # Guia de instalação
│   └── arquitetura.md  # Documentação técnica
├── main.py             # Ponto de entrada do programa
├── requirements.txt    # Dependências Python
├── CHANGELOG.md        # Histórico de mudanças
└── README.md           # Este arquivo
```

## 📚 Documentação

- 📖 **[Índice da Documentação](docs/index.md)** - Navegação completa
- 📋 **[Documentação Principal](docs/README.md)** - Visão geral completa
- 🎮 **[Guia de Controles](docs/controles.md)** - Como usar controles Xbox/genéricos
- ⚙️ **[Guia de Instalação](docs/instalacao.md)** - Instalação detalhada
- 🏗️ **[Arquitetura](docs/arquitetura.md)** - Documentação técnica

## 🎮 Novas Funcionalidades

### Sistema de Menu e Seleção de Modo
* **Menu interativo**: Seleção de modo de jogo antes de iniciar
* **Múltiplos jogadores**: Suporte a Player 1, 2 e 3
* **Contagem regressiva**: Preparação visual antes do início
* **Navegação intuitiva**: Setas para navegar, Enter para confirmar

### Sistema de Controles Avançado
* **Detecção automática**: Reconhece controles Xbox e genéricos automaticamente
* **Mapeamento inteligente**: Adapta-se a diferentes tipos de controle
* **Feedback visual**: Mostra status do controle na tela
* **Múltiplos controles**: Suporta até 4 controles simultâneos
* **Zona morta configurável**: Evita movimento acidental nos analógicos

### Controles Suportados
- **Xbox**: 360, One, Series X|S (USB e Bluetooth)
- **PlayStation**: PS3, PS4, PS5
- **Genéricos**: Logitech, USB, Bluetooth compatíveis

## ✨ Correções Implementadas

Este projeto foi completamente revisado e corrigido para garantir funcionalidade perfeita:

### 🔧 Correções de Sprites
* **Caminhos absolutos**: Corrigidos os caminhos dos sprites para funcionar em qualquer diretório
* **Indexação do Pacman**: Corrigida a lógica de seleção de sprites baseada em direção e animação
* **Indexação dos fantasmas**: Implementado sistema correto para sprites baseado em ID, direção e status
* **Mapeamento do cenário**: Corrigido mapeamento entre tipos de cena e sprites correspondentes

### 🎮 Correções de Lógica
* **Inicialização**: Corrigidas posições iniciais do Pacman e fantasmas
* **Movimento**: Melhorada lógica de movimento com interpolação suave
* **Colisões**: Sistema de colisão mais preciso entre Pacman e fantasmas
* **Estados dos fantasmas**: Implementados corretamente os estados CAPTURE, ESCAPE e DEAD
* **Ressurreição**: Fantasmas mortos ressuscitam após um tempo determinado

### 🖥️ Melhorias de Interface
* **HUD**: Adicionado sistema de pontuação em tempo real
* **Informações**: Exibição de moedas restantes e status do poder
* **Feedback visual**: Melhor feedback para ações do jogador

## Melhorias implementadas na versão Python

* **Arquitetura orientada a objetos**: Código mais organizado e manutenível
* **pygame-ce**: Biblioteca moderna e bem mantida para jogos em Python
* **Type hints**: Melhor documentação e desenvolvimento com verificação de tipos
* **Código Python limpo**: Mais legível e fácil de modificar que a versão C++
* **Instalação simples**: Apenas um comando pip para instalar dependências
* **Multiplataforma**: Funciona em Windows, Linux e macOS sem compilação

## Visualização

![Pac-Man](https://github.com/gabryel-lima/pacman/blob/master/pacman.gif)

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.