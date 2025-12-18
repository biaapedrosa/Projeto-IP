import pygame
import sys
from classes.config import *
import classes.assets as assets
from classes.fase import Fase

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    pygame.display.set_caption("Zarpar!")
    TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    RELOGIO = pygame.time.Clock()


    # CARREGAMENTO DOS ASSETS
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
    
    # Carregar o Sprite da Estrela (importante para a vitória)
    assets.SPRITE_ESTRELA = assets.carregar_imagem("estrela.png")
    if assets.SPRITE_ESTRELA:
        assets.SPRITE_ESTRELA = pygame.transform.scale(assets.SPRITE_ESTRELA, (32, 32))

    assets.BG_IMAGE = assets.carregar_imagem("background.png", LARGURA_TELA, ALTURA_TELA)
    assets.NUVENS_IMAGEM = assets.carregar_imagem("nuvens.png")
    assets.FONTE = pygame.font.SysFont("arial", 18, bold=True)

    # Sons
    assets.SOM_PULO = assets.carregar_som("pulo.wav")
    assets.SOM_MOEDA = assets.carregar_som("moeda.ogg")
    assets.SOM_DIAMANTE = assets.carregar_som("diamante.wav")
    assets.SOM_RUM = assets.carregar_som("rum.wav")
    assets.SOM_INIMIGO = assets.carregar_som("inimigo.wav")
    assets.SOM_VITORIA = assets.carregar_som("vitoria.wav")
    assets.SOM_GAMEOVER = assets.carregar_som("gameover.wav")

    # Iniciar o objeto da Fase
    fase = Fase()
    rodando = True

    while rodando:
        RELOGIO.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                rodando = False
            
            # Lógica de Reinício (SÓ FUNCIONA EM GAME OVER OU VITÓRIA)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                if fase.game_over or fase.vitoria:
                    fase = Fase() # Reinicia a fase do zero

        # Atualiza a lógica (só roda se não for fim de jogo)
        fase.atualizar()
        
        # Desenha tudo 
        fase.desenhar(TELA)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()