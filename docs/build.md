# 📦 Guia de Build - Criando Executáveis

Este guia explica como criar executáveis autocontidos do PacMan para Windows e Linux usando PyInstaller.

## 🎯 Visão Geral

Os executáveis criados são **autocontidos**, ou seja, não precisam de Python instalado no sistema de destino. Eles incluem todas as dependências necessárias.

## 📋 Pré-requisitos

### Para Linux:
- Python 3.11+ com ambiente virtual
- PyInstaller instalado
- Pacotes de desenvolvimento do Python:
  ```bash
  sudo apt install python3-dev python3.11-dev
  ```

### Para Windows (usando Wine no Linux):
- Wine instalado e configurado
- Python para Windows instalado no Wine
- PyInstaller instalado no Wine

## 🚀 Métodos de Build

### Método 1: Script Automatizado (Recomendado)

Execute o script principal que oferece um menu interativo:

```bash
python build.py
```

O script oferece as seguintes opções:
1. Construir apenas para Linux
2. Construir apenas para Windows
3. Construir para ambas as plataformas
4. Apenas criar scripts de instalação

### Método 2: Comandos Manuais

#### Para Linux:
```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Construir executável
pyinstaller pacman.spec --clean
```

#### Para Windows (usando Wine):
```bash
# Usar o script específico
./build_windows.sh

# Ou manualmente:
source .venv/bin/activate
WINEPREFIX=~/.wine-pyinstaller wine python -m PyInstaller pacman.spec --clean
```

## 📁 Arquivos Gerados

Após o build bem-sucedido, você encontrará:

- **Linux**: `dist/PacMan` (executável ELF)
- **Windows**: `dist/PacMan.exe` (executável PE)

## 🧪 Testando os Executáveis

### Linux:
```bash
./dist/PacMan
```

### Windows:
```bash
wine dist/PacMan.exe
```

## 📦 Scripts de Instalação

O script `build.py` também cria scripts de instalação:

- `install_linux.sh`: Instala o jogo no Linux
- `install_windows.bat`: Instala o jogo no Windows

## ⚙️ Configuração do Arquivo .spec

O arquivo `pacman.spec` contém as configurações do PyInstaller:

- **Dados incluídos**: Pasta `img/` e `src/`
- **Módulos ocultos**: pygame, módulos do jogo
- **Console**: Desabilitado (jogo gráfico)
- **UPX**: Habilitado para compressão

## 🔧 Solução de Problemas

### Erro: "Python library not found"
```bash
sudo apt install python3-dev python3.11-dev
```

### Erro: "Wine not found"
```bash
sudo apt install wine
winecfg  # Configure na primeira execução
```

### Erro: "Python not found in Wine"
1. Baixe o instalador do Python para Windows
2. Execute: `wine python-installer.exe`
3. Instale PyInstaller: `wine pip install pyinstaller`

### Executável muito grande
- O executável inclui todas as dependências do Python
- Use UPX para compressão adicional
- Considere usar `--onefile` para um único arquivo

## 📊 Tamanhos Típicos

- **Linux**: ~15MB
- **Windows**: ~15MB

## 🎯 Distribuição

Para distribuir o jogo:

1. **Linux**: Copie o arquivo `PacMan` para o sistema de destino
2. **Windows**: Copie o arquivo `PacMan.exe` para o sistema de destino
3. **Dependências**: Os executáveis são autocontidos (não precisam de Python instalado)

## 🔄 Atualizações

Para reconstruir após mudanças no código:

```bash
# Limpar builds anteriores
rm -rf build/ dist/

# Reconstruir
python build.py
```

## 📝 Notas Importantes

- Os executáveis são específicos da arquitetura (x86_64)
- Para outras arquiteturas, construa no sistema de destino
- O jogo requer bibliotecas gráficas (SDL2) no sistema de destino
- Teste sempre os executáveis antes da distribuição

## 🛠️ Arquivos de Build

- `build.py` - Script principal automatizado
- `build_windows.sh` - Script específico para Windows
- `pacman.spec` - Configuração do PyInstaller
- `install_linux.sh` - Script de instalação para Linux
- `install_windows.bat` - Script de instalação para Windows
