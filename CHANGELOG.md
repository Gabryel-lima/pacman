# Changelog - Pac-Man

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

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
