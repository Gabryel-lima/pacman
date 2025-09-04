#include "pacman.h"
#include <iostream>

int main(int, char**) {
    Game game;
    
    if (!game.init()) {
        std::cerr << "Falha ao inicializar o jogo!" << std::endl;
        return -1;
    }
    
    game.run();
    
    return 0;
}
