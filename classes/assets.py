# classes/assets.py
import pygame
import os
from .config import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")
SOUND_DIR = os.path.join(BASE_DIR, "sons")

# =========================
# FUNÇÕES
# =========================

def carregar_imagem(nome, w=None, h=None):
    caminho = os.path.join(ASSETS_DIR, nome)
    try:
        img = pygame.image.load(caminho).convert_alpha()
        if w and h:
            img = pygame.transform.scale(img, (w, h))
        return img
    except Exception as e:
        print(f"[AVISO] Não consegui carregar '{caminho}': {e}")
        return None


def carregar_som(nome):
    caminho = os.path.join(SOUND_DIR, nome)
    try:
        return pygame.mixer.Sound(caminho)
    except Exception as e:
        print(f"[AVISO] Não consegui carregar som '{caminho}': {e}")
        return None


def tocar(som):
    if som:
        som.play()

# =========================
# SPRITES (CARREGADOS NO MAIN)
# =========================

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

BG_IMAGE = None
NUVENS_IMAGEM = None

FONTE = None

SOM_PULO = None
SOM_MOEDA = None
SOM_DIAMANTE = None
SOM_RUM = None
SOM_INIMIGO = None
SOM_VITORIA = None
SOM_GAMEOVER = None
