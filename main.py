import pygame
import sys
from classes.config import *
import classes.assets as assets
from classes.fase import Fase

def main():
    pygame.init()
    # Inicialização robusta do som
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.font.init()

    pygame.display.set_caption("Zarpar!")
    TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    RELOGIO = pygame.time.Clock()

    # CARREGAMENTO
    assets.SPRITE_PLATAFORMA = assets.carregar_imagem("obstaculo.png")
    assets.SPRITE_JOGADOR_IDLE = assets.carregar_imagem("pirata.png")
    assets.SPRITE_JOGADOR_WALK = assets.carregar_imagem("pirata_andando.png")
    assets.SPRITE_JOGADOR_JUMP = assets.carregar_imagem("pirata_pulando.png")
    assets.SPRITE_INIMIGO = assets.carregar_imagem("carangueijo.png")
    assets.SPRITE_MOEDA = assets.carregar_imagem("moeda.png")
    assets.SPRITE_RUM = assets.carregar_imagem("rum.png")
    assets.SPRITE_DIAMANTE = assets.carregar_imagem("diamante.png")
    assets.SPRITE_CHAVE = assets.carregar_imagem("chave.png")
    assets.SPRITE_NAVIO = assets.carregar_imagem("navio.png")
    assets.SPRITE_COQUEIRO = assets.carregar_imagem("coqueiro.png")
    assets.SPRITE_AREIA = assets.carregar_imagem("areia.png")
    assets.SPRITE_ESTRELA = assets.carregar_imagem("estrela.png", 32, 32)

    assets.BG_IMAGE = assets.carregar_imagem("background.png", LARGURA_TELA, ALTURA_TELA)
    assets.NUVENS_IMAGEM = assets.carregar_imagem("nuvens.png")

    if assets.NUVENS_IMAGEM:
        assets.NUVENS_IMAGEM = pygame.transform.scale(
            assets.NUVENS_IMAGEM, (250, 150)
        )

    assets.FONTE = pygame.font.SysFont("arial", 18, bold=True)

    # SONS
    assets.SOM_PULO = assets.carregar_som("pulo.wav")
    assets.SOM_MOEDA = assets.carregar_som("moeda.wav")
    assets.SOM_DIAMANTE = assets.carregar_som("diamante.wav")
    assets.SOM_RUM = assets.carregar_som("rum.wav")
    assets.SOM_INIMIGO = assets.carregar_som("inimigo.wav")
    assets.SOM_VITORIA = assets.carregar_som("vitoria.wav")
    assets.SOM_GAMEOVER = assets.carregar_som("gameover.wav")

    # Tocar música de fundo 
    assets.iniciar_musica("musica_fundo.ogg", 0.2) 

    fase = Fase()
    rodando = True

    while rodando:
        RELOGIO.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                rodando = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                if fase.game_over or fase.vitoria:
                    fase = Fase() # Reinicia
                    assets.iniciar_musica("musica_fundo.mp3", 0.2)

        fase.atualizar()
        fase.desenhar(TELA)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()