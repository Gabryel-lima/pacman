# Pac-Man SDL2

Este projeto é uma replicação do famoso jogo Pac-Man utilizando C++ e a biblioteca SDL2.
O jogo foi reescrito para ser mais moderno e multiplataforma.

## Tecnologias utilizadas

* **C++17**: Linguagem de programação principal
* **SDL2**: Biblioteca gráfica multiplataforma para renderização e eventos
* **SDL2_image**: Extensão do SDL2 para carregar imagens PNG
* **Makefile**: Sistema de build nativo e eficiente

## Características

* Interface gráfica moderna com SDL2
* Movimento suave dos personagens
* Sistema de pontuação
* Power pellets que permitem comer fantasmas
* Detecção de colisão
* Estados de jogo (início, jogando, game over, vitória)

## Pré-requisitos

Para compilar e executar o jogo, você precisa ter instalado:

* Make
* SDL2 development libraries
* SDL2_image development libraries
* Compilador C++ com suporte ao C++17 (g++ ou clang++)

### Instalação automática das dependências

O Makefile inclui comandos para instalar automaticamente as dependências:

#### Ubuntu/Debian
```bash
make install-deps
```

#### Fedora/CentOS/RHEL
```bash
make install-deps-fedora
```

#### Arch Linux
```bash
make install-deps-arch
```

### Instalação manual

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install libsdl2-dev libsdl2-image-dev build-essential
```

#### Fedora/CentOS/RHEL
```bash
sudo dnf install SDL2-devel SDL2_image-devel gcc-c++
```

#### Arch Linux
```bash
sudo pacman -S sdl2 sdl2_image gcc
```

## Como compilar e executar

### Método rápido
```bash
git clone https://github.com/gab-braga/pacman.git
cd pacman
make run
```

### Passo a passo

1. Clone este repositório:
```bash
git clone https://github.com/gab-braga/pacman.git
cd pacman
```

2. Verifique as dependências (opcional):
```bash
make check-deps
```

3. Compile o projeto:
```bash
make
```

4. Execute o jogo:
```bash
./pacman_game
```

### Comandos úteis do Makefile

* `make` - Compila o jogo (versão release)
* `make debug` - Compila com símbolos de debug
* `make run` - Compila e executa automaticamente
* `make clean` - Remove arquivos de build
* `make help` - Mostra todos os comandos disponíveis

## Controles do jogo

* **Setas direcionais**: Movem o Pac-Man pela tela
* **P**: Inicia o jogo / Reinicia após game over
* **ESC**: Sair do jogo

## Estrutura do projeto

```
pacman/
├── src/
│   ├── main.cpp        # Ponto de entrada do programa
│   ├── game.cpp        # Implementação principal da classe Game
│   ├── pacman.cpp      # Lógica específica do jogo Pac-Man
│   └── pacman.h        # Definições e declarações
├── images/             # Texturas e sprites do jogo
├── Makefile            # Sistema de build
└── README.md           # Este arquivo
```

## Melhorias implementadas

* **Arquitetura orientada a objetos**: Código mais organizado e manutenível
* **SDL2**: Melhor performance e compatibilidade multiplataforma
* **Gerenciamento automático de recursos**: Prevenção de vazamentos de memória
* **Sistema de build eficiente**: Makefile com comandos úteis e detecção automática de dependências
* **Código C++ moderno**: Uso de recursos do C++17

## Visualização

![Pac-Man](https://github.com/gab-braga/pacman/blob/master/pacman.gif)

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.