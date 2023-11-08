import pygame
import sys

# Inicialize o Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Sobrevivência ao Tsunami")

# Carregue a imagem do tsunami como plano de fundo
imagem_fundo = pygame.image.load("tsunami.png")  # Substitua "tsunami.png" pelo caminho para sua imagem
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))

# Cores
amarelo = (255, 255, 0)

fonte_titulo = pygame.font.SysFont("georgia", 55)  # Use a fonte especificada
fonte_texto = pygame.font.SysFont("georgia", 20)  # Use a fonte especificada

# Defina o estilo do texto em amarelo
fonte_titulo.set_bold(True)  # Torna o texto em negrito
fonte_titulo.set_italic(True)  # Torna o texto em itálico

# Renderize o título
titulo = fonte_titulo.render("Sobrevivência ao Tsunami", True, amarelo)
retangulo_titulo = titulo.get_rect()
retangulo_titulo.center = (largura // 2, altura // 13)

# Renderize o texto
texto1 = fonte_texto.render("Seja bem vindo!", True, amarelo)
texto2 = fonte_texto.render("Neste jogo você irá aprender", True, amarelo)
texto3 = fonte_texto.render("a sobreviver a um tsunami!", True, amarelo)
retangulo_texto1 = texto1.get_rect()
retangulo_texto2 = texto2.get_rect()
retangulo_texto3 = texto3.get_rect()

retangulo_texto1.topright = (largura - 200, 110)
retangulo_texto2.topright = (largura - 90, 140)
retangulo_texto3.topright = (largura - 99, 170)

# Loop principal do jogo
executando = True
while executando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executando = False

    # Desenhe o plano de fundo
    tela.blit(imagem_fundo, (0, 0))

    # Desenhe o título no centro da tela
    tela.blit(titulo, retangulo_titulo)

    # Desenhe o texto no canto superior direito
    tela.blit(texto1, retangulo_texto1)
    tela.blit(texto2, retangulo_texto2)
    tela.blit(texto3, retangulo_texto3)

    # Atualize a tela
    pygame.display.flip()

# Encerre o Pygame
pygame.quit()
sys.exit()