import pygame
from .config import *
from .entidades import *
from .assets import *

class Fase:
    def __init__(self):
        self.chao_y = 520

        self.todos = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.areia = pygame.sprite.Group()
        self.itens = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.decor = pygame.sprite.Group()

        self.game_over = False
        self.vitoria = False
        self.camera_x = 0
        self.cloud_offset = 0

        self.criar_terreno()
        self.criar_jogador()
        self.criar_inimigos()
        self.criar_itens()
        self.criar_navio()
        self.criar_coqueiros()

    # =====================
    # CRIAÇÃO
    # =====================

    def criar_terreno(self):
        plataformas = [
            (400, 420, 150),
            (700, 360, 120),
            (1100, 450, 200),
            (1500, 420, 200),
        ]
        for x, y, w in plataformas:
            p = Plataforma(x, y, w)
            self.plataformas.add(p)
            self.todos.add(p)

        for x, w in [(900, 200), (2000, 180)]:
            a = AreiaMovedica(x, self.chao_y, w)
            self.areia.add(a)
            self.todos.add(a)

    def criar_jogador(self):
        self.jogador = Jogador(50, 0)
        self.jogador.rect.bottom = self.chao_y
        self.todos.add(self.jogador)

    def criar_inimigos(self):
        dados = [
            (600, 550, 750),
            (1400, 1350, 1600),
            (2500, 2450, 2700),
        ]
        for x, esq, dire in dados:
            i = Inimigo(x, 0, esq, dire)
            i.rect.bottom = self.chao_y
            self.inimigos.add(i)
            self.todos.add(i)

    def criar_itens(self):
        # moedas → 8px acima do chão
        for x in [300, 450, 510, 750, 1150]:
            m = Moeda(x, 0)
            m.rect.bottom = self.chao_y - 8
            self.itens.add(m)
            self.todos.add(m)

        # diamantes → 10px acima do chão
        for x in [950, 2050, 2750]:
            d = Diamante(x, 0)
            d.rect.bottom = self.chao_y - 10
            self.itens.add(d)
            self.todos.add(d)

        # rum → 8px acima do chão
        for x in [1600, 3200]:
            r = GarrafaRum(x, 0)
            r.rect.bottom = self.chao_y - 8
            self.itens.add(r)
            self.todos.add(r)

        # chave → 10px acima do chão
        c = Chave(3400, 0)
        c.rect.bottom = self.chao_y - 10
        self.itens.add(c)
        self.todos.add(c)

    def criar_navio(self):
        self.navio = Navio(WORLD_WIDTH - 300, 0)
        self.navio.rect.bottom = self.chao_y
        self.todos.add(self.navio)

    def criar_coqueiros(self):
        for x in (200, 700, 1300, 1900, 2500, 3100):
            c = Coqueiro(x, 0)
            c.rect.bottom = self.chao_y
            self.decor.add(c)
            self.todos.add(c)

    # =====================
    # ATUALIZAÇÃO
    # =====================

    def atualizar(self):
        if self.game_over or self.vitoria:
            return

        teclas = pygame.key.get_pressed()

        self.jogador.mover_horizontal(teclas, self.plataformas)
        self.jogador.mover_vertical(self.plataformas, self.chao_y)

        if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and self.jogador.no_chao:
            self.jogador.pular()

        self.jogador.atualizar_animacao()

        for i in self.inimigos:
            i.update(self.plataformas, self.chao_y)

        for item in pygame.sprite.spritecollide(self.jogador, self.itens, True):
            item.aplicar(self.jogador)

        if pygame.sprite.spritecollideany(self.jogador, self.inimigos):
            self.game_over = True
            tocar(SOM_INIMIGO)
            tocar(SOM_GAMEOVER)

        if self.jogador.rect.colliderect(self.navio.rect) and self.jogador.tem_chave:
            self.vitoria = True
            tocar(SOM_VITORIA)

        self.camera_x = max(
            0,
            min(self.jogador.rect.centerx - LARGURA_TELA // 2,
                WORLD_WIDTH - LARGURA_TELA)
        )

    # =====================
    # DESENHO
    # =====================

    def desenhar(self, tela):
        if BG_IMAGE:
            tela.blit(BG_IMAGE, (0, 0))
        else:
            tela.fill(COR_CEU)

        pygame.draw.rect(
            tela,
            COR_CHÃO,
            pygame.Rect(-self.camera_x, self.chao_y, WORLD_WIDTH, ALTURA_TELA)
        )

        for s in self.todos:
            tela.blit(s.image, (s.rect.x - self.camera_x, s.rect.y))

        self.desenhar_hud(tela)

        if self.game_over:
            self.mensagem(tela, "GAME OVER – Pressione R")
        elif self.vitoria:
            self.mensagem(tela, "VOCÊ ZARPOU! – Pressione R")

    def desenhar_hud(self, tela):
        texto = (
            f"Moedas: {self.jogador.moedas}   "
            f"Diamantes: {self.jogador.diamantes}   "
            f"Rum: {self.jogador.rum}"
        )
        surf = FONTE.render(texto, True, COR_TEXTO)
        tela.blit(surf, (15, 15))

    def mensagem(self, tela, texto):
        surf = FONTE.render(texto, True, (255, 255, 255))
        rect = surf.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
        tela.blit(surf, rect)
