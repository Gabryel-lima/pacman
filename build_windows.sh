#!/bin/bash
# Script para construir executável para Windows usando Wine

echo "🪟 Construindo executável para Windows..."

# Verificar se Wine está instalado
if ! command -v wine &> /dev/null; then
    echo "❌ Wine não está instalado!"
    echo "Para instalar Wine:"
    echo "  sudo apt update"
    echo "  sudo apt install wine"
    echo "  winecfg  # Configure Wine na primeira execução"
    exit 1
fi

# Verificar se Python está instalado no Wine
if ! wine python --version &> /dev/null; then
    echo "❌ Python não está instalado no Wine!"
    echo "Para instalar Python no Wine:"
    echo "  1. Baixe o instalador do Python para Windows"
    echo "  2. Execute: wine python-installer.exe"
    echo "  3. Instale o PyInstaller: wine pip install pyinstaller"
    exit 1
fi

# Ativar ambiente virtual e construir
echo "🔨 Construindo executável..."
source .venv/bin/activate

# Usar Wine para executar PyInstaller
WINEPREFIX=~/.wine-pyinstaller wine python -m PyInstaller pacman.spec --clean

if [ $? -eq 0 ]; then
    echo "✅ Executável para Windows criado com sucesso!"
    echo "📁 Arquivo: dist/PacMan.exe"
else
    echo "❌ Erro ao criar executável para Windows"
    exit 1
fi
