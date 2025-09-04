# Makefile para Pacman SDL2
# Compilador e flags
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
DEBUG_FLAGS = -std=c++17 -Wall -Wextra -g -DDEBUG

# Diretórios
SRCDIR = src
BUILDDIR = build
IMAGEDIR = images

# Detectar bibliotecas SDL2 usando pkg-config
SDL2_CFLAGS = $(shell pkg-config --cflags sdl2 SDL2_image)
SDL2_LIBS = $(shell pkg-config --libs sdl2 SDL2_image)

# Arquivos fonte
SOURCES = $(wildcard $(SRCDIR)/*.cpp)
OBJECTS = $(SOURCES:$(SRCDIR)/%.cpp=$(BUILDDIR)/%.o)
TARGET = pacman_game

# Regra principal
.PHONY: all clean debug install run help

all: $(TARGET)

# Compilação do executável
$(TARGET): $(OBJECTS) | copy_images
	@echo "Linkando $(TARGET)..."
	$(CXX) $(OBJECTS) -o $@ $(SDL2_LIBS)
	@echo "✓ Build concluído com sucesso!"

# Compilação dos objetos
$(BUILDDIR)/%.o: $(SRCDIR)/%.cpp | $(BUILDDIR)
	@echo "Compilando $<..."
	$(CXX) $(CXXFLAGS) $(SDL2_CFLAGS) -c $< -o $@

# Criar diretório de build
$(BUILDDIR):
	@mkdir -p $(BUILDDIR)

# Verificar se imagens existem (elas já estão no local correto)
copy_images:
	@if [ -d "$(IMAGEDIR)" ]; then \
		echo "✓ Assets encontrados em $(IMAGEDIR)"; \
	else \
		echo "⚠ Aviso: Diretório $(IMAGEDIR) não encontrado"; \
	fi

# Build de debug
debug: CXXFLAGS = $(DEBUG_FLAGS)
debug: $(TARGET)
	@echo "✓ Build de debug concluído!"

# Executar o jogo
run: $(TARGET)
	@echo "Executando $(TARGET)..."
	./$(TARGET)

# Instalar dependências (Ubuntu/Debian)
install-deps:
	@echo "Instalando dependências SDL2..."
	sudo apt update
	sudo apt install -y libsdl2-dev libsdl2-image-dev build-essential

# Instalar dependências (Fedora/CentOS/RHEL)
install-deps-fedora:
	@echo "Instalando dependências SDL2 (Fedora)..."
	sudo dnf install -y SDL2-devel SDL2_image-devel gcc-c++

# Instalar dependências (Arch Linux)
install-deps-arch:
	@echo "Instalando dependências SDL2 (Arch)..."
	sudo pacman -S --needed sdl2 sdl2_image gcc

# Limpeza
clean:
	@echo "Limpando arquivos de build..."
	rm -rf $(BUILDDIR)
	rm -f $(TARGET)
	@echo "✓ Limpeza concluída!"

# Limpeza completa (inclui imagens copiadas)
clean-all: clean
	@echo "Removendo imagens copiadas..."
	rm -rf images
	@echo "✓ Limpeza completa concluída!"

# Verificar dependências
check-deps:
	@echo "Verificando dependências..."
	@pkg-config --exists sdl2 && echo "✓ SDL2 encontrado" || echo "✗ SDL2 não encontrado"
	@pkg-config --exists SDL2_image && echo "✓ SDL2_image encontrado" || echo "✗ SDL2_image não encontrado"
	@which $(CXX) > /dev/null && echo "✓ Compilador $(CXX) encontrado" || echo "✗ Compilador $(CXX) não encontrado"

# Mostrar informações do sistema
info:
	@echo "=== Informações do Build ==="
	@echo "Compilador: $(CXX)"
	@echo "Flags: $(CXXFLAGS)"
	@echo "SDL2 CFLAGS: $(SDL2_CFLAGS)"
	@echo "SDL2 LIBS: $(SDL2_LIBS)"
	@echo "Arquivos fonte: $(SOURCES)"
	@echo "Target: $(TARGET)"

# Ajuda
help:
	@echo "=== Makefile do Pacman SDL2 ==="
	@echo ""
	@echo "Comandos disponíveis:"
	@echo "  make                 - Compila o jogo (release)"
	@echo "  make debug           - Compila o jogo (debug)"
	@echo "  make run             - Compila e executa o jogo"
	@echo "  make clean           - Remove arquivos de build"
	@echo "  make clean-all       - Remove tudo (build + assets)"
	@echo "  make check-deps      - Verifica dependências"
	@echo "  make install-deps    - Instala dependências (Ubuntu/Debian)"
	@echo "  make install-deps-fedora - Instala dependências (Fedora)"
	@echo "  make install-deps-arch   - Instala dependências (Arch)"
	@echo "  make info            - Mostra informações do build"
	@echo "  make help            - Mostra esta ajuda"
	@echo ""
	@echo "Exemplo de uso:"
	@echo "  make clean && make debug && make run"

# Regras que não criam arquivos
.PHONY: copy_images check-deps info help install-deps install-deps-fedora install-deps-arch
