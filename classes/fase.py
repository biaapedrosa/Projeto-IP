import pygame
from .config import *
from .entidades import *
import classes.assets as assets

class Fase:
    def __init__(self):
        self.chao_y = 520
        
        # Grupos de Sprites
        self.todos = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.areia = pygame.sprite.Group()
        self.itens = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.decor = pygame.sprite.Group()

        # Estados e Variáveis
        self.game_over = False
        self.vitoria = False
        self.camera_x = 0
        self.cloud_offset = 0
        self.estrelas = 0
        
        # Contadores para o sistema de estrelas
        self.total_moedas = 0
        self.total_diamantes = 0

        # Inicialização do mapa
        self.criar_terreno()
        self.criar_jogador()
        self.criar_inimigos()
        self.criar_itens()
        self.criar_navio()
        self.criar_coqueiros()


    # MÉTODOS DE CRIAÇÃO (SETUP)
    def criar_terreno(self):
        plataformas_coords = [
            (400, 420, 150),
            (700, 360, 120),
            (1100, 450, 200),
            (1500, 420, 200),
        ]
        for x, y, w in plataformas_coords:
            p = Plataforma(x, y, w)
            self.plataformas.add(p)
            self.todos.add(p)

        areias_coords = [(900, 200), (2000, 180)]
        for x, w in areias_coords:
            a = AreiaMovedica(x, self.chao_y, w)
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
        # Moedas
        coords_moedas = [(300, 480), (450, 380), (510, 380), (750, 330), (1150, 420)]
        for x, y in coords_moedas:
            m = Moeda(x, y)
            self.itens.add(m)
            self.todos.add(m)
            self.total_moedas += 1

        # Diamantes
        coords_diamantes = [(950, 460), (2050, 460), (2750, 310)]
        for x, y in coords_diamantes:
            d = Diamante(x, y)
            self.itens.add(d)
            self.todos.add(d)
            self.total_diamantes += 1

        # Rum (Power-up)
        for x, y in [(1600, 460), (3200, 460)]:
            r = GarrafaRum(x, y)
            self.itens.add(r)
            self.todos.add(r)

        # Chave
        c = Chave(3400, 440)
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


    # LÓGICA E ATUALIZAÇÃO
    def atualizar(self):
        if self.game_over or self.vitoria:
            return

        # Timer do Super Pulo
        if self.jogador.super_pulo:
            if pygame.time.get_ticks() - self.jogador.super_pulo_timer >= 6000:
                self.jogador.super_pulo = False

        teclas = pygame.key.get_pressed()

        # Lógica da Areia (Redução de velocidade)
        em_areia = any(self.jogador.rect.colliderect(a.hitbox) for a in self.areia)
        self.jogador.vel_x = 3 if em_areia else 5

        # Movimentação do Jogador
        self.jogador.mover_horizontal(teclas, self.plataformas)
        self.jogador.mover_vertical(self.plataformas, self.chao_y)

        if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and self.jogador.no_chao:
            self.jogador.pular()

        self.jogador.atualizar_animacao()

        # Inimigos
        for inimigo in self.inimigos:
            inimigo.update(self.plataformas, self.chao_y)

        # Colisões com Itens
        coletados = pygame.sprite.spritecollide(self.jogador, self.itens, True)
        for item in coletados:
            item.aplicar(self.jogador)

        # Condição de Vitória (Navio + Chave)
        if self.jogador.rect.colliderect(self.navio.rect) and self.jogador.tem_chave:
            self.vitoria = True
            self.estrelas = self.calcular_estrelas()
            if assets.SOM_VITORIA: assets.tocar(assets.SOM_VITORIA)

        # Condição de Derrota (Inimigos ou Queda)
        if pygame.sprite.spritecollideany(self.jogador, self.inimigos):
            self.game_over = True
            assets.tocar(assets.SOM_INIMIGO)
            assets.tocar(assets.SOM_GAMEOVER)

        if self.jogador.rect.top > ALTURA_TELA + 100:
            self.game_over = True
            assets.tocar(assets.SOM_GAMEOVER)

        # Câmera e Parallax
        self.camera_x = max(0, min(self.jogador.rect.centerx - LARGURA_TELA // 2, WORLD_WIDTH - LARGURA_TELA))
        if assets.NUVENS_IMAGEM:
            self.cloud_offset += 0.3

    def calcular_estrelas(self):
        m = self.jogador.moedas
        d = self.jogador.diamantes
        metade_moedas = self.total_moedas / 2

        if m == self.total_moedas and d == self.total_diamantes: return 5
        if m == self.total_moedas: return 4
        if d == self.total_diamantes and m > metade_moedas: return 3
        if d == self.total_diamantes: return 2
        return 1


    # DESENHO (RENDER)
    def desenhar(self, tela):
        # Fundo e Nuvens
        if assets.BG_IMAGE:
            tela.blit(assets.BG_IMAGE, (0, 0))
        else:
            tela.fill(COR_CEU)

        if assets.NUVENS_IMAGEM:
            larg = assets.NUVENS_IMAGEM.get_width()
            x_base = -self.cloud_offset % larg
            for i in range(3):
                tela.blit(assets.NUVENS_IMAGEM, (x_base + i * larg, 20))

        # Chão
        pygame.draw.rect(tela, COR_CHÃO, pygame.Rect(-self.camera_x, self.chao_y, WORLD_WIDTH, ALTURA_TELA))

        # Sprites com Câmera
        for s in self.todos:
            tela.blit(s.image, (s.rect.x - self.camera_x, s.rect.y))

        # HUD e Mensagens
        self.desenhar_hud(tela)

        if self.game_over:
            self.mensagem(tela, "GAME OVER – Pressione R")
        elif self.vitoria:
            self.mensagem(tela, "VOCÊ ZARPOU! – Pressione R")

        # Aviso de Super Pulo
        if self.jogador.super_pulo:
            texto = assets.FONTE.render("SUPER PULO ATIVO!", True, (0, 0, 139))
            tela.blit(texto, (LARGURA_TELA // 2 - texto.get_width() // 2, 170))

    def desenhar_hud(self, tela):
        pygame.draw.rect(tela, (255, 170, 150), (10, 10, 350, 95), border_radius=10)
        pygame.draw.rect(tela, (255, 130, 120), (10, 10, 350, 95), width=3, border_radius=10)

        j = self.jogador
        linha1 = f"Moedas: {j.moedas} | Rum: {j.rum} | Diamantes: {j.diamantes}"
        linha2 = "Chave: Coletada" if j.tem_chave else "Chave: Não coletada"

        if assets.FONTE:
            tela.blit(assets.FONTE.render(linha1, True, COR_TEXTO), (20, 25))
            tela.blit(assets.FONTE.render(linha2, True, COR_TEXTO), (20, 55))

    def mensagem(self, tela, texto):
        larg_c, alt_c = 390, 84
        cx, cy = (LARGURA_TELA - larg_c) // 2, (ALTURA_TELA - alt_c) // 2
        
        pygame.draw.rect(tela, (255, 170, 150), (cx, cy, larg_c, alt_c), border_radius=15)
        pygame.draw.rect(tela, (255, 130, 120), (cx, cy, larg_c, alt_c), width=4, border_radius=15)

        if assets.FONTE:
            surf = assets.FONTE.render(texto, True, (255, 255, 255))
            rect = surf.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 12))
            tela.blit(surf, rect)

        # Estrelas na vitória
        if self.vitoria and assets.SPRITE_ESTRELA:
            inicio_x = (LARGURA_TELA - (self.estrelas * 36)) // 2
            for i in range(self.estrelas):
                tela.blit(assets.SPRITE_ESTRELA, (inicio_x + i * 36, cy + alt_c - 42))