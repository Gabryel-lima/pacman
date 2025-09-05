#!/usr/bin/env python3
"""
Pac-Man Game - Python/pygame version
Baseado na lógica do arquivo Pac_Man.py
"""

import pygame
import sys
from src.game import PacMan

def main():
    """Função principal do jogo"""
    # Inicializar pygame
    pygame.init()
    
    # Criar instância do jogo com escala 26
    jogo = PacMan(26)
    
    # Executar o jogo
    jogo.run()
    return 0

if __name__ == "__main__":
    sys.exit(main())
