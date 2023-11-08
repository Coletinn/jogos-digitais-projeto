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

som_ligado = True

def alternar_som():
    global som_ligado
    if som_ligado:
        pygame.mixer.music.stop()
    else:
        pygame.mixer.music.play(-1)
    som_ligado = not som_ligado

botao_iniciar = pygame.Rect(largura // 2 - 100, altura // 2 + 10, 200, 50)
cor_botao = (0, 0, 0)

botao_instrucoes = pygame.Rect(largura // 2 - 100, altura // 2 - 70, 200, 50)
cor_botao_instrucoes = (0, 0, 0) 

botao_som = pygame.Rect(largura - 475, altura - 220, 150, 50)

imagem_tsunami = None
mostrar_imagem_tsunami = False
mostrar_caixa_instrucoes = False
fechar_instrucoes = False

texto_instrucoes = [
    "Instruções:",
    "1. Este é um jogo de sobrevivência a um tsunami.",
    "2. Para iniciar o jogo, clique no botão 'Jogar'.",
    "3. Mova os personagens até os lugares seguros para pontuar!.",
    "4. Boa sorte e divirta-se!",
]

class Personagem(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y, escala=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagem)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * escala), int(self.image.get_height() * escala)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

escala_cj = 0.3
escala_bigsmoke = 0.3
personagem_cj = Personagem("cj.png", largura // 3, altura // 1.3, escala_cj)
personagem_bigsmoke = Personagem("bigsmoke.png", largura * 3 // 4, altura // 1.3, escala_bigsmoke)

personagens = pygame.sprite.Group(personagem_cj, personagem_bigsmoke)

executando = True
while executando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executando = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if botao_iniciar.collidepoint(event.pos):
                imagem_tsunami = pygame.image.load("rio-beach.png")
                imagem_tsunami = pygame.transform.scale(imagem_tsunami, (largura, altura))
                mostrar_imagem_tsunami = True
                mostrar_caixa_instrucoes = False
                fechar_instrucoes = False 
            elif botao_instrucoes.collidepoint(event.pos):
                mostrar_caixa_instrucoes = True
            elif botao_som.collidepoint(event.pos):
                alternar_som()
            elif fechar_instrucoes and botao_fechar_instrucoes.collidepoint(event.pos):
                mostrar_caixa_instrucoes = False

    tela.blit(imagem_fundo, (0, 0))

    tela.blit(titulo, retangulo_titulo)
    tela.blit(texto1, retangulo_texto1)
    tela.blit(texto2, retangulo_texto2)
    tela.blit(texto3, retangulo_texto3)

    pygame.draw.rect(tela, cor_botao_instrucoes, botao_instrucoes)
    fonte_botao_instrucoes = pygame.font.SysFont("georgia", 30)
    texto_botao_instrucoes = fonte_botao_instrucoes.render("Instruções", True, (255, 255, 0))
    retangulo_botao_instrucoes = texto_botao_instrucoes.get_rect(center=botao_instrucoes.center)
    tela.blit(texto_botao_instrucoes, retangulo_botao_instrucoes)

    pygame.draw.rect(tela, cor_botao, botao_iniciar)
    fonte_botao = pygame.font.SysFont("georgia", 30)
    texto_botao = fonte_botao.render("Jogar", True, (255, 255, 0))
    retangulo_botao = texto_botao.get_rect(center=botao_iniciar.center)
    tela.blit(texto_botao, retangulo_botao)

    pygame.draw.rect(tela, (0, 255, 0) if som_ligado else (255, 0, 0), botao_som)
    fonte_botao_som = pygame.font.SysFont("georgia", 20)
    texto_botao_som = fonte_botao_som.render("Som: Ligado" if som_ligado else "Som: Desligado", True, (0, 0, 0))
    retangulo_botao_som = texto_botao_som.get_rect(center=botao_som.center)
    tela.blit(texto_botao_som, retangulo_botao_som)

    if mostrar_imagem_tsunami:
        tela.blit(imagem_tsunami, (0, 0))

    personagens.draw(tela)

    if mostrar_caixa_instrucoes:
        pygame.draw.rect(tela, (51, 153, 255), (100, 100, largura - 200, altura - 200))
        fonte_instrucoes = pygame.font.SysFont("georgia", 20)
        y = 150
        for linha in texto_instrucoes:
            texto = fonte_instrucoes.render(linha, True, (255, 255, 0))
            retangulo_texto = texto.get_rect(center=(largura // 2, y))
            tela.blit(texto, retangulo_texto)
            y += 30

        botao_fechar_instrucoes = pygame.Rect(largura - 200, altura - 140, 100, 40)
        pygame.draw.rect(tela, (255, 0, 0), botao_fechar_instrucoes)
        fonte_botao_fechar_instrucoes = pygame.font.SysFont("georgia", 20)
        texto_botao_fechar_instrucoes = fonte_botao_fechar_instrucoes.render("Fechar", True, (255, 255, 255))
        retangulo_botao_fechar_instrucoes = texto_botao_fechar_instrucoes.get_rect(center=botao_fechar_instrucoes.center)
        tela.blit(texto_botao_fechar_instrucoes, retangulo_botao_fechar_instrucoes)
        fechar_instrucoes = True

    pygame.display.flip()

pygame.mixer.music.stop()
pygame.mixer.quit()

pygame.quit()
sys.exit()