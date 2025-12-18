import pygame
from .config import *
import classes.assets as assets


# SUPERCLASSE GENÉRICA
class Elemento(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, cor=None, sprite=None):
        super().__init__()

        if sprite is not None:
            self.image = pygame.transform.scale(sprite, (largura, altura))
        else:
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            if cor:
                self.image.fill(cor)

        self.rect = self.image.get_rect(topleft=(x, y))



# TERRENO / CENÁRIO
class Plataforma(Elemento):
    def __init__(self, x, y, largura):
        super().__init__(
            x, y,
            largura, 30,
            COR_PLATAFORMA,
            assets.SPRITE_PLATAFORMA
        )


class AreiaMovedica(Elemento):
    def __init__(self, x, chao_y, largura, profundidade_visual=24, faixa_colisao=10):
        y_draw = chao_y
        super().__init__(x, y_draw, largura, profundidade_visual, cor=(230, 230, 180))

        if assets.SPRITE_AREIA:
            tile_w, tile_h = assets.SPRITE_AREIA.get_size()
            surf = pygame.Surface((largura, tile_h), pygame.SRCALPHA)
            for i in range(0, largura, tile_w):
                surf.blit(assets.SPRITE_AREIA, (i, 0))
            self.image = pygame.transform.scale(surf, (largura, profundidade_visual))
            self.rect = self.image.get_rect(topleft=(x, y_draw))

        self.hitbox = pygame.Rect(
            x,
            chao_y - faixa_colisao,
            largura,
            faixa_colisao
        )


class Navio(Elemento):
    def __init__(self, x, y):
        if assets.SPRITE_NAVIO:
            bw, bh = assets.SPRITE_NAVIO.get_size()
            largura = 180                  
            proporcao = largura / bw
            altura = int(bh * proporcao)

            sprite = pygame.transform.scale(
                assets.SPRITE_NAVIO, (largura, altura)
            )
            super().__init__(x, y, largura, altura, sprite=sprite)
        else:
            super().__init__(x, y, 120, 80, cor=(100, 50, 20))


class Coqueiro(Elemento):
    def __init__(self, x, y):
        if assets.SPRITE_COQUEIRO:
            sprite = pygame.transform.scale(
                assets.SPRITE_COQUEIRO, (90, 150)   
            )
            super().__init__(x, y, 90, 150, sprite=sprite)
        else:
            super().__init__(x, y, 40, 80, cor=(0, 255, 0))



# JOGADOR
class Jogador(Elemento):
    ESCALA = 2   

    def __init__(self, x, y):
        if assets.SPRITE_JOGADOR_IDLE:
            bw, bh = assets.SPRITE_JOGADOR_IDLE.get_size()
            w = bw * self.ESCALA
            h = bh * self.ESCALA

            self.frame_idle = pygame.transform.scale(
                assets.SPRITE_JOGADOR_IDLE, (w, h)
            )
            self.frame_walk = pygame.transform.scale(
                assets.SPRITE_JOGADOR_WALK, (w, h)
            ) if assets.SPRITE_JOGADOR_WALK else self.frame_idle

            self.frame_jump = pygame.transform.scale(
                assets.SPRITE_JOGADOR_JUMP, (w, h)
            ) if assets.SPRITE_JOGADOR_JUMP else self.frame_idle

            sprite_ini = self.frame_idle
        else:
            w, h = 40, 60
            self.frame_idle = None
            self.frame_walk = None
            self.frame_jump = None
            sprite_ini = None

        super().__init__(x, y, w, h, sprite=sprite_ini)

        self.vel_x = 5
        self.vel_y = 0
        self.no_chao = False
        self._movendo_horizontal = 0

        self.moedas = 0
        self.diamantes = 0
        self.rum = 0
        self.pontos = 0
        self.tem_chave = False

        self.super_pulo = False
        self.super_pulo_timer = 0

    def set_image(self, img):
        if img is None:
            return
        midbottom = self.rect.midbottom
        self.image = img
        self.rect = img.get_rect()
        self.rect.midbottom = midbottom

    def mover_horizontal(self, teclas, plataformas):
        dx = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -self.vel_x
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = self.vel_x

        self._movendo_horizontal = dx
        self.rect.x += dx

        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if dx > 0:
                    self.rect.right = p.rect.left
                elif dx < 0:
                    self.rect.left = p.rect.right

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WORLD_WIDTH, self.rect.right)

    def mover_vertical(self, plataformas, chao_y):
        self.vel_y += GRAVIDADE
        self.rect.y += self.vel_y
        self.no_chao = False

        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.no_chao = True
                else:
                    self.rect.top = p.rect.bottom
                self.vel_y = 0

        if self.rect.bottom >= chao_y:
            self.rect.bottom = chao_y
            self.vel_y = 0
            self.no_chao = True

    def pular(self):
        if self.no_chao:
            self.vel_y = FORCA_PULO * (1.6 if self.super_pulo else 1.0)
            assets.tocar(assets.SOM_PULO)

    def atualizar_animacao(self):
        if self.frame_idle is None:
            return

        if not self.no_chao:
            self.set_image(self.frame_jump)
        elif self._movendo_horizontal != 0:
            self.set_image(self.frame_walk)
        else:
            self.set_image(self.frame_idle)



# INIMIGO
class Inimigo(Elemento):
    ESCALA = 1.5   

    def __init__(self, x, y, esq, dir_lim):
        if assets.SPRITE_INIMIGO:
            bw, bh = assets.SPRITE_INIMIGO.get_size()
            w = int(bw * self.ESCALA)
            h = int(bh * self.ESCALA)
            sprite = pygame.transform.scale(
                assets.SPRITE_INIMIGO, (w, h)
            )
        else:
            w, h = 40, 30
            sprite = None

        super().__init__(x, y, w, h, sprite=sprite)

        self.dir = -1
        self.vel = 2
        self.esq = esq
        self.dir_lim = dir_lim

    def update(self, plataformas, chao_y):
        self.rect.x += self.vel * self.dir

        if self.rect.left <= self.esq:
            self.rect.left = self.esq
            self.dir = 1
        elif self.rect.right >= self.dir_lim:
            self.rect.right = self.dir_lim
            self.dir = -1

        self.rect.y += 4
        grounded = False

        for p in plataformas:
            if self.rect.colliderect(p.rect):
                self.rect.bottom = p.rect.top
                grounded = True

        if not grounded and self.rect.bottom >= chao_y:
            self.rect.bottom = chao_y



# COLETÁVEIS 
class Moeda(Elemento):
    def __init__(self, x, y):
        sprite = pygame.transform.scale(
            assets.SPRITE_MOEDA, (24, 24)
        ) if assets.SPRITE_MOEDA else None
        super().__init__(x, y, 24, 24, sprite=sprite)

    def aplicar(self, jogador):
        jogador.moedas += 1
        jogador.pontos += 10
        assets.tocar(assets.SOM_MOEDA)


class Diamante(Elemento):
    def __init__(self, x, y):
        sprite = pygame.transform.scale(
            assets.SPRITE_DIAMANTE, (30, 26)
        ) if assets.SPRITE_DIAMANTE else None
        super().__init__(x, y, 30, 26, sprite=sprite)

    def aplicar(self, jogador):
        jogador.diamantes += 1
        jogador.pontos += 50
        assets.tocar(assets.SOM_DIAMANTE)


class GarrafaRum(Elemento):
    def __init__(self, x, y):
        sprite = pygame.transform.scale(
            assets.SPRITE_RUM, (28, 40)
        ) if assets.SPRITE_RUM else None
        super().__init__(x, y, 28, 40, sprite=sprite)

    def aplicar(self, jogador):
        jogador.rum += 1
        jogador.pontos += 5
        jogador.super_pulo = True
        jogador.super_pulo_timer = pygame.time.get_ticks()
        assets.tocar(assets.SOM_RUM)


class Chave(Elemento):
    def __init__(self, x, y):
        sprite = pygame.transform.scale(
            assets.SPRITE_CHAVE, (24, 24)
        ) if assets.SPRITE_CHAVE else None
        super().__init__(x, y, 24, 24, sprite=sprite)

    def aplicar(self, jogador):
        jogador.tem_chave = True
