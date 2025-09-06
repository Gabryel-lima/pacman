#!/usr/bin/env python3
"""
Script para construir executáveis do PacMan para Windows e Linux
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔄 {description}...")
    print(f"Comando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído com sucesso!")
        if result.stdout:
            print("Saída:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}:")
        print(f"Código de saída: {e.returncode}")
        if e.stdout:
            print("Saída:", e.stdout)
        if e.stderr:
            print("Erro:", e.stderr)
        return False

def clean_build_dirs():
    """Limpa diretórios de build anteriores"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Removendo {dir_name}/...")
            shutil.rmtree(dir_name)
    
    # Limpar arquivos .pyc
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def build_linux():
    """Constrói executável para Linux"""
    print("\n🐧 Construindo executável para Linux...")
    
    # Ativar ambiente virtual e construir
    command = "source .venv/bin/activate && pyinstaller pacman.spec --clean"
    return run_command(command, "Build para Linux")

def build_windows():
    """Constrói executável para Windows"""
    print("\n🪟 Construindo executável para Windows...")
    
    # Verificar se Wine está disponível
    wine_available = shutil.which('wine') is not None
    
    if wine_available:
        print("🍷 Wine detectado - construindo para Windows...")
        # Usar Wine para construir para Windows
        command = "source .venv/bin/activate && WINEPREFIX=~/.wine-pyinstaller wine python -m PyInstaller pacman.spec --clean"
        return run_command(command, "Build para Windows via Wine")
    else:
        print("⚠️  Wine não encontrado. Para construir para Windows, você precisa:")
        print("   1. Instalar Wine: sudo apt install wine")
        print("   2. Configurar um prefixo Wine para Python")
        print("   3. Ou usar uma máquina Windows")
        return False

def create_installer_scripts():
    """Cria scripts de instalação simples"""
    
    # Script para Linux
    linux_installer = """#!/bin/bash
# Instalador simples para Linux

echo "🎮 Instalando PacMan..."

# Criar diretório de instalação
INSTALL_DIR="$HOME/.local/share/pacman"
mkdir -p "$INSTALL_DIR"

# Copiar executável
cp dist/PacMan "$INSTALL_DIR/"

# Criar link simbólico
ln -sf "$INSTALL_DIR/PacMan" "$HOME/.local/bin/pacman-game"

echo "✅ PacMan instalado em $INSTALL_DIR"
echo "🚀 Execute com: pacman-game"
"""
    
    with open('install_linux.sh', 'w') as f:
        f.write(linux_installer)
    os.chmod('install_linux.sh', 0o755)
    
    # Script para Windows
    windows_installer = """@echo off
REM Instalador simples para Windows

echo 🎮 Instalando PacMan...

REM Criar diretório de instalação
set INSTALL_DIR=%USERPROFILE%\\AppData\\Local\\PacMan
mkdir "%INSTALL_DIR%" 2>nul

REM Copiar executável
copy "dist\\PacMan.exe" "%INSTALL_DIR%\\"

REM Criar atalho na área de trabalho
echo [InternetShortcut] > "%USERPROFILE%\\Desktop\\PacMan.url"
echo URL=file:///%INSTALL_DIR%/PacMan.exe >> "%USERPROFILE%\\Desktop\\PacMan.url"

echo ✅ PacMan instalado em %INSTALL_DIR%
echo 🚀 Execute clicando no atalho na área de trabalho
pause
"""
    
    with open('install_windows.bat', 'w') as f:
        f.write(windows_installer)

def main():
    """Função principal"""
    print("🎮 Construtor de Executáveis PacMan")
    print("=" * 40)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('main.py'):
        print("❌ Erro: Execute este script no diretório raiz do projeto PacMan")
        sys.exit(1)
    
    # Verificar ambiente virtual
    if not os.path.exists('.venv'):
        print("❌ Erro: Ambiente virtual não encontrado. Execute: python -m venv .venv")
        sys.exit(1)
    
    # Limpar builds anteriores
    clean_build_dirs()
    
    # Menu de opções
    print("\nEscolha uma opção:")
    print("1. Construir apenas para Linux")
    print("2. Construir apenas para Windows")
    print("3. Construir para ambas as plataformas")
    print("4. Apenas criar scripts de instalação")
    
    try:
        choice = input("\nDigite sua escolha (1-4): ").strip()
    except KeyboardInterrupt:
        print("\n\n👋 Operação cancelada pelo usuário")
        sys.exit(0)
    
    success_count = 0
    
    if choice in ['1', '3']:
        if build_linux():
            success_count += 1
    
    if choice in ['2', '3']:
        if build_windows():
            success_count += 1
    
    if choice == '4' or success_count > 0:
        create_installer_scripts()
        print("\n📦 Scripts de instalação criados:")
        print("   - install_linux.sh (para Linux)")
        print("   - install_windows.bat (para Windows)")
    
    # Resumo final
    print("\n" + "=" * 40)
    if success_count > 0:
        print(f"✅ {success_count} executável(is) construído(s) com sucesso!")
        print("\n📁 Arquivos gerados:")
        if os.path.exists('dist'):
            for item in os.listdir('dist'):
                print(f"   - dist/{item}")
    else:
        print("❌ Nenhum executável foi construído")
    
    print("\n🎯 Próximos passos:")
    print("   1. Teste os executáveis na pasta dist/")
    print("   2. Use os scripts de instalação se necessário")
    print("   3. Distribua os arquivos conforme necessário")

if __name__ == "__main__":
    main()
