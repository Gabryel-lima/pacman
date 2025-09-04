#ifndef PACMAN_H
#define PACMAN_H

#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <vector>
#include <string>

// Constantes do jogo
#define WINDOW_SIZE 600
#define MAP_SIZE 26
#define CELL_SIZE (WINDOW_SIZE / MAP_SIZE)

// Estados do jogo
#define STARTING 0
#define PLAYING 1
#define FAILED 2
#define WON 3

// Direções
#define RIGHT 0
#define DOWN  1
#define LEFT  2
#define UP    3

// Tipos de célula do mapa
#define OBSTACLE (-1)
#define FREE_WAY 0
#define COIN_WAY 1
#define POWER_WAY 2

// Estados do fantasma
#define DEAD (-1)
#define CAPTURE 0
#define ESCAPE 1
#define PAUSE 2

// IDs dos fantasmas
#define PH_ORANGE 0
#define PH_PINK 4
#define PH_CYAN 8
#define PH_RED 12

// Estruturas
struct Point {
    int x, y;
};

struct Vertex {
    int x, y;
    int border[4];
};

struct Scene {
    int map[MAP_SIZE][MAP_SIZE];
    int coins;
    int vertexCount;
    Vertex *graph;
};

struct Pacman {
    int status;
    int xi, yi;  // posições iniciais
    int xl, yl;  // posições anteriores
    int x, y;    // posições dinâmicas
    int direction, step, partial;
    int points;
    int power;
    int life;
    int deadAnimation;
};

struct Phantom {
    int status;
    int xi, yi;  // posições iniciais
    int xl, yl;  // posições anteriores
    int x, y;    // posições dinâmicas
    int direction, step, partial;
    int life;
    int isCrossing;
    int isReturn;
    int *path;
    int indexCurrent;
    int id;
};

// Classe principal do jogo
class Game {
private:
    SDL_Window* window;
    SDL_Renderer* renderer;
    bool running;
    int gameMode;
    
    // Texturas
    std::vector<SDL_Texture*> pacmanTextures;
    std::vector<SDL_Texture*> phantomTextures;
    std::vector<SDL_Texture*> sceneTextures;
    SDL_Texture* gameStartTexture;
    SDL_Texture* gameOverTexture;
    SDL_Texture* gameWonTexture;
    
    // Objetos do jogo
    Scene* scene;
    Pacman* pacman;
    Phantom* phantoms[4];
    
    // Métodos privados
    bool initSDL();
    bool loadTextures();
    void cleanup();
    SDL_Texture* loadTexture(const std::string& path);
    
public:
    Game();
    ~Game();
    
    bool init();
    void run();
    void handleEvents();
    void update();
    void render();
    void playGame();
    
    // Métodos do jogo
    Scene* generateScene();
    Pacman* createPacman(int x, int y);
    Phantom* createPhantom(int x, int y, int id, int direction);
    
    void drawScene();
    void drawPacman();
    void drawPhantom(Phantom* phantom);
    void drawGameStart();
    void drawGameOver();
    void drawGameWon();
    
    void movePacman();
    void movePhantom(Phantom* phantom);
    void alterDirectionPacman(int direction);
    
    bool checkLifePacman();
    bool checkScoreWon();
    
    void destroyScene();
    void destroyPacman();
    void destroyPhantom(Phantom* phantom);
};

// Constantes globais
extern const Point DIRECTIONS[4];
extern const int SCENES_POSITION[MAP_SIZE][MAP_SIZE];

#endif // PACMAN_H
