#!/usr/bin/env python3
"""
Pac-Man Game - Python/pygame-ce version
Conversão do jogo Pac-Man de C++/SDL2 para Python/pygame-ce
"""

import pygame
import sys
from src.game import Game

def main():
    """Função principal do jogo"""
    game = Game()
    
    if not game.init():
        print("Falha ao inicializar o jogo!")
        return -1
    
    game.run()
    return 0

if __name__ == "__main__":
    sys.exit(main())
