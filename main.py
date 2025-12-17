import pygame
import sys
import os

# CONFIGURAÇÕES GERAIS


LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60
WORLD_WIDTH = 4000

# Cores (HUD / fallback)
COR_CEU = (135, 206, 235)
COR_CHÃO = (150, 105, 60)
COR_PLATAFORMA = (160, 82, 45)
COR_TEXTO = (255, 255, 255)

GRAVIDADE = 0.6
FORCA_PULO = -12

pygame.init()

#  som — reduz delay
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
except Exception as e:
    print("[AVISO] Mixer de áudio não iniciou:", e)

pygame.display.set_caption("Zarpar!")
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
RELOGIO = pygame.time.Clock()
FONTE = pygame.font.SysFont("arial", 18, bold=True)

# CAMINHOS / CARREGAMENTO


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR,"assets", "images")
SOUND_DIR = os.path.join(BASE_DIR, "sons")


def carregar_imagem(nome_arquivo, largura=None, altura=None):
    """Carrega uma imagem da pasta de assets, opcionalmente redimensionando."""
    caminho = os.path.join(ASSETS_DIR, nome_arquivo)
    try:
        img = pygame.image.load(caminho).convert_alpha()
    except Exception as e:
        print(f"[AVISO] Não consegui carregar '{caminho}': {e}")
        return None

    if largura is not None and altura is not None:
        img = pygame.transform.scale(img, (largura, altura))
    return img


def cortar_transparencia(imagem):
    """Remove bordas 100% transparentes de um sprite."""
    if imagem is None:
        return None
    bbox = imagem.get_bounding_rect()
    return imagem.subsurface(bbox).copy()


def carregar_som(nome):
    """Carrega um efeito sonoro (Sound)."""
    caminho = os.path.join(SOUND_DIR, nome)
    try:
        return pygame.mixer.Sound(caminho)
    except Exception as e:
        print(f"[AVISO] Não consegui carregar som '{caminho}': {e}")
        return None


def tocar(som):
    """Toca um som com segurança (se existir e mixer estiver ok)."""
    if som is not None:
        try:
            som.play()
        except Exception:
            pass


def iniciar_musica():
    """Inicia música de fundo em loop (se existir)."""
    caminho = os.path.join(SOUND_DIR, "musica_fundo.ogg")
    try:
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"[AVISO] Não consegui iniciar música '{caminho}': {e}")


def parar_musica():
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass


# SONS


SOM_PULO = carregar_som("pulo.wav")
SOM_MOEDA = carregar_som("moeda.ogg")
SOM_DIAMANTE = carregar_som("diamante.wav")
SOM_RUM = carregar_som("rum.wav")
SOM_INIMIGO = carregar_som("inimigo.wav")
SOM_VITORIA = carregar_som("vitoria.wav")
SOM_GAMEOVER = carregar_som("gameover.wav")

# Volumes (
for s, vol in [
    (SOM_PULO, 0.6),
    (SOM_MOEDA, 0.65),
    (SOM_DIAMANTE, 0.7),
    (SOM_RUM, 0.6),
    (SOM_INIMIGO, 0.7),
    (SOM_VITORIA, 0.8),
    (SOM_GAMEOVER, 0.8),
]:
    if s:
        try:
            s.set_volume(vol)
        except Exception:
            pass

# inicia música ao abrir o jogo
iniciar_musica()

# IMAGENS


BG_IMAGE = carregar_imagem("background.png", LARGURA_TELA, ALTURA_TELA)
NUVENS_IMAGEM = cortar_transparencia(carregar_imagem("nuvens.png"))
if NUVENS_IMAGEM:
    try:
        NUVENS_IMAGEM = pygame.transform.scale(NUVENS_IMAGEM, (250, 150))
    except Exception:
        pass

SPRITE_PLATAFORMA = cortar_transparencia(carregar_imagem("obstaculo.png"))

SPRITE_JOGADOR_IDLE = cortar_transparencia(carregar_imagem("pirata.png"))
SPRITE_JOGADOR_WALK = cortar_transparencia(carregar_imagem("pirata_andando.png"))
SPRITE_JOGADOR_JUMP = cortar_transparencia(carregar_imagem("pirata_pulando.png"))

if SPRITE_JOGADOR_IDLE:
    try:
        SPRITE_JOGADOR_IDLE = pygame.transform.scale(SPRITE_JOGADOR_IDLE, (25, 35))
    except Exception:
        pass
if SPRITE_JOGADOR_WALK:
    try:
        SPRITE_JOGADOR_WALK = pygame.transform.scale(SPRITE_JOGADOR_WALK, (25, 35))
    except Exception:
        pass
if SPRITE_JOGADOR_JUMP:
    try:
        SPRITE_JOGADOR_JUMP = pygame.transform.scale(SPRITE_JOGADOR_JUMP, (25, 35))
    except Exception:
        pass

SPRITE_INIMIGO = cortar_transparencia(carregar_imagem("carangueijo.png"))
if SPRITE_INIMIGO:
    try:
        SPRITE_INIMIGO = pygame.transform.scale(SPRITE_INIMIGO, (50, 35))
    except Exception:
        pass

SPRITE_MOEDA_BASE = cortar_transparencia(carregar_imagem("moeda.png"))
SPRITE_MOEDA = pygame.transform.scale(SPRITE_MOEDA_BASE, (24, 24)) if SPRITE_MOEDA_BASE else None

SPRITE_RUM_BASE = cortar_transparencia(carregar_imagem("rum.png"))
SPRITE_RUM = pygame.transform.scale(SPRITE_RUM_BASE, (28, 40)) if SPRITE_RUM_BASE else None

SPRITE_DIAMANTE_BASE = cortar_transparencia(carregar_imagem("diamante.png"))
SPRITE_DIAMANTE = pygame.transform.scale(SPRITE_DIAMANTE_BASE, (30, 26)) if SPRITE_DIAMANTE_BASE else None

SPRITE_CHAVE_BASE = cortar_transparencia(carregar_imagem("chave.png"))
SPRITE_CHAVE = pygame.transform.scale(SPRITE_CHAVE_BASE, (24, 24)) if SPRITE_CHAVE_BASE else None

SPRITE_NAVIO_BASE = cortar_transparencia(carregar_imagem("navio.png"))
if SPRITE_NAVIO_BASE is not None:
    nv_w, nv_h = SPRITE_NAVIO_BASE.get_size()
    NAVIO_LARGURA = 180
    proporcao_navio = NAVIO_LARGURA / nv_w
    NAVIO_ALTURA = int(nv_h * proporcao_navio)
    SPRITE_NAVIO = pygame.transform.scale(SPRITE_NAVIO_BASE, (NAVIO_LARGURA, NAVIO_ALTURA))
else:
    SPRITE_NAVIO = None

SPRITE_COQUEIRO_BASE = carregar_imagem("coqueiro.png")
if SPRITE_COQUEIRO_BASE is not None:
    SPRITE_COQUEIRO_BASE = cortar_transparencia(SPRITE_COQUEIRO_BASE)
    SPRITE_COQUEIRO = pygame.transform.scale(SPRITE_COQUEIRO_BASE, (90, 150))
else:
    SPRITE_COQUEIRO = None

SPRITE_AREIA_BASE = cortar_transparencia(carregar_imagem("areia.png"))
SPRITE_AREIA = SPRITE_AREIA_BASE if SPRITE_AREIA_BASE else None

SPRITE_ESTRELA_BASE = cortar_transparencia(carregar_imagem("estrela.png"))
SPRITE_ESTRELA = pygame.transform.scale(SPRITE_ESTRELA_BASE, (27, 27)) if SPRITE_ESTRELA_BASE else None



# SUPERCLASSE GENÉRICA


class Elemento(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, cor=None, sprite=None):
        super().__init__()
        if sprite is not None:
            try:
                img_w, img_h = sprite.get_size()
                if img_w == largura and img_h == altura:
                    self.image = sprite.copy()
                else:
                    self.image = pygame.transform.scale(sprite, (largura, altura))
            except Exception:
                self.image = pygame.transform.scale(sprite, (largura, altura))
        else:
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            if cor is not None:
                self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(x, y))


# PLATAFORMAS, AREIA, NAVIO, COQUEIRO


class Plataforma(Elemento):
    def __init__(self, x, y, largura):
        super().__init__(x, y, largura, 30, cor=COR_PLATAFORMA, sprite=SPRITE_PLATAFORMA)


class AreiaMovedica(Elemento):
    """
    Desenha a areia "dentro do piso" (começa em chao_y),
    mas a colisão/efeito usa uma hitbox fininha acima do chão.
    """
    def __init__(self, x, chao_y, largura, profundidade_visual=24, faixa_colisao=10):
        y_draw = chao_y  # começa no topo do chão, para parecer "dentro"
        super().__init__(x, y_draw, largura, profundidade_visual, cor=(230, 230, 180), sprite=None)

        if SPRITE_AREIA is not None:
            tile_w, tile_h = SPRITE_AREIA.get_size()
            surf = pygame.Surface((largura, tile_h), pygame.SRCALPHA)
            for i in range(0, largura, tile_w):
                surf.blit(SPRITE_AREIA, (i, 0))
            self.image = pygame.transform.scale(surf, (largura, profundidade_visual))
            self.rect = self.image.get_rect(topleft=(x, y_draw))

        self.hitbox = pygame.Rect(x, chao_y - faixa_colisao, largura, faixa_colisao)


class Navio(Elemento):
    def __init__(self, x, y):
        if SPRITE_NAVIO is not None:
            w, h = SPRITE_NAVIO.get_size()
            super().__init__(x, y, w, h, sprite=SPRITE_NAVIO)
        else:
            super().__init__(x, y, 120, 80, cor=(100, 50, 20))


class Coqueiro(Elemento):
    def __init__(self, x, y):
        if SPRITE_COQUEIRO is not None:
            w, h = SPRITE_COQUEIRO.get_size()
            super().__init__(x, y, w, h, sprite=SPRITE_COQUEIRO)
        else:
            super().__init__(x, y, 40, 80, cor=(0, 255, 0))


# PERSONAGENS


class Jogador(Elemento):
    ESCALA = 2

    def __init__(self, x, y):
        if SPRITE_JOGADOR_IDLE:
            base_w, base_h = SPRITE_JOGADOR_IDLE.get_size()
            w = base_w * self.ESCALA
            h = base_h * self.ESCALA

            self.frame_idle = pygame.transform.scale(SPRITE_JOGADOR_IDLE, (w, h))
            self.frame_walk = pygame.transform.scale(SPRITE_JOGADOR_WALK, (w, h)) if SPRITE_JOGADOR_WALK else self.frame_idle
            self.frame_jump = pygame.transform.scale(SPRITE_JOGADOR_JUMP, (w, h)) if SPRITE_JOGADOR_JUMP else self.frame_idle

            sprite_ini = self.frame_idle
        else:
            sprite_ini = None
            w, h = 40, 60
            self.frame_idle = None
            self.frame_walk = None
            self.frame_jump = None

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
            tocar(SOM_PULO)

    def atualizar_animacao(self):
        if self.frame_idle is None:
            return
        if not self.no_chao:
            self.set_image(self.frame_jump)
        else:
            if self._movendo_horizontal != 0:
                self.set_image(self.frame_walk)
            else:
                self.set_image(self.frame_idle)


class Inimigo(Elemento):
    ESCALA = 1.5

    def __init__(self, x, y, esq, dir_lim):
        if SPRITE_INIMIGO:
            bw, bh = SPRITE_INIMIGO.get_size()
            w = int(bw * self.ESCALA)
            h = int(bh * self.ESCALA)
            sprite = pygame.transform.scale(SPRITE_INIMIGO, (w, h))
        else:
            sprite = None
            w, h = 40, 30

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


class Coletavel(Elemento):
    def aplicar(self, jogador):
        pass


class Moeda(Coletavel):
    def __init__(self, x, y):
        sprite = SPRITE_MOEDA
        w, h = sprite.get_size() if sprite else (20, 20)
        super().__init__(x, y, w, h, sprite=sprite)

    def aplicar(self, jogador):
        jogador.moedas += 1
        jogador.pontos += 10
        tocar(SOM_MOEDA)


class Diamante(Coletavel):
    def __init__(self, x, y):
        sprite = SPRITE_DIAMANTE
        w, h = sprite.get_size() if sprite else (20, 20)
        super().__init__(x, y, w, h, sprite=sprite)

    def aplicar(self, jogador):
        jogador.diamantes += 1
        jogador.pontos += 50
        tocar(SOM_DIAMANTE)


class GarrafaRum(Coletavel):
    def __init__(self, x, y):
        sprite = SPRITE_RUM
        w, h = sprite.get_size() if sprite else (16, 28)
        super().__init__(x, y, w, h, sprite=sprite)

    def aplicar(self, jogador):
        jogador.rum += 1
        jogador.pontos += 5
        jogador.super_pulo = True
        jogador.super_pulo_timer = pygame.time.get_ticks()
        tocar(SOM_RUM)


class Chave(Coletavel):
    def __init__(self, x, y):
        if SPRITE_CHAVE is not None:
            w, h = SPRITE_CHAVE.get_size()
            sprite = SPRITE_CHAVE
        else:
            w, h = 18, 18
            sprite = None
        super().__init__(x, y, w, h, sprite=sprite)

    def aplicar(self, jogador):
        jogador.tem_chave = True
       



# FASE


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

        self.em_areia_anterior = False
        self.cloud_offset = 0

        self.total_moedas = 0
        self.total_diamantes = 0
        self.estrelas = 0

        self._som_fim_tocado = False

        self.criar_terreno()
        self.criar_jogador()
        self.criar_inimigos()
        self.criar_itens()
        self.criar_navio()
        self.criar_coqueiros()

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

        areias = [
            (900, 200),
            (2000, 180),
        ]
        for x, w in areias:
            a = AreiaMovedica(x, self.chao_y, w, profundidade_visual=24, faixa_colisao=10)
            self.areia.add(a)
            self.todos.add(a)

    def criar_jogador(self):
        self.jogador = Jogador(50, 460)
        self.todos.add(self.jogador)

    def criar_inimigos(self):
        dados = [
            (600, 490, 550, 750),
            (1400, 490, 1350, 1600),
            (2500, 490, 2450, 2700),
        ]
        for x, y, esq, dire in dados:
            inimigo = Inimigo(x, y, esq, dire)
            self.inimigos.add(inimigo)
            self.todos.add(inimigo)

    def criar_itens(self):
        moedas = [
            (300, 480), (450, 380), (510, 380),
            (750, 330), (1150, 420)
        ]
        diamantes = [(950, 460), (2050, 460), (2750, 310)]
        rum = [(1600, 460), (3200, 460)]

        for x, y in moedas:
            m = Moeda(x, y)
            self.itens.add(m)
            self.todos.add(m)
            self.total_moedas += 1

        for x, y in diamantes:
            d = Diamante(x, y)
            self.itens.add(d)
            self.todos.add(d)
            self.total_diamantes += 1

        for x, y in rum:
            r = GarrafaRum(x, y)
            self.itens.add(r)
            self.todos.add(r)

        chave = Chave(3400, 440)
        self.itens.add(chave)
        self.todos.add(chave)

    def criar_navio(self):
        navio = Navio(WORLD_WIDTH - 300, 100)
        navio.rect.bottom = self.chao_y
        self.navio = navio
        self.todos.add(navio)

    def criar_coqueiros(self):
        if SPRITE_COQUEIRO:
            for x in (200, 700, 1300, 1900, 2500, 3100):
                c = Coqueiro(x, 0)
                c.rect.bottom = self.chao_y
                self.decor.add(c)
                self.todos.add(c)

    def atualizar(self):
        if self.game_over or self.vitoria:
            return

        #  super pulo dura 6s 
        if self.jogador.super_pulo:
            if pygame.time.get_ticks() - self.jogador.super_pulo_timer >= 6000:
                self.jogador.super_pulo = False

        teclas = pygame.key.get_pressed()

        # areia 
        em_areia = any(self.jogador.rect.colliderect(a.hitbox) for a in self.areia)
        self.em_areia_anterior = em_areia

        self.jogador.vel_x = 3 if em_areia else 5

        self.jogador.mover_horizontal(teclas, self.plataformas)
        self.jogador.mover_vertical(self.plataformas, self.chao_y)

        if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and self.jogador.no_chao:
            self.jogador.pular()

        self.jogador.atualizar_animacao()

        for inimigo in self.inimigos:
            inimigo.update(self.plataformas, self.chao_y)

        coletados = pygame.sprite.spritecollide(self.jogador, self.itens, dokill=True)
        for item in coletados:
            item.aplicar(self.jogador)

        # vitória
        if self.jogador.rect.colliderect(self.navio.rect) and self.jogador.tem_chave:
            self.vitoria = True
            self.estrelas = self.calcular_estrelas()
            parar_musica()
            tocar(SOM_VITORIA)

        # derrota por inimigo
        if pygame.sprite.spritecollideany(self.jogador, self.inimigos):
            self.game_over = True
            parar_musica()
            tocar(SOM_INIMIGO)
            tocar(SOM_GAMEOVER)

        # queda
        if self.jogador.rect.top > ALTURA_TELA + 200:
            self.game_over = True
            parar_musica()
            tocar(SOM_GAMEOVER)

        # câmera
        self.camera_x = max(
            0,
            min(self.jogador.rect.centerx - LARGURA_TELA // 2, WORLD_WIDTH - LARGURA_TELA)
        )

        if NUVENS_IMAGEM:
            self.cloud_offset += 0.3

    def desenhar_fundo(self, tela):
        if BG_IMAGE:
            tela.blit(BG_IMAGE, (0, 0))
        else:
            tela.fill(COR_CEU)

        if NUVENS_IMAGEM:
            larg = NUVENS_IMAGEM.get_width()
            x_base = -self.cloud_offset % larg
            for i in range(3):
                tela.blit(NUVENS_IMAGEM, (x_base + i * larg, 20))

    def desenhar(self, tela):
        self.desenhar_fundo(tela)

        # chão
        pygame.draw.rect(
            tela,
            COR_CHÃO,
            pygame.Rect(-self.camera_x, self.chao_y, WORLD_WIDTH, ALTURA_TELA)
        )

        # sprites
        for s in self.todos:
            tela.blit(s.image, (s.rect.x - self.camera_x, s.rect.y))

        self.desenhar_hud(tela)

        if self.game_over:
            self.mensagem(tela, "GAME OVER – Pressione R")
        elif self.vitoria:
            self.mensagem(tela, "VOCÊ ZARPOU! – Pressione R")

        if self.jogador.super_pulo:
            texto = FONTE.render("SUPER PULO ATIVO!", True, (0, 0, 139))
            rect = texto.get_rect(center=(LARGURA_TELA // 2, 170))
            tela.blit(texto, rect)

    def desenhar_hud(self, tela):
        j = self.jogador

        caixa_larg = 350
        caixa_alt = 95
        caixa_x = 10
        caixa_y = 10

        pygame.draw.rect(tela, (255, 170, 150), (caixa_x, caixa_y, caixa_larg, caixa_alt), border_radius=10)
        pygame.draw.rect(tela, (255, 130, 120), (caixa_x, caixa_y, caixa_larg, caixa_alt), width=3, border_radius=10)

        linha1 = f"Moedas: {j.moedas} | Rum: {j.rum} | Diamantes: {j.diamantes}"
        linha2 = "Chave: Coletada" if j.tem_chave else "Chave: Não coletada"

        tela.blit(FONTE.render(linha1, True, COR_TEXTO), (caixa_x + 10, caixa_y + 15))
        tela.blit(FONTE.render(linha2, True, COR_TEXTO), (caixa_x + 10, caixa_y + 55))

    def mensagem(self, tela, texto):
        largura_caixa = 390
        altura_caixa = 84

        caixa_x = (LARGURA_TELA - largura_caixa) // 2
        caixa_y = (ALTURA_TELA - altura_caixa) // 2

        pygame.draw.rect(tela, (255, 170, 150), (caixa_x, caixa_y, largura_caixa, altura_caixa), border_radius=15)
        pygame.draw.rect(tela, (255, 130, 120), (caixa_x, caixa_y, largura_caixa, altura_caixa), width=4, border_radius=15)

        surf = FONTE.render(texto, True, (255, 255, 255))
        rect = surf.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 12))
        tela.blit(surf, rect)

        if self.vitoria and SPRITE_ESTRELA:
            inicio_x = (LARGURA_TELA - (self.estrelas * 36)) // 2
            y = caixa_y + altura_caixa - 42
            for i in range(self.estrelas):
                tela.blit(SPRITE_ESTRELA, (inicio_x + i * 36, y))

    def calcular_estrelas(self):
        m = self.jogador.moedas
        d = self.jogador.diamantes
        metade_moedas = self.total_moedas / 2

        if m == self.total_moedas and d == self.total_diamantes:
            return 5
        if m == self.total_moedas and d < self.total_diamantes:
            return 4
        if d == self.total_diamantes and m > metade_moedas:
            return 3
        if d == self.total_diamantes and m == 0:
            return 2
        if d == self.total_diamantes and 0 < m <= metade_moedas:
            return 1
        return 1


# LOOP PRINCIPAL


def main():
    fase = Fase()
    rodando = True

    while rodando:
        RELOGIO.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                rodando = False

            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                if fase.game_over or fase.vitoria:
                    # reinicia música e fase
                    iniciar_musica()
                    fase = Fase()

        fase.atualizar()
        fase.desenhar(TELA)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
    