import pygame
import sys

pygame.init()

pygame.mixer.init()

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Sobrevivência ao Tsunami")

imagem_fundo = pygame.image.load("game-beach.jpg")
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))

amarelo = (255, 255, 0)

fonte_titulo = pygame.font.SysFont("georgia", 55)
fonte_texto = pygame.font.SysFont("georgia", 20)

fonte_titulo.set_bold(True)
fonte_titulo.set_italic(True)

titulo = fonte_titulo.render("Sobrevivência ao Tsunami", True, amarelo)
retangulo_titulo = titulo.get_rect()
retangulo_titulo.center = (largura // 2, altura // 13)

texto1 = fonte_texto.render("Seja bem vindo!", True, amarelo)
texto2 = fonte_texto.render("Neste jogo você irá aprender", True, amarelo)
texto3 = fonte_texto.render("a sobreviver a um tsunami!", True, amarelo)
retangulo_texto1 = texto1.get_rect()
retangulo_texto2 = texto2.get_rect()
retangulo_texto3 = texto3.get_rect()

retangulo_texto1.topright = (largura - 350, 80)
retangulo_texto2.topright = (largura - 240, 105)
retangulo_texto3.topright = (largura - 250, 130)

pygame.mixer.music.load("san-andreas-music.mp3")
pygame.mixer.music.play(-1)

executando = True
while executando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executando = False

    tela.blit(imagem_fundo, (0, 0))

    tela.blit(titulo, retangulo_titulo)

    tela.blit(texto1, retangulo_texto1)
    tela.blit(texto2, retangulo_texto2)
    tela.blit(texto3, retangulo_texto3)

    pygame.display.flip()

pygame.mixer.music.stop()
pygame.mixer.quit()

pygame.quit()
sys.exit()