import tkinter as tk
import cv2
import numpy as np
import time

from PIL import Image, ImageTk, ImageDraw, ImageFont


# ============================================================
# CONFIGURAÇÕES
# ============================================================

CAMINHO_CAMERA = 1
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 30
ESPELHAR_CAMERA = True

TITULO_JANELA = "AX - Field X"
MODO_FULLSCREEN = True
LARGURA_JANELA = 1366
ALTURA_JANELA = 768

LARGURA_PAINEL_DIREITO = 300

COR_FUNDO = "#0B1116"
COR_FUNDO_CAMERA = "#05080A"
COR_PAINEL = "#101820"
COR_BORDA = "#26343D"
COR_TEXTO = "#E8EEF2"
COR_TEXTO_SECUNDARIO = "#9AAAB5"
COR_VERDE = "#63D84F"
COR_VERDE_ESCURA = "#315F2D"
COR_PRETO = "#000000"

CAMINHO_LOGO = "icon/Field_X_AX.png"
LOGO_LARGURA = 110
MARGEM_LOGO_X = 25
MARGEM_LOGO_Y = 20

COR_CANTOS = (99, 216, 79)
ESPESSURA_CANTOS = 2
COMPRIMENTO_CANTO = 25

CAMINHO_FONTE = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
)
CAMINHO_FONTE_NORMAL = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
)


# ============================================================
# FUNÇÕES
# ============================================================

def carregar_fonte(caminho, tamanho):
    try:
        return ImageFont.truetype(caminho, tamanho)
    
    except OSError:
        return ImageFont.load_default()

def carregar_logo(caminho, largura_alvo):
    try:
        logo = Image.open(caminho).convert("RGBA")
        largura_original, altura_original = logo.size
        escala = largura_alvo / largura_original
        altura_alvo = int(altura_original * escala)
        logo = logo.resize( (largura_alvo, altura_alvo), Image.Resampling.LANCZOS)
        return logo

    except Exception as erro:
        print(f"Aviso: não foi possível carregar a logo: {erro}")
        return None

def mesclar_retangulos(retangulos):
    if not retangulos:
        return []

    caixas = [
        [int(x), int(y), int(w), int(h)]
        for (x, y, w, h) in retangulos
    ]

    pontuacoes = [1.0] * len(caixas)
    indices = cv2.dnn.NMSBoxes( caixas, pontuacoes, score_threshold=0.0, nms_threshold=0.3)

    if len(indices) == 0:
        return []

    indices = np.array(indices).flatten()

    return [
        tuple(caixas[i])
        for i in indices
    ]

def detectar_rostos(cinza, classificador_frontal, classificador_perfil):
    parametros = {"scaleFactor": 1.1, "minNeighbors": 5, "minSize": (80, 80)}
    retangulos = []

    encontrados = classificador_frontal.detectMultiScale(cinza, **parametros)
    retangulos.extend(list(encontrados))
    
    encontrados = classificador_perfil.detectMultiScale(cinza, **parametros)
    retangulos.extend(list(encontrados))

    largura = cinza.shape[1]

    cinza_espelhada = cv2.flip(cinza, 1)
    encontrados = classificador_perfil.detectMultiScale(cinza_espelhada, **parametros)

    for (x, y, w, h) in encontrados:
        novo_x = largura - x - w
        retangulos.append((novo_x, y, w, h))

    return mesclar_retangulos(retangulos)
    
def desenhar_cantos(quadro, x, y, w, h):

    pontos = (

        (
            (x, y),
            (x + COMPRIMENTO_CANTO, y),
            (x, y + COMPRIMENTO_CANTO)
        ),

        (
            (x + w, y),
            (x + w - COMPRIMENTO_CANTO, y),
            (x + w, y + COMPRIMENTO_CANTO)
        ),

        (
            (x, y + h),
            (x + COMPRIMENTO_CANTO, y + h),
            (x, y + h - COMPRIMENTO_CANTO)
        ),

        (
            (x + w, y + h),
            (x + w - COMPRIMENTO_CANTO, y + h),
            (x + w, y + h - COMPRIMENTO_CANTO)
        )
    )

    for canto, horizontal, vertical in pontos:

        cv2.line(
            quadro,
            canto,
            horizontal,
            COR_CANTOS,
            ESPESSURA_CANTOS
        )

        cv2.line(
            quadro,
            canto,
            vertical,
            COR_CANTOS,
            ESPESSURA_CANTOS
        )

def desenhar_etiqueta_deteccao(quadro, texto, x, y):

    fonte = carregar_fonte(
        CAMINHO_FONTE,
        18
    )

    imagem_rgba = Image.fromarray(
        cv2.cvtColor(
            quadro,
            cv2.COLOR_BGR2RGB
        )
    ).convert("RGBA")

    sobreposicao = Image.new(
        "RGBA",
        imagem_rgba.size,
        (0, 0, 0, 0)
    )

    desenho = ImageDraw.Draw(
        sobreposicao
    )

    caixa_texto = desenho.textbbox(
        (0, 0),
        texto,
        font=fonte
    )

    largura_texto = (
        caixa_texto[2] -
        caixa_texto[0]
    )

    altura_texto = (
        caixa_texto[3] -
        caixa_texto[1]
    )

    padding_x = 10
    padding_y = 7

    caixa = (
        x,
        y,
        x +
        largura_texto +
        padding_x * 2,
        y +
        altura_texto +
        padding_y * 2
    )

    desenho.rounded_rectangle(
        caixa,
        radius=7,
        fill=(50, 120, 45, 220),
        outline=(99, 216, 79, 255),
        width=1
    )

    desenho.text(
        (
            x + padding_x,
            y + padding_y - caixa_texto[1]
        ),
        texto,
        font=fonte,
        fill=(255, 255, 255, 255)
    )

    resultado = Image.alpha_composite(
        imagem_rgba,
        sobreposicao
    ).convert("RGB")

    quadro[:] = cv2.cvtColor(
        np.array(resultado),
        cv2.COLOR_RGB2BGR
    )

def redimensionar_manter_proporcao(imagem, largura, altura):
    largura_original, altura_original = imagem.size

    escala = min(largura / largura_original, altura / altura_original)
    nova_largura = max(1, int(largura_original * escala))
    nova_altura = max(1, int(altura_original * escala))

    imagem = imagem.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)

    fundo = Image.new("RGB", (largura, altura), COR_PRETO)

    x = (
        largura -
        nova_largura
    ) // 2
    y = (
        altura -
        nova_altura
    ) // 2

    fundo.paste(imagem, (x, y))

    return fundo


# ============================================================
# CLASSE
# ============================================================

class InterfaceAX:

    def __init__(
        self,
        root,
        captura,
        classificador_frontal,
        classificador_perfil
    ):

        self.root = root

        self.captura = captura

        self.classificador_frontal = (
            classificador_frontal
        )

        self.classificador_perfil = (
            classificador_perfil
        )

        self.logo = carregar_logo(
            CAMINHO_LOGO,
            LOGO_LARGURA
        )

        self.fonte_titulo = carregar_fonte(
            CAMINHO_FONTE,
            16
        )

        self.fonte_normal = carregar_fonte(
            CAMINHO_FONTE_NORMAL,
            13
        )

        self.fonte_pequena = carregar_fonte(
            CAMINHO_FONTE_NORMAL,
            11
        )

        self.ultimo_tempo = time.perf_counter()

        self.fps = 0

        self.frame_anterior = None

        self.configurar_janela()

        self.criar_interface()

        self.root.after(
            10,
            self.atualizar_camera
        )

    def configurar_janela(self):

        self.root.title(
            TITULO_JANELA
        )

        self.root.configure(
            bg=COR_FUNDO
        )

        if MODO_FULLSCREEN:

            self.root.attributes(
                "-fullscreen",
                True
            )

        else:

            self.root.geometry(
                f"{LARGURA_JANELA}x{ALTURA_JANELA}"
            )

        self.root.bind(
            "<Escape>",
            self.fechar
        )

        self.root.bind(
            "q",
            self.fechar
        )

    def criar_interface(self):

        self.container = tk.Frame(
            self.root,
            bg=COR_FUNDO
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        self.area_camera = tk.Frame(
            self.container,
            bg=COR_FUNDO_CAMERA
        )

        self.area_camera.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.painel_direito = tk.Frame(
            self.container,
            bg=COR_PAINEL,
            width=LARGURA_PAINEL_DIREITO
        )

        self.painel_direito.pack(
            side="right",
            fill="y"
        )

        self.painel_direito.pack_propagate(
            False
        )

        self.label_camera = tk.Label(
            self.area_camera,
            bg=COR_FUNDO_CAMERA,
            bd=0,
            highlightthickness=0
        )

        self.label_camera.pack(
            fill="both",
            expand=True
        )

        self.criar_painel_direito()

    def criar_painel_direito(self):

        titulo = tk.Label(
            self.painel_direito,
            text="CLASSIFICAÇÃO\n(TEMPO REAL)",
            bg=COR_PAINEL,
            fg=COR_TEXTO,
            font=("DejaVu Sans", 15, "bold"),
            justify="left"
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=(25, 15)
        )

        linha = tk.Frame(
            self.painel_direito,
            bg=COR_BORDA,
            height=1
        )

        linha.pack(
            fill="x",
            padx=20
        )

        self.card_pessoa = self.criar_card(titulo="Pessoa", confianca="0.00", status="Não detectada")
        self.card_daninha = self.criar_card(titulo="Planta daninha", confianca="0.00", status="Não detectada")
        self.card_cultura = self.criar_card(titulo="Cultura (soja/milho)", confianca="0.00", status="Não detectada")

        self.criar_status_sistema()

    def criar_card(
        self,
        titulo,
        confianca,
        status
    ):

        card = tk.Frame(
            self.painel_direito,
            bg="#141E26",
            highlightbackground=COR_BORDA,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=15,
            pady=8
        )


        label_titulo = tk.Label(
            card,
            text=titulo,
            bg="#141E26",
            fg=COR_TEXTO,
            font=("DejaVu Sans", 12, "bold"),
            anchor="w"
        )

        label_titulo.pack(
            fill="x",
            padx=12,
            pady=(12, 2)
        )


        label_confianca = tk.Label(
            card,
            text=confianca,
            bg="#141E26",
            fg="#A6D8E8",
            font=("DejaVu Sans", 22, "bold"),
            anchor="w"
        )

        label_confianca.pack(
            fill="x",
            padx=12
        )


        label_status = tk.Label(
            card,
            text=status,
            bg="#141E26",
            fg=COR_TEXTO_SECUNDARIO,
            font=("DejaVu Sans", 11),
            anchor="w"
        )

        label_status.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )


        return {
            "frame": card,
            "titulo": label_titulo,
            "confianca": label_confianca,
            "status": label_status
        }

    def criar_status_sistema(self):

        separador = tk.Frame(
            self.painel_direito,
            bg=COR_BORDA,
            height=1
        )

        separador.pack(
            fill="x",
            padx=20,
            pady=(15, 15)
        )


        titulo = tk.Label(
            self.painel_direito,
            text="SISTEMA",
            bg=COR_PAINEL,
            fg=COR_TEXTO,
            font=("DejaVu Sans", 12, "bold"),
            anchor="w"
        )

        titulo.pack(
            fill="x",
            padx=20
        )


        self.label_camera_status = tk.Label(
            self.painel_direito,
            text="CÂMERA: IRIUN",
            bg=COR_PAINEL,
            fg=COR_VERDE,
            font=("DejaVu Sans", 10),
            anchor="w"
        )

        self.label_camera_status.pack(
            fill="x",
            padx=20,
            pady=(10, 2)
        )


        self.label_resolution = tk.Label(
            self.painel_direito,
            text="RESOLUÇÃO: --",
            bg=COR_PAINEL,
            fg=COR_TEXTO_SECUNDARIO,
            font=("DejaVu Sans", 10),
            anchor="w"
        )

        self.label_resolution.pack(
            fill="x",
            padx=20,
            pady=2
        )


        self.label_fps = tk.Label(
            self.painel_direito,
            text="FPS: --",
            bg=COR_PAINEL,
            fg=COR_TEXTO_SECUNDARIO,
            font=("DejaVu Sans", 10),
            anchor="w"
        )

        self.label_fps.pack(
            fill="x",
            padx=20,
            pady=2
        )


        self.label_processamento = tk.Label(
            self.painel_direito,
            text="PROCESSAMENTO: LOCAL",
            bg=COR_PAINEL,
            fg=COR_TEXTO_SECUNDARIO,
            font=("DejaVu Sans", 10),
            anchor="w"
        )

        self.label_processamento.pack(
            fill="x",
            padx=20,
            pady=2
        )

    def atualizar_painel(
        self,
        quantidade_rostos
    ):

        if quantidade_rostos > 0:

            confianca = min(
                0.99,
                0.80 +
                quantidade_rostos * 0.03
            )

            self.card_pessoa[
                "confianca"
            ].config(
                text=f"{confianca:.2f}"
            )

            self.card_pessoa[
                "status"
            ].config(
                text=f"{quantidade_rostos} pessoa(s) detectada(s)",
                fg=COR_VERDE
            )

        else:

            self.card_pessoa[
                "confianca"
            ].config(
                text="0.00"
            )

            self.card_pessoa[
                "status"
            ].config(
                text="Não detectada",
                fg=COR_TEXTO_SECUNDARIO
            )

        self.card_daninha[
            "confianca"
        ].config(
            text="0.00"
        )

        self.card_daninha[
            "status"
        ].config(
            text="Não detectada",
            fg=COR_TEXTO_SECUNDARIO
        )

        self.card_cultura[
            "confianca"
        ].config(
            text="0.00"
        )

        self.card_cultura[
            "status"
        ].config(
            text="Não detectada",
            fg=COR_TEXTO_SECUNDARIO
        )

    def desenhar_logo(
        self,
        imagem
    ):

        if self.logo is None:
            return imagem

        imagem = imagem.convert(
            "RGBA"
        )

        imagem.alpha_composite(
            self.logo,
            (
                MARGEM_LOGO_X,
                MARGEM_LOGO_Y
            )
        )

        return imagem

    def desenhar_informacoes_camera(
        self,
        imagem,
        largura,
        altura
    ):

        desenho = ImageDraw.Draw(
            imagem
        )

        fonte = self.fonte_pequena

        texto = (
            f"AX  |  VISÃO COMPUTACIONAL"
            f"  |  PROCESSAMENTO LOCAL"
        )

        caixa = desenho.textbbox(
            (0, 0),
            texto,
            font=fonte
        )

        largura_texto = (
            caixa[2] -
            caixa[0]
        )

        x = (
            largura -
            largura_texto
        ) // 2

        y = altura - 30

        desenho.text(
            (x, y),
            texto,
            font=fonte,
            fill=(220, 230, 235)
        )

    def atualizar_camera(self):

        inicio = time.perf_counter()

        ok, quadro = self.captura.read()

        if not ok:

            self.label_camera_status.config(
                text="CÂMERA: ERRO",
                fg="#FF5555"
            )

            self.root.after(
                100,
                self.atualizar_camera
            )

            return


        self.label_camera_status.config(
            text="CÂMERA: IRIUN",
            fg=COR_VERDE
        )

        if ESPELHAR_CAMERA:

            quadro = cv2.flip(
                quadro,
                1
            )

        altura_frame, largura_frame = (
            quadro.shape[:2]
        )

        self.label_resolution.config(
            text=(
                f"RESOLUÇÃO: "
                f"{largura_frame} × {altura_frame}"
            )
        )

        cinza = cv2.cvtColor(
            quadro,
            cv2.COLOR_BGR2GRAY
        )

        pessoas = detectar_rostos(
            cinza,
            self.classificador_frontal,
            self.classificador_perfil
        )

        for (x, y, w, h) in pessoas:

            desenhar_cantos(
                quadro,
                x,
                y,
                w,
                h
            )

            texto = "Pessoa"

            texto_y = y - 38

            if texto_y < 10:

                texto_y = y + h + 10

            desenhar_etiqueta_deteccao(
                quadro,
                texto,
                x,
                texto_y
            )

        self.atualizar_painel(
            len(pessoas)
        )

        imagem = cv2.cvtColor(
            quadro,
            cv2.COLOR_BGR2RGB
        )

        imagem = Image.fromarray(
            imagem
        )

        largura_area = (
            self.area_camera.winfo_width()
        )

        altura_area = (
            self.area_camera.winfo_height()
        )

        if (
            largura_area <= 1 or
            altura_area <= 1
        ):

            self.root.after(
                10,
                self.atualizar_camera
            )

            return

        imagem = redimensionar_manter_proporcao(
            imagem,
            largura_area,
            altura_area
        )

        imagem = self.desenhar_logo(
            imagem
        )

        self.desenhar_informacoes_camera(
            imagem,
            largura_area,
            altura_area
        )

        imagem_tk = ImageTk.PhotoImage(
            imagem
        )

        self.label_camera.configure(
            image=imagem_tk
        )

        self.label_camera.image = imagem_tk

        fim = time.perf_counter()

        tempo_frame = (
            fim -
            self.ultimo_tempo
        )

        self.ultimo_tempo = fim

        if tempo_frame > 0:

            fps_atual = (
                1 /
                tempo_frame
            )

            self.fps = (
                self.fps * 0.9 +
                fps_atual * 0.1
            )

        self.label_fps.config(
            text=f"FPS: {self.fps:.1f}"
        )

        latencia = (
            (fim - inicio) *
            1000
        )

        self.root.after(
            1,
            self.atualizar_camera
        )

    def fechar(self, evento=None):

        try:
            self.captura.release()
        except Exception:
            pass

        self.root.destroy()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 50)
    print("AX - FIELD X")
    print("Sistema de visão computacional")
    print("=" * 50)

    caminho_frontal = (
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    caminho_perfil = (
        cv2.data.haarcascades +
        "haarcascade_profileface.xml"
    )


    classificador_frontal = (
        cv2.CascadeClassifier(
            caminho_frontal
        )
    )

    classificador_perfil = (
        cv2.CascadeClassifier(
            caminho_perfil
        )
    )


    if classificador_frontal.empty():

        print(
            "ERRO: não foi possível carregar "
            "o detector frontal."
        )

        return


    if classificador_perfil.empty():

        print(
            "ERRO: não foi possível carregar "
            "o detector de perfil."
        )

        return

    print(
        f"Abrindo câmera: "
        f"{CAMINHO_CAMERA}"
    )


    captura = cv2.VideoCapture(CAMINHO_CAMERA)


    if not captura.isOpened():

        print()
        print(
            "ERRO: não foi possível abrir "
            "a câmera."
        )

        print(
            f"Verifique se {CAMINHO_CAMERA} "
            "está disponível."
        )

        return

    captura.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    captura.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    captura.set(cv2.CAP_PROP_FPS, CAMERA_FPS)

    largura_real = int( captura.get( cv2.CAP_PROP_FRAME_WIDTH ) )
    altura_real = int( captura.get( cv2.CAP_PROP_FRAME_HEIGHT ) )

    fps_real = captura.get( cv2.CAP_PROP_FPS )

    print("Câmera aberta.")
    print(f"Resolução: {largura_real}x{altura_real}")
    print(f"FPS: {fps_real}")
    print()

    root = tk.Tk()

    interface = InterfaceAX(root, captura, classificador_frontal, classificador_perfil)

    try:

        root.mainloop()

    except KeyboardInterrupt:

        print(
            "Programa interrompido."
        )

    finally:

        captura.release()

        cv2.destroyAllWindows()

        print(
            "Câmera liberada."
        )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()