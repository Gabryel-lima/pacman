# Controles do Pac-Man

Este jogo suporta tanto controles de teclado quanto controles de Xbox e controles genéricos, com detecção automática e mapeamento inteligente de botões.

## Controles de Teclado

### No Menu
- **Setas (↑/↓)**: Navegar entre opções
- **ENTER**: Confirmar seleção
- **ESC**: Sair do jogo

### No Jogo
- **WASD** ou **Setas**: Mover o Pac-Man
- **R**: Reiniciar o jogo
- **ESC**: Sair do jogo

## Controles de Xbox/Genéricos

### No Menu
- **D-pad (↑/↓)**: Navegar entre opções
- **A**: Confirmar seleção
- **ESC** (teclado): Sair do jogo

### No Jogo
- **D-pad**: Mover o Pac-Man (cima, baixo, esquerda, direita)
- **Analógico esquerdo**: Mover o Pac-Man (mais preciso que o D-pad)
- **Start**: Reiniciar o jogo
- **ESC** (teclado): Sair do jogo

## Modos de Jogo

O jogo oferece três modos diferentes, cada um com controles específicos:

### Player 1
- **Controles**: WASD
- **Descrição**: Modo padrão para um jogador

### Player 2
- **Controles**: Setas direcionais
- **Descrição**: Modo alternativo para um jogador

### Player 3
- **Controles**: IJKL
- **Descrição**: Modo adicional para um jogador

> **Nota**: Atualmente, todos os modos são para um jogador. Os diferentes controles permitem personalizar a experiência de jogo.

## Detecção Automática

O jogo detecta automaticamente:
- **Controles Xbox**: Microsoft Xbox controllers, XInput devices
- **Controles genéricos**: PlayStation, Logitech, e outros controles compatíveis
- **Múltiplos controles**: Suporta até 4 controles simultâneos (usa o primeiro conectado)

## Feedback Visual

- **Controle conectado**: Mostra o nome e tipo do controle no canto superior esquerdo em verde
- **Sem controle**: Mostra instruções do teclado em amarelo
- **Instruções**: Lista de controles disponíveis é exibida na tela

## Configurações Técnicas

- **Zona morta**: 0.3 (30%) para analógicos - evita movimento acidental
- **Detecção**: Verifica novos controles a cada frame
- **Compatibilidade**: Funciona com controles USB e Bluetooth

## Solução de Problemas

### Controle não detectado
1. Verifique se o controle está conectado via USB ou Bluetooth
2. Teste o controle em outros jogos para confirmar funcionamento
3. Reinicie o jogo após conectar o controle

### Movimento impreciso
- Use o D-pad para movimento mais preciso
- O analógico tem zona morta configurada para evitar movimento acidental

### Múltiplos controles
- O jogo usa automaticamente o primeiro controle detectado
- Para trocar de controle, desconecte o atual e conecte o desejado

## Suporte a Controles

### Xbox Controllers
- Xbox 360 (USB/Wireless)
- Xbox One (USB/Bluetooth)
- Xbox Series X/S (USB/Bluetooth)
- Controles compatíveis com XInput

### Controles Genéricos
- PlayStation 3/4/5
- Logitech F310/F510/F710
- Controles genéricos USB
- Controles Bluetooth compatíveis

## Desenvolvimento

O sistema de controles foi implementado usando:
- `pygame.joystick` para detecção e input
- Mapeamento automático de botões
- Suporte a múltiplos tipos de controle
- Feedback visual em tempo real
