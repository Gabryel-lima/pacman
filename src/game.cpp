#include "pacman.h"
#include <iostream>
#include <cstdlib>
#include <ctime>

// Constantes globais
const Point DIRECTIONS[4] = {
    {1, 0},   // RIGHT
    {0, 1},   // DOWN
    {-1, 0},  // LEFT
    {0, -1}   // UP
};

const int SCENES_POSITION[MAP_SIZE][MAP_SIZE] = {
    {7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8},
    {3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3},
    {3, 1, 7, 4, 8, 1, 7, 4, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 4, 8, 1, 7, 4, 8, 1, 3},
    {3, 2, 3, 0, 3, 1, 3, 0, 0, 0, 3, 1, 3, 3, 1, 3, 0, 0, 0, 3, 1, 3, 0, 3, 2, 3},
    {3, 1, 5, 4, 6, 1, 5, 4, 4, 4, 6, 1, 5, 6, 1, 5, 4, 4, 4, 6, 1, 5, 4, 6, 1, 3},
    {3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3},
    {3, 1, 9, 4, 10, 1, 7, 8, 1, 9, 4, 4, 8, 7, 4, 4, 10, 1, 7, 8, 1, 9, 4, 10, 1, 3},
    {3, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 3},
    {5, 4, 4, 4, 8, 1, 3, 5, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 6, 3, 1, 7, 4, 4, 4, 6},
    {0, 0, 0, 0, 3, 1, 3, 7, 4, 4, 6, 1, 5, 6, 1, 5, 4, 4, 8, 3, 1, 3, 0, 0, 0, 0},
    {7, 4, 4, 4, 6, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 5, 4, 4, 4, 8},
    {3, 1, 1, 1, 1, 1, 5, 6, 1, 7, 4, 4, 4, 4, 4, 4, 8, 1, 5, 6, 1, 1, 1, 1, 1, 3},
    {5, 4, 4, 4, 8, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 1, 7, 4, 4, 4, 6},
    {0, 0, 0, 0, 3, 1, 7, 8, 1, 5, 4, 4, 4, 4, 4, 4, 6, 1, 7, 8, 1, 3, 0, 0, 0, 0},
    {7, 4, 4, 4, 6, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 5, 4, 4, 4, 8},
    {3, 1, 1, 1, 1, 1, 3, 3, 1, 7, 4, 4, 4, 4, 4, 4, 8, 1, 3, 3, 1, 1, 1, 1, 1, 3},
    {3, 1, 7, 4, 10, 1, 5, 6, 1, 5, 4, 4, 8, 7, 4, 4, 6, 1, 5, 6, 1, 9, 4, 8, 1, 3},
    {3, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 3},
    {3, 1, 5, 4, 4, 8, 1, 7, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 8, 1, 7, 4, 4, 6, 1, 3},
    {3, 1, 1, 1, 1, 3, 1, 5, 4, 4, 6, 1, 5, 6, 1, 5, 4, 4, 6, 1, 3, 1, 1, 1, 1, 3},
    {5, 4, 4, 8, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 7, 4, 4, 6},
    {7, 4, 4, 6, 1, 11, 1, 7, 8, 1, 9, 4, 8, 7, 4, 10, 1, 7, 8, 1, 11, 1, 5, 4, 4, 8},
    {3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3},
    {3, 2, 9, 4, 4, 4, 4, 6, 5, 4, 10, 1, 5, 6, 1, 9, 4, 6, 5, 4, 4, 4, 4, 10, 2, 3},
    {3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3},
    {5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 6}
};

Game::Game() : window(nullptr), renderer(nullptr), running(false), gameMode(STARTING),
               scene(nullptr), pacman(nullptr) {
    for (int i = 0; i < 4; i++) {
        phantoms[i] = nullptr;
    }
    srand(time(nullptr));
}

Game::~Game() {
    cleanup();
}

bool Game::init() {
    if (!initSDL()) {
        return false;
    }
    
    if (!loadTextures()) {
        return false;
    }
    
    return true;
}

bool Game::initSDL() {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        std::cerr << "Erro ao inicializar SDL: " << SDL_GetError() << std::endl;
        return false;
    }
    
    window = SDL_CreateWindow("PACMAN - SDL2",
                             SDL_WINDOWPOS_CENTERED,
                             SDL_WINDOWPOS_CENTERED,
                             WINDOW_SIZE, WINDOW_SIZE,
                             SDL_WINDOW_SHOWN);
    
    if (!window) {
        std::cerr << "Erro ao criar janela: " << SDL_GetError() << std::endl;
        return false;
    }
    
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        std::cerr << "Erro ao criar renderer: " << SDL_GetError() << std::endl;
        return false;
    }
    
    if (!(IMG_Init(IMG_INIT_PNG) & IMG_INIT_PNG)) {
        std::cerr << "Erro ao inicializar SDL_image: " << IMG_GetError() << std::endl;
        return false;
    }
    
    return true;
}

bool Game::loadTextures() {
    // Carregar texturas do Pacman
    std::vector<std::string> pacmanPaths = {
        "images/pacman-1.png", "images/pacman-2.png", "images/pacman-3.png",
        "images/pacman-4.png", "images/pacman-5.png", "images/pacman-6.png",
        "images/pacman-7.png", "images/pacman-8.png", "images/pacman-9.png",
        "images/pacman-10.png", "images/pacman-11.png", "images/pacman-12.png"
    };
    
    for (const auto& path : pacmanPaths) {
        SDL_Texture* texture = loadTexture(path);
        if (!texture) {
            std::cerr << "Falha ao carregar textura: " << path << std::endl;
            return false;
        }
        pacmanTextures.push_back(texture);
    }
    
    // Carregar texturas dos fantasmas
    std::vector<std::string> phantomPaths;
    for (int i = 1; i <= 24; i++) {
        phantomPaths.push_back("images/phantom-" + std::to_string(i) + ".png");
    }
    
    for (const auto& path : phantomPaths) {
        SDL_Texture* texture = loadTexture(path);
        if (!texture) {
            std::cerr << "Falha ao carregar textura: " << path << std::endl;
            return false;
        }
        phantomTextures.push_back(texture);
    }
    
    // Carregar texturas do cenário
    std::vector<std::string> scenePaths = {
        "images/empty.png", "images/coin.png", "images/power.png",
        "images/vertical.png", "images/horizontal.png",
        "images/curve-base-left.png", "images/curve-base-right.png",
        "images/curve-top-left.png", "images/curve-top-right.png",
        "images/end-left.png", "images/end-right.png",
        "images/end-base.png", "images/end-top.png"
    };
    
    for (const auto& path : scenePaths) {
        SDL_Texture* texture = loadTexture(path);
        if (!texture) {
            std::cerr << "Falha ao carregar textura: " << path << std::endl;
            return false;
        }
        sceneTextures.push_back(texture);
    }
    
    // Carregar texturas de interface
    gameStartTexture = loadTexture("images/game-start.png");
    gameOverTexture = loadTexture("images/game-over.png");
    gameWonTexture = loadTexture("images/you-won.png");
    
    return true;
}

SDL_Texture* Game::loadTexture(const std::string& path) {
    SDL_Texture* texture = IMG_LoadTexture(renderer, path.c_str());
    if (!texture) {
        std::cerr << "Erro ao carregar textura " << path << ": " << IMG_GetError() << std::endl;
    }
    return texture;
}

void Game::run() {
    running = true;
    
    Uint32 frameStart;
    int frameTime;
    const int FPS = 60;
    const int frameDelay = 1000 / FPS;
    
    while (running) {
        frameStart = SDL_GetTicks();
        
        handleEvents();
        update();
        render();
        
        frameTime = SDL_GetTicks() - frameStart;
        if (frameDelay > frameTime) {
            SDL_Delay(frameDelay - frameTime);
        }
    }
}

void Game::handleEvents() {
    SDL_Event event;
    while (SDL_PollEvent(&event)) {
        switch (event.type) {
            case SDL_QUIT:
                running = false;
                break;
                
            case SDL_KEYDOWN:
                switch (event.key.keysym.sym) {
                    case SDLK_p:
                        if (gameMode == STARTING || gameMode == FAILED || gameMode == WON) {
                            if (gameMode == STARTING) {
                                gameMode = PLAYING;
                                playGame();
                            } else {
                                gameMode = STARTING;
                            }
                        }
                        break;
                        
                    case SDLK_RIGHT:
                        if (pacman && gameMode == PLAYING) {
                            alterDirectionPacman(RIGHT);
                        }
                        break;
                        
                    case SDLK_LEFT:
                        if (pacman && gameMode == PLAYING) {
                            alterDirectionPacman(LEFT);
                        }
                        break;
                        
                    case SDLK_UP:
                        if (pacman && gameMode == PLAYING) {
                            alterDirectionPacman(UP);
                        }
                        break;
                        
                    case SDLK_DOWN:
                        if (pacman && gameMode == PLAYING) {
                            alterDirectionPacman(DOWN);
                        }
                        break;
                        
                    case SDLK_ESCAPE:
                        running = false;
                        break;
                }
                break;
        }
    }
}

void Game::update() {
    static Uint32 lastUpdate = 0;
    Uint32 now = SDL_GetTicks();
    
    if (now - lastUpdate > 200 && gameMode == PLAYING) {  // Atualizar a cada 200ms
        if (pacman && scene) {
            if (checkLifePacman()) {
                if (checkScoreWon()) {
                    gameMode = WON;
                } else {
                    movePacman();
                    for (int i = 0; i < 4; i++) {
                        if (phantoms[i]) {
                            movePhantom(phantoms[i]);
                        }
                    }
                }
            } else {
                gameMode = FAILED;
            }
        }
        lastUpdate = now;
    }
}

void Game::render() {
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderClear(renderer);
    
    if (scene) drawScene();
    if (pacman) drawPacman();
    
    for (int i = 0; i < 4; i++) {
        if (phantoms[i]) {
            drawPhantom(phantoms[i]);
        }
    }
    
    if (gameMode == STARTING) drawGameStart();
    if (gameMode == FAILED) drawGameOver();
    if (gameMode == WON) drawGameWon();
    
    SDL_RenderPresent(renderer);
}

void Game::playGame() {
    // Limpar objetos anteriores
    destroyScene();
    destroyPacman();
    for (int i = 0; i < 4; i++) {
        if (phantoms[i]) {
            destroyPhantom(phantoms[i]);
            phantoms[i] = nullptr;
        }
    }
    
    // Criar novos objetos
    scene = generateScene();
    pacman = createPacman(12, 5);
    phantoms[0] = createPhantom(11, 10, PH_ORANGE, LEFT);
    phantoms[1] = createPhantom(14, 10, PH_PINK, RIGHT);
    phantoms[2] = createPhantom(11, 14, PH_CYAN, LEFT);
    phantoms[3] = createPhantom(14, 14, PH_RED, RIGHT);
}

void Game::cleanup() {
    // Destruir objetos do jogo
    destroyScene();
    destroyPacman();
    for (int i = 0; i < 4; i++) {
        if (phantoms[i]) {
            destroyPhantom(phantoms[i]);
        }
    }
    
    // Destruir texturas
    for (auto texture : pacmanTextures) {
        if (texture) SDL_DestroyTexture(texture);
    }
    for (auto texture : phantomTextures) {
        if (texture) SDL_DestroyTexture(texture);
    }
    for (auto texture : sceneTextures) {
        if (texture) SDL_DestroyTexture(texture);
    }
    
    if (gameStartTexture) SDL_DestroyTexture(gameStartTexture);
    if (gameOverTexture) SDL_DestroyTexture(gameOverTexture);
    if (gameWonTexture) SDL_DestroyTexture(gameWonTexture);
    
    // Limpar SDL
    if (renderer) SDL_DestroyRenderer(renderer);
    if (window) SDL_DestroyWindow(window);
    
    IMG_Quit();
    SDL_Quit();
}
