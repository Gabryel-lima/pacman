#include "pacman.h"
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include <iostream>

// Implementação dos métodos do jogo

Scene* Game::generateScene() {
    Scene* scene = new Scene();
    scene->coins = 0;
    
    // Copiar o mapa de posições e gerar o mapa lógico
    for (int i = 0; i < MAP_SIZE; i++) {
        for (int j = 0; j < MAP_SIZE; j++) {
            int sceneType = SCENES_POSITION[i][j];
            
            if (sceneType == 0) {  // Empty space
                scene->map[i][j] = FREE_WAY;
            } else if (sceneType == 1) {  // Coin
                scene->map[i][j] = COIN_WAY;
                scene->coins++;
            } else if (sceneType == 2) {  // Power pellet
                scene->map[i][j] = POWER_WAY;
                scene->coins++;
            } else {  // Wall/obstacle
                scene->map[i][j] = OBSTACLE;
            }
        }
    }
    
    scene->vertexCount = 0;
    scene->graph = nullptr;
    
    return scene;
}

Pacman* Game::createPacman(int x, int y) {
    Pacman* pac = new Pacman();
    
    pac->status = 0;
    pac->xi = pac->x = x;
    pac->yi = pac->y = y;
    pac->xl = x;
    pac->yl = y;
    pac->direction = RIGHT;
    pac->nextDirection = RIGHT;  // Inicializar próxima direção
    pac->step = 0;
    pac->partial = 0;
    pac->points = 0;
    pac->power = 0;
    pac->life = 1;
    pac->deadAnimation = 0;
    
    return pac;
}

Phantom* Game::createPhantom(int x, int y, int id, int direction) {
    Phantom* phantom = new Phantom();
    
    phantom->status = CAPTURE;
    phantom->xi = phantom->x = x;
    phantom->yi = phantom->y = y;
    phantom->xl = x;
    phantom->yl = y;
    phantom->direction = direction;
    phantom->step = 0;
    phantom->partial = 0;
    phantom->life = 1;
    phantom->isCrossing = 0;
    phantom->isReturn = 0;
    phantom->path = nullptr;
    phantom->indexCurrent = 0;
    phantom->id = id;
    
    return phantom;
}

void Game::drawScene() {
    for (int i = 0; i < MAP_SIZE; i++) {
        for (int j = 0; j < MAP_SIZE; j++) {
            SDL_Rect destRect = {j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE};
            
            int sceneType = SCENES_POSITION[i][j];
            
            // Desenhar fundo vazio primeiro
            SDL_RenderCopy(renderer, sceneTextures[0], nullptr, &destRect);
            
            // Desenhar elementos específicos
            if (sceneType >= 1 && sceneType < (int)sceneTextures.size()) {
                // Se é uma moeda ou power pellet, verificar se ainda não foi coletada
                if ((sceneType == 1 && scene->map[i][j] == COIN_WAY) ||
                    (sceneType == 2 && scene->map[i][j] == POWER_WAY)) {
                    SDL_RenderCopy(renderer, sceneTextures[sceneType], nullptr, &destRect);
                } else if (sceneType > 2) {  // Paredes e outros elementos
                    SDL_RenderCopy(renderer, sceneTextures[sceneType], nullptr, &destRect);
                }
            }
        }
    }
}

void Game::drawPacman() {
    if (!pacman) return;
    
    // Validar coordenadas e partial antes de desenhar
    int safeX = pacman->x;
    int safeY = pacman->y;
    int safePartial = pacman->partial;
    
    // Garantir que as coordenadas estejam dentro dos limites
    if (safeX < 0) safeX = 0;
    if (safeX >= MAP_SIZE) safeX = MAP_SIZE - 1;
    if (safeY < 0) safeY = 0;
    if (safeY >= MAP_SIZE) safeY = MAP_SIZE - 1;
    
    // Garantir que partial esteja no range válido
    if (safePartial < 0) safePartial = 0;
    if (safePartial > 4) safePartial = 4;
    
    // Calcular offset baseado na direção
    int offsetX = 0, offsetY = 0;
    if (safePartial > 0) {
        int offset = safePartial * CELL_SIZE / 5;
        switch (pacman->direction) {
            case RIGHT: offsetX = offset; break;
            case LEFT:  offsetX = -offset; break;
            case DOWN:  offsetY = offset; break;
            case UP:    offsetY = -offset; break;
        }
    }
    
    SDL_Rect destRect = {
        safeX * CELL_SIZE + offsetX,
        safeY * CELL_SIZE + offsetY,
        CELL_SIZE,
        CELL_SIZE
    };
    
    // Selecionar a textura baseada na direção e animação
    int textureIndex = pacman->direction * 3 + (pacman->step % 3);
    if (textureIndex < (int)pacmanTextures.size()) {
        SDL_RenderCopy(renderer, pacmanTextures[textureIndex], nullptr, &destRect);
    }
}

void Game::drawPhantom(Phantom* phantom) {
    if (!phantom) return;
    
    // Validar coordenadas e partial antes de desenhar
    int safeX = phantom->x;
    int safeY = phantom->y;
    int safePartial = phantom->partial;
    
    // Garantir que as coordenadas estejam dentro dos limites
    if (safeX < 0) safeX = 0;
    if (safeX >= MAP_SIZE) safeX = MAP_SIZE - 1;
    if (safeY < 0) safeY = 0;
    if (safeY >= MAP_SIZE) safeY = MAP_SIZE - 1;
    
    // Garantir que partial esteja no range válido
    if (safePartial < 0) safePartial = 0;
    if (safePartial > 4) safePartial = 4;
    
    // Calcular offset baseado na direção
    int offsetX = 0, offsetY = 0;
    if (safePartial > 0) {
        int offset = safePartial * CELL_SIZE / 5;
        switch (phantom->direction) {
            case RIGHT: offsetX = offset; break;
            case LEFT:  offsetX = -offset; break;
            case DOWN:  offsetY = offset; break;
            case UP:    offsetY = -offset; break;
        }
    }
    
    SDL_Rect destRect = {
        safeX * CELL_SIZE + offsetX,
        safeY * CELL_SIZE + offsetY,
        CELL_SIZE,
        CELL_SIZE
    };
    
    // Selecionar a textura baseada no ID e status
    int textureIndex = phantom->id;
    if (phantom->status == ESCAPE) {
        textureIndex += 16;  // Texturas de fuga
    }
    
    if (textureIndex < (int)phantomTextures.size()) {
        SDL_RenderCopy(renderer, phantomTextures[textureIndex], nullptr, &destRect);
    }
}

void Game::drawGameStart() {
    if (gameStartTexture) {
        SDL_RenderCopy(renderer, gameStartTexture, nullptr, nullptr);
    }
}

void Game::drawGameOver() {
    if (gameOverTexture) {
        SDL_RenderCopy(renderer, gameOverTexture, nullptr, nullptr);
    }
}

void Game::drawGameWon() {
    if (gameWonTexture) {
        SDL_RenderCopy(renderer, gameWonTexture, nullptr, nullptr);
    }
}

void Game::alterDirectionPacman(int direction) {
    if (!pacman || !scene) return;
    
    int newX = pacman->x + DIRECTIONS[direction].x;
    int newY = pacman->y + DIRECTIONS[direction].y;
    
    // Aplicar wraparound horizontal primeiro (apenas para direções horizontais)
    if (direction == LEFT || direction == RIGHT) {
        if (newX < 0) {
            newX = MAP_SIZE - 1;
        } else if (newX >= MAP_SIZE) {
            newX = 0;
        }
    }
    
    // Verificar limites verticais
    if (newY >= 0 && newY < MAP_SIZE) {
        // Verificar se não é obstáculo
        if (scene->map[newY][newX] != OBSTACLE) {
            pacman->nextDirection = direction;
        }
    }
}

void Game::movePacman() {
    if (!pacman || !scene) return;
    
    // Validar e corrigir partial se necessário
    if (pacman->partial < 0) pacman->partial = 0;
    if (pacman->partial > 5) pacman->partial = 0;
    
    pacman->partial++;
    
    if (pacman->partial >= 5) {  // Movimento completo
        // Aplicar a próxima direção se for diferente da atual
        if (pacman->nextDirection != pacman->direction) {
            pacman->direction = pacman->nextDirection;
        }
        
        pacman->partial = 0;  // Reset seguro
        pacman->xl = pacman->x;
        pacman->yl = pacman->y;
        
        // Validar coordenadas atuais
        if (pacman->x < 0) pacman->x = 0;
        if (pacman->x >= MAP_SIZE) pacman->x = MAP_SIZE - 1;
        if (pacman->y < 0) pacman->y = 0;
        if (pacman->y >= MAP_SIZE) pacman->y = MAP_SIZE - 1;
        
        int newX = pacman->x + DIRECTIONS[pacman->direction].x;
        int newY = pacman->y + DIRECTIONS[pacman->direction].y;
        
        // Aplicar wraparound horizontal primeiro (apenas para direções horizontais)
        if (pacman->direction == LEFT || pacman->direction == RIGHT) {
            if (newX < 0) {
                newX = MAP_SIZE - 1;
            } else if (newX >= MAP_SIZE) {
                newX = 0;
            }
        }
        
        // Verificar se pode mover
        bool canMove = false;
        
        // Verificar limites verticais
        if (newY >= 0 && newY < MAP_SIZE) {
            // Verificar se não é obstáculo
            if (scene->map[newY][newX] != OBSTACLE) {
                canMove = true;
            }
        }
        
        if (canMove) {
            pacman->x = newX;
            pacman->y = newY;
            
            // Coletar moedas ou power pellets
            if (scene->map[newY][newX] == COIN_WAY) {
                scene->map[newY][newX] = FREE_WAY;
                pacman->points += 10;
                scene->coins--;
            } else if (scene->map[newY][newX] == POWER_WAY) {
                scene->map[newY][newX] = FREE_WAY;
                pacman->points += 50;
                pacman->power = 100;  // Duração do poder
                scene->coins--;
            }
        }
        
        pacman->step++;
    }
    
    // Decrementar poder
    if (pacman->power > 0) {
        pacman->power--;
    }
}

void Game::movePhantom(Phantom* phantom) {
    if (!phantom || !scene) return;
    
    // Validar e corrigir partial se necessário
    if (phantom->partial < 0) phantom->partial = 0;
    if (phantom->partial > 5) phantom->partial = 0;
    
    phantom->partial++;
    
    if (phantom->partial >= 5) {  // Movimento completo
        phantom->partial = 0;  // Reset seguro
        phantom->xl = phantom->x;
        phantom->yl = phantom->y;
        
        // Validar coordenadas atuais
        if (phantom->x < 0) phantom->x = 0;
        if (phantom->x >= MAP_SIZE) phantom->x = MAP_SIZE - 1;
        if (phantom->y < 0) phantom->y = 0;
        if (phantom->y >= MAP_SIZE) phantom->y = MAP_SIZE - 1;
        
        // Lógica simples de movimento para os fantasmas
        // Tentar mover na direção atual
        int newX = phantom->x + DIRECTIONS[phantom->direction].x;
        int newY = phantom->y + DIRECTIONS[phantom->direction].y;
        
        // Aplicar wraparound horizontal primeiro (apenas para direções horizontais)
        if (phantom->direction == LEFT || phantom->direction == RIGHT) {
            if (newX < 0) {
                newX = MAP_SIZE - 1;
            } else if (newX >= MAP_SIZE) {
                newX = 0;
            }
        }
        
        // Verificar se pode mover na direção atual
        bool canMove = false;
        
        // Verificar limites verticais
        if (newY >= 0 && newY < MAP_SIZE) {
            // Verificar se não é obstáculo
            if (scene->map[newY][newX] != OBSTACLE) {
                canMove = true;
            }
        }
        
        // Se não pode mover, escolher nova direção
        if (!canMove) {
            // Tentar outras direções
            for (int i = 0; i < 4; i++) {
                int testX = phantom->x + DIRECTIONS[i].x;
                int testY = phantom->y + DIRECTIONS[i].y;
                
                // Aplicar wraparound horizontal primeiro (apenas para direções horizontais)
                if (i == LEFT || i == RIGHT) {
                    if (testX < 0) testX = MAP_SIZE - 1;
                    if (testX >= MAP_SIZE) testX = 0;
                }
                
                // Verificar limites verticais
                if (testY >= 0 && testY < MAP_SIZE) {
                    // Verificar se pode mover nesta direção
                    if (scene->map[testY][testX] != OBSTACLE) {
                        phantom->direction = i;
                        newX = testX;
                        newY = testY;
                        canMove = true;
                        break;
                    }
                }
            }
        }
        
        // Só mover se for possível
        if (canMove) {
            phantom->x = newX;
            phantom->y = newY;
        }
        
        phantom->step++;
        
        // Verificar colisão com Pacman
        if (phantom->x == pacman->x && phantom->y == pacman->y) {
            if (pacman->power > 0) {
                // Pacman come o fantasma
                phantom->status = DEAD;
                pacman->points += 200;
            } else {
                // Fantasma mata Pacman
                pacman->life = 0;
            }
        }
    }
}

bool Game::checkLifePacman() {
    return pacman && pacman->life > 0;
}

bool Game::checkScoreWon() {
    return scene && scene->coins <= 0;
}

void Game::destroyScene() {
    if (scene) {
        if (scene->graph) {
            delete[] scene->graph;
        }
        delete scene;
        scene = nullptr;
    }
}

void Game::destroyPacman() {
    if (pacman) {
        delete pacman;
        pacman = nullptr;
    }
}

void Game::destroyPhantom(Phantom* phantom) {
    if (phantom) {
        if (phantom->path) {
            delete[] phantom->path;
        }
        delete phantom;
    }
}
