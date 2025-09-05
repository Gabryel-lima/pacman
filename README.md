# Pac-Man pygame-ce

Este projeto é uma replicação do famoso jogo Pac-Man utilizando Python e a biblioteca pygame-ce.
O jogo foi convertido de C++/SDL2 para Python para ser mais acessível e fácil de modificar.

## Tecnologias utilizadas

* **Python 3.8+**: Linguagem de programação principal
* **pygame-ce**: Biblioteca gráfica moderna para jogos em Python
* **Type hints**: Para melhor documentação e desenvolvimento

## Características

* Interface gráfica moderna com pygame-ce
* Movimento suave dos personagens
* Sistema de pontuação
* Power pellets que permitem comer fantasmas
* Detecção de colisão
* Estados de jogo (início, jogando, game over, vitória)
* Código Python orientado a objetos e bem estruturado

## Pré-requisitos

Para executar o jogo, você precisa ter instalado:

* Python 3.8 ou superior
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
git clone https://github.com/gab-braga/pacman.git
cd pacman
pip install -r requirements.txt
python main.py
```

### Passo a passo

1. Clone este repositório:
```bash
git clone https://github.com/gab-braga/pacman.git
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

* **Setas direcionais**: Movem o Pac-Man pela tela
* **P**: Inicia o jogo / Reinicia após game over
* **ESC**: Sair do jogo

## Estrutura do projeto

```
pacman/
├── src/
│   ├── __init__.py     # Pacote Python
│   ├── game.py         # Classe principal do jogo
│   ├── entities.py     # Classes Pacman, Phantom e Scene
│   └── constants.py    # Constantes e configurações do jogo
├── images/             # Sprites e imagens do jogo
├── main.py             # Ponto de entrada do programa
├── requirements.txt    # Dependências Python
└── README.md           # Este arquivo
```

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

![Pac-Man](https://github.com/gab-braga/pacman/blob/master/pacman.gif)

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.