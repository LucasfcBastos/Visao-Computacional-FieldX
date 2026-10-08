# Field X AX — Sistema de Detecção

Sistema de demonstração desenvolvido para representar, em bancada, o funcionamento do sistema de visão computacional da **Field X**.

O projeto utiliza uma câmera para capturar imagens em tempo real e realizar uma demonstração de detecção através de visão computacional, apresentando as informações diretamente sobre o vídeo.

> **Observação:** este projeto é um protótipo de demonstração para apresentações em bancada e eventos como o **Bistro**. Ele representa visualmente o conceito do sistema de detecção da Field X e não corresponde à versão final do sistema embarcado do AX.

---

# Objetivo

O objetivo deste projeto é servir como uma **representação visual do sistema de detecção da Field X** durante apresentações do projeto.

Durante uma demonstração, o sistema:

- Captura imagens através de uma câmera;
- Processa os frames em tempo real;
- Realiza a detecção através de visão computacional;
- Exibe as detecções sobre a imagem;
- Apresenta informações da detecção em uma interface;
- Representa a futura integração entre visão computacional e o sistema de pulverização seletiva do AX.

A aplicação foi desenvolvida principalmente para utilização em:

- Apresentações em bancada;
- Demonstrações do projeto;
- Eventos;
- Protótipos;
- Validação visual da interface;
- Apresentações do conceito do Field X AX.

---

# Tecnologias utilizadas

O projeto utiliza:

- **Python 3**
- **OpenCV**
- **NumPy**
- **Pillow**
- **Tkinter**

### OpenCV

Responsável pela captura e processamento das imagens da câmera e pelos recursos de visão computacional.

### NumPy

Utilizado no processamento das imagens e manipulação dos dados dos frames.

### Pillow

Utilizado para manipulação das imagens, textos, etiquetas e elementos gráficos.

### Tkinter

Utilizado para construção da interface gráfica da aplicação.

---

## Instalação

O sistema utiliza Python e algumas bibliotecas para captura e processamento de imagens.

### Requisitos

- Python 3.10 ou superior
- Webcam ou câmera conectada ao computador
- Git (opcional)

As bibliotecas utilizadas são:

- OpenCV
- NumPy
- Pillow
- Tkinter

---

### Linux

#### 1. Verifique o Python

```bash
python3 --version
```

Caso o Python não esteja instalado:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

#### 2. Instale as bibliotecas

```bash
pip3 install opencv-python numpy pillow
```

#### 3. Execute o sistema

Entre na pasta do projeto:

```bash
cd caminho/para/o/projeto
```

Depois execute:

```bash
python3 main.py
```

#### 4. Configuração da câmera

No Linux, as câmeras normalmente aparecem como dispositivos `/dev/videoX`.

Exemplo:

```text
/dev/video0
/dev/video1
/dev/video2
```

Para verificar as câmeras disponíveis:

```bash
v4l2-ctl --list-devices
```

Caso o comando não esteja disponível:

```bash
sudo apt install v4l-utils
```

---

### macOS

#### 1. Verifique o Python

```bash
python3 --version
```

Caso não tenha Python instalado, ele pode ser instalado pelo Homebrew:

```bash
brew install python
```

#### 2. Instale as bibliotecas

```bash
python3 -m pip install opencv-python numpy pillow
```

#### 3. Execute o sistema

Entre na pasta do projeto:

```bash
cd caminho/para/o/projeto
```

Execute:

```bash
python3 main.py
```

> **Observação:** o código atual utiliza um caminho de câmera específico do Linux (`/dev/video0`). Para utilizar o sistema no macOS, será necessário adaptar a configuração da câmera no código.

---

### Windows

#### 1. Instale o Python

Baixe e instale o Python pelo site oficial:

https://www.python.org/

Durante a instalação, marque a opção:

```text
Add Python to PATH
```

#### 2. Verifique a instalação

Abra o PowerShell ou CMD:

```powershell
python --version
```

#### 3. Instale as bibliotecas

```powershell
python -m pip install opencv-python numpy pillow
```

#### 4. Execute o sistema

Entre na pasta do projeto:

```powershell
cd caminho\para\o\projeto
```

Execute:

```powershell
python main.py
```

> **Observação:** o código atual utiliza um caminho de câmera específico do Linux (`/dev/video0`). Para utilizar o sistema no Windows, será necessário adaptar a configuração da câmera no código.

---

## Execução rápida

Depois de instalar as dependências, basta executar:

### Linux

```bash
python3 main.py
```

### macOS

```bash
python3 main.py
```

### Windows

```powershell
python main.py
```

---

## Solução de problemas

### A câmera não aparece

Verifique se a câmera está conectada e reconhecida pelo sistema.

No Linux:

```bash
v4l2-ctl --list-devices
```

Também verifique se o caminho configurado no código corresponde à câmera desejada.

### Erro ao instalar bibliotecas

Tente atualizar o `pip`:

```bash
python3 -m pip install --upgrade pip
```

Depois instale novamente:

```bash
python3 -m pip install opencv-python numpy pillow
```

No Windows:

```powershell
python -m pip install --upgrade pip
python -m pip install opencv-python numpy pillow
```

### Tkinter não encontrado no Linux

Instale o pacote:

```bash
sudo apt install python3-tk
```

Depois execute novamente:

```bash
python3 main.py
```