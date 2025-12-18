import pygame
import os

# Pega o caminho absoluto da pasta onde este arquivo está (classes)
_diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# Sobe um nível para chegar na raiz (Projeto-IP)
BASE_DIR = os.path.dirname(_diretorio_atual)

# Define as pastas de recursos
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sons")


# FUNÇÕES DE CARREGAMENTO
def carregar_imagem(nome, w=None, h=None):
    caminho = os.path.join(ASSETS_DIR, nome)
    try:
        img = pygame.image.load(caminho).convert_alpha()
        # Cortar transparência para colisão precisa
        bbox = img.get_bounding_rect()
        img = img.subsurface(bbox).copy()
        if w and h:
            img = pygame.transform.scale(img, (w, h))
        return img
    except Exception as e:
        print(f"[AVISO] Não carregou imagem '{nome}': {e}")
        return None

def carregar_som(nome):
    caminho = os.path.join(SOUND_DIR, nome)
    try:
        if os.path.exists(caminho):
            return pygame.mixer.Sound(caminho)
        else:
            print(f"[ERRO] Som não encontrado: {caminho}")
            return None
    except Exception as e:
        print(f"[ERRO] Falha ao carregar som '{nome}': {e}")
        return None

def tocar(som):
    if som:
        som.play()


# FUNÇÕES DE MÚSICA 
def iniciar_musica(nome, volume=0.2):
    caminho = os.path.join(SOUND_DIR, nome)
    try:
        if os.path.exists(caminho):
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1) # -1 toca em loop
        else:
            print(f"[AVISO] Música não encontrada: {caminho}")
    except Exception as e:
        print(f"[ERRO] Falha na música: {e}")

def parar_musica():
    pygame.mixer.music.stop()


# VARIÁVEIS DE SPRITES E SONS
SPRITE_PLATAFORMA = None
SPRITE_JOGADOR_IDLE = None
SPRITE_JOGADOR_WALK = None
SPRITE_JOGADOR_JUMP = None
SPRITE_INIMIGO = None
SPRITE_MOEDA = None
SPRITE_RUM = None
SPRITE_DIAMANTE = None
SPRITE_CHAVE = None
SPRITE_NAVIO = None
SPRITE_COQUEIRO = None
SPRITE_AREIA = None
SPRITE_ESTRELA = None

FONTE = None

SOM_PULO = None
SOM_MOEDA = None
SOM_DIAMANTE = None
SOM_RUM = None
SOM_INIMIGO = None
SOM_VITORIA = None
SOM_GAMEOVER = None
BG_IMAGE = None
NUVENS_IMAGEM = None