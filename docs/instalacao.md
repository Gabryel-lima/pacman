# Guia de Instalação e Configuração

Este guia fornece instruções detalhadas para instalar e configurar o jogo Pac-Man em diferentes sistemas operacionais.

## Pré-requisitos

### Sistema Operacional
- **Windows**: 7, 8, 10, 11 (64-bit recomendado)
- **macOS**: 10.14 (Mojave) ou superior
- **Linux**: Ubuntu 18.04+, Debian 10+, Fedora 30+, Arch Linux

### Software Necessário
- **Python**: 3.7 ou superior
- **pip**: Gerenciador de pacotes Python (incluído com Python 3.4+)
- **Git**: Para clonar o repositório (opcional)

### Hardware Recomendado
- **CPU**: Dual-core 2.0 GHz ou superior
- **RAM**: 4 GB ou mais
- **GPU**: Qualquer GPU com suporte a OpenGL 2.0+
- **Controles**: Xbox, PlayStation, ou controle genérico USB/Bluetooth

## Instalação

### Método 1: Download Direto

1. **Baixe o projeto**
   - Faça download do arquivo ZIP do repositório
   - Extraia para uma pasta de sua escolha

2. **Navegue até a pasta**
   ```bash
   cd pacman
   ```

### Método 2: Git Clone

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd pacman
   ```

### Configuração do Ambiente Python

#### 1. Verificar Python
```bash
python --version
# ou
python3 --version
```

**Saída esperada**: Python 3.7.x ou superior

#### 2. Criar Ambiente Virtual (Recomendado)

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

**Dependências instaladas:**
- `pygame-ce>=2.4.0` - Engine de jogos

## Configuração de Controles

### Controles Xbox

#### Windows
1. **Conecte o controle** via USB ou adaptador wireless
2. **Instale drivers** (geralmente automático)
3. **Teste no Painel de Controle** → Dispositivos e Impressoras

#### macOS
1. **Conecte via USB** ou Bluetooth
2. **Vá em Preferências do Sistema** → Bluetooth
3. **Pareie o controle** se usando Bluetooth

#### Linux
1. **Conecte o controle**
2. **Instale xpadneo** (para controles Xbox One/Series):
   ```bash
   # Ubuntu/Debian
   sudo apt install xpadneo-dkms
   
   # Arch Linux
   yay -S xpadneo-dkms
   ```

### Controles PlayStation

#### Windows
1. **Use DS4Windows** para controles PS4/PS5
2. **Download**: https://ds4-windows.com/
3. **Instale e configure** o controle

#### macOS
1. **Conecte via USB** ou Bluetooth
2. **Funciona nativamente** com macOS

#### Linux
1. **Instale ds4drv**:
   ```bash
   pip install ds4drv
   sudo ds4drv
   ```

### Controles Genéricos

1. **Conecte via USB**
2. **Teste no sistema** antes de executar o jogo
3. **O jogo detectará automaticamente**

## Executando o Jogo

### Primeira Execução

1. **Ative o ambiente virtual** (se usando):
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

2. **Execute o jogo**:
   ```bash
   python main.py
   ```

### Verificações Iniciais

1. **Janela do jogo abre** corretamente
2. **Controles detectados** (se conectados)
3. **Movimento funciona** (teclado ou controle)
4. **Som funciona** (se implementado)

## Configurações Avançadas

### Modificar Configurações do Jogo

Edite `src/constants.py`:

```python
# Configurações de janela
SCALE = 26              # Tamanho dos elementos
FPS = 60                # Frames por segundo

# Configurações de jogo
SPRITE_SPEED = 2        # Velocidade dos sprites
HARMLESS_MODE_DURATION = 16  # Duração do modo inofensivo

# Configurações de controles
DEADZONE = 0.3          # Zona morta dos analógicos
```

### Configurações de Controles

Edite `src/controller.py`:

```python
# Zona morta para analógicos
self.deadzone = 0.3  # 30% - ajuste conforme necessário

# Mapeamento de botões personalizado
button_mappings = {
    # Adicione novos mapeamentos aqui
}
```

## Solução de Problemas

### Problemas Comuns

#### 1. Python não encontrado
**Erro**: `python: command not found`

**Solução**:
- **Windows**: Instale Python do python.org
- **macOS**: Use `python3` em vez de `python`
- **Linux**: `sudo apt install python3 python3-pip`

#### 2. pygame não instala
**Erro**: `pip install pygame-ce` falha

**Solução**:
```bash
# Atualize pip
pip install --upgrade pip

# Instale dependências do sistema (Linux)
sudo apt install python3-dev libsdl2-dev

# Tente novamente
pip install pygame-ce
```

#### 3. Controle não detectado
**Sintomas**: Jogo não reconhece o controle

**Soluções**:
1. **Verifique conexão**: USB/Bluetooth
2. **Teste em outro jogo**: Confirme funcionamento
3. **Reinicie o jogo**: Após conectar controle
4. **Verifique drivers**: Especialmente no Windows

#### 4. Performance baixa
**Sintomas**: Jogo lento ou travando

**Soluções**:
1. **Reduza FPS**: Em `constants.py`
2. **Feche outros programas**: Libere recursos
3. **Verifique GPU**: Drivers atualizados

#### 5. Sprites não carregam
**Sintomas**: Quadrados coloridos em vez de sprites

**Soluções**:
1. **Verifique pasta img/**: Deve existir
2. **Verifique arquivos**: Sprites devem estar presentes
3. **Permissões**: Pasta deve ser legível

### Logs de Debug

Para ativar logs detalhados, adicione temporariamente:

```python
# Em src/controller.py
print(f"Controle detectado: {controller.get_name()}")

# Em src/game.py
print(f"Posição Pac-Man: {self.pac_man_pos}")
```

### Testando Controles

Use este script para testar controles:

```python
import pygame
pygame.init()
pygame.joystick.init()

print(f"Controles detectados: {pygame.joystick.get_count()}")
for i in range(pygame.joystick.get_count()):
    controller = pygame.joystick.Joystick(i)
    controller.init()
    print(f"Controle {i}: {controller.get_name()}")
```

## Atualizações

### Atualizando o Jogo

1. **Backup**: Faça backup de configurações personalizadas
2. **Pull**: `git pull origin main`
3. **Dependências**: `pip install -r requirements.txt --upgrade`
4. **Teste**: Execute o jogo para verificar funcionamento

### Atualizando Dependências

```bash
# Atualizar pygame
pip install --upgrade pygame-ce

# Atualizar todas as dependências
pip install --upgrade -r requirements.txt
```

## Desinstalação

### Remover Completamente

1. **Desative ambiente virtual**:
   ```bash
   deactivate
   ```

2. **Remova a pasta**:
   ```bash
   rm -rf pacman  # Linux/macOS
   rmdir /s pacman  # Windows
   ```

3. **Limpe cache pip** (opcional):
   ```bash
   pip cache purge
   ```

---

**Nota**: Este guia assume conhecimento básico de linha de comando. Para usuários iniciantes, recomenda-se usar uma IDE como PyCharm ou VS Code.
