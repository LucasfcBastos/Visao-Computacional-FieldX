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

# Estrutura do projeto

A estrutura esperada do projeto é:

```text
FieldX/
│
├── main.py
│
├── icon/
│   └── Field_X_AX.png
│
└── README.md
