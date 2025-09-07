# 🎮 Pac-Man Python

Uma implementação moderna do clássico jogo Pac-Man em Python usando pygame-ce, com suporte completo a controles Xbox e múltiplos jogadores.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![pygame-ce](https://img.shields.io/badge/pygame--ce-2.4+-green.svg)](https://github.com/pygame-community/pygame-ce)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Características Principais

- 🎮 **Suporte completo a controles Xbox/PlayStation/genéricos**
- 👥 **Múltiplos jogadores** (até 3 jogadores simultâneos)
- 🎯 **Sistema de menu interativo** com seleção de modo
- 🔧 **Detecção automática de controles** conectados
- 📱 **Feedback visual** de status dos controles
- ⏱️ **Contagem regressiva** antes do início do jogo
- 🧠 **IA avançada dos fantasmas** com pathfinding inteligente
- 🎭 **Comportamentos distintos** para cada fantasma
- 🏗️ **Código orientado a objetos** bem estruturado
- 🎨 **Interface gráfica moderna** com pygame-ce

## 🚀 Início Rápido

### Instalação e Execução

```bash
# Clone o repositório
git clone https://github.com/gabryel-lima/pacman.git
cd pacman

# Instale as dependências
pip install -r requirements.txt

# Execute o jogo
python main.py
```

### 🎮 Controles

| Ação | Teclado | Controle |
|------|---------|----------|
| Mover | WASD / Setas | D-pad / Analógico |
| Reiniciar | R | Start |
| Sair | ESC | ESC (teclado) |
| Confirmar | ENTER | A / X |

**Modos de Jogo:**
- **Player 1**: WASD
- **Player 2**: Setas direcionais  
- **Player 3**: IJKL

## 📋 Pré-requisitos

- **Python 3.7+**
- **pygame-ce 2.4+** (instalado automaticamente)

## 🎯 Criando Executáveis

Para distribuir o jogo, você pode criar executáveis autocontidos:

```bash
# Método automatizado (recomendado)
python build.py

# Ou manualmente para Linux
pyinstaller pacman.spec --clean
```

> 📦 **[Guia completo de build](docs/build.md)** - Instruções detalhadas para Windows e Linux

## 🎮 Controles Suportados

- ✅ **Xbox 360/One/Series X|S** (USB e Bluetooth)
- ✅ **PlayStation 3/4/5**
- ✅ **Controles genéricos USB/Bluetooth**
- ✅ **Detecção automática**
- ✅ **Múltiplos controles simultâneos**

## 📚 Documentação Completa

- 📖 **[Índice da Documentação](docs/index.md)** - Navegação completa
- 🚀 **[Guia de Início Rápido](docs/quick-start.md)** - Comece a jogar em 5 minutos
- 🎮 **[Guia de Controles](docs/controles.md)** - Controles Xbox/PlayStation/genéricos
- 📦 **[Guia de Build](docs/build.md)** - Criar executáveis para Windows/Linux
- ⚙️ **[Instalação Detalhada](docs/instalacao.md)** - Instalação passo a passo
- 🏗️ **[Arquitetura](docs/arquitetura.md)** - Documentação técnica

## 📁 Estrutura do Projeto

```
pacman/
├── src/                    # Código fonte do jogo
│   ├── game.py            # Lógica principal do jogo
│   ├── controller.py      # Sistema de controles
│   ├── menu.py            # Sistema de menu
│   └── constants.py       # Configurações
├── docs/                  # Documentação completa
├── img/                   # Sprites e imagens
├── main.py               # Ponto de entrada
├── build.py              # Script de build automatizado
├── pacman.spec           # Configuração PyInstaller
└── requirements.txt      # Dependências
```

## ✨ Funcionalidades

### 🧠 Sistema de IA Avançado dos Fantasmas
- **Pathfinding inteligente** com algoritmos BFS e A*
- **Comportamentos distintos** para cada fantasma:
  - 🔵 **Azul**: Modo scatter (vai para cantos)
  - 🟠 **Laranja**: Modo chase com distância inteligente
  - 🩷 **Rosa**: Modo ambush (intercepta o Pacman)
  - 🔴 **Vermelho**: Modo aggressive (perseguição direta)
- **Predição de movimento** do Pacman
- **Sistema anti-travamento** para evitar fantasmas presos
- **Comportamento cooperativo** entre fantasmas
- **Ciclos dinâmicos** de comportamento (scatter ↔ chase)

### 🎮 Sistema de Controles Avançado
- **Detecção automática** de controles Xbox/PlayStation/genéricos
- **Múltiplos jogadores** simultâneos (até 3)
- **Feedback visual** de status dos controles
- **Mapeamento inteligente** para diferentes tipos de controle

### 🎯 Sistema de Menu
- **Menu interativo** com seleção de modo de jogo
- **Contagem regressiva** antes do início
- **Navegação intuitiva** com controles

### 🏗️ Qualidade do Código
- **Arquitetura orientada a objetos** bem estruturada
- **Type hints** para melhor desenvolvimento
- **Código Python limpo** e manutenível
- **Multiplataforma** (Windows, Linux, macOS)

## 🎥 Demonstração

![Pac-Man](https://github.com/gabryel-lima/pacman/blob/master/pacman.gif)

## 📄 Licença

Este projeto está disponível sob a [Licença MIT](LICENSE).

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja o [guia de contribuição](CONTRIBUTING.md) para mais detalhes.

---

**Desenvolvido com ❤️ em Python**