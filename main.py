import pygame
import sys
import time

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

texto1 = fonte_texto.render("Seja bem-vindo!", True, amarelo)
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
som_game_over = pygame.mixer.Sound("game-over.mp3")
som_vitoria = pygame.mixer.Sound("vitoria.mp3")

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
botao_teste = pygame.Rect(largura // 3 - 100, altura // 1.2, 450, 50)
cor_botao_teste = (0, 0, 0) 

botao_som = pygame.Rect(largura - 475, altura - 220, 150, 50)

mostrar_texto_instrucoes = True

botao_correr = pygame.Rect(largura // 2 - 100, altura // 2 + 70, 200, 50)
cor_botao_correr = (0, 0, 0)
mostrar_botao_correr = False

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

pontuacao = 0
temporizador = 0
tempo_entre_colisoes = 1000
temporizador_colisao_cj = 0
temporizador_colisao_bigsmoke = 0

velocidade_onda = 0.6

mostrar_texto_instrucoes = True

class Casa(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y, escala=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagem)
        self.original_image = self.image
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * escala), int(self.image.get_height() * escala)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Helicoptero(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y, escala=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagem)
        self.original_image = self.image
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * escala), int(self.image.get_height() * escala)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Casa(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y, escala=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagem)
        self.original_image = self.image
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * escala), int(self.image.get_height() * escala)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Personagem(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y, escala=1, tipo=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagem)
        self.original_image = self.image
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * escala), int(self.image.get_height() * escala)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.inclinacao = 0
        self.escala_original = escala
        self.velocidade_horizontal = 0
        self.tipo = tipo

    def inclinar(self, angulo):
        self.inclinacao = angulo
        self.image = pygame.transform.rotate(self.original_image, self.inclinacao)
        self.rect = self.image.get_rect(center=self.rect.center)

escala_cj = 0.3
escala_bigsmoke = 0.3
personagem_cj = Personagem("cj.png", largura // 3, altura // 1.3, escala_cj, tipo="CJ")
personagem_bigsmoke = Personagem("bigsmoke.png", largura * 3 // 4, altura // 1.3, escala_bigsmoke, tipo='Big Smoke')
helicoptero_sprite = Helicoptero("helicopter.png", largura // 3, altura // 1.3, 0.3)
cj_resgatado = False
big_smoke_resgatado = False

personagens = pygame.sprite.Group(personagem_cj, personagem_bigsmoke)

sprite_areia = Personagem("areia.png", largura // 4, altura // 1.1, escala=0.4)

tempo_inicial = None
display_victory_message = False

som_vitoria_count = 0
next_level = False

executando = True
while executando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executando = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if botao_iniciar.collidepoint(event.pos):
                tempo_inicial = time.time()
                imagem_tsunami = pygame.image.load("fundo.png")
                imagem_tsunami = pygame.transform.scale(imagem_tsunami, (largura, altura))
                mostrar_imagem_tsunami = True
                mostrar_caixa_instrucoes = False
                fechar_instrucoes = False

                personagens.add(sprite_areia)

                oceano = Personagem("ocean.png", largura // 1.3, altura // 0.99, escala=0.08)
                onda2 = Personagem("tsunami.png", largura // 0.8, altura // 1.3, escala=0.30)
                onda3 = Personagem("tsunami.png", largura * 4 // 4, altura // 1.3, escala=0.20)

                personagens.add(oceano, onda2, onda3)

                onda2.velocidade_horizontal = -velocidade_onda
                onda3.velocidade_horizontal = -velocidade_onda

                personagem_cj.rect.x -= 200
                personagem_cj.rect.y += 12

                personagem_bigsmoke.rect.x -= 350
                personagem_bigsmoke.rect.y += 12

                mostrar_botao_correr = True

            elif botao_instrucoes.collidepoint(event.pos):
                mostrar_caixa_instrucoes = True
            elif botao_som.collidepoint(event.pos):
                alternar_som()
            elif fechar_instrucoes and botao_fechar_instrucoes.collidepoint(event.pos):
                mostrar_caixa_instrucoes = False
            elif mostrar_botao_correr and botao_correr.collidepoint(event.pos):
                print("Correndo!")

            elif botao_teste.collidepoint(event.pos):
                next_level = True

            elif next_level:
                tela.fill((0, 0, 0))
                pygame.display.flip()

            if next_level:
                onda2.rect.x = largura // 0.8
                onda3.rect.x = largura * 4 // 4
                if helicoptero_sprite.rect.collidepoint(event.pos):
                    pontuacao += 100
                    display_victory_message = True

    keys = pygame.key.get_pressed()

    if mostrar_imagem_tsunami:
        if pontuacao < 94:
            if keys[pygame.K_LEFT]:
                personagem_cj.rect.x -= 3
                personagem_bigsmoke.rect.x -= 3
                pontuacao += 1

            for onda in personagens.sprites():
                if isinstance(onda, Personagem) and onda != sprite_areia:
                    onda.rect.x += onda.velocidade_horizontal

            tempo_decorrido = time.time() - tempo_inicial

            if tempo_inicial is not None and tempo_decorrido > 8:
                pygame.mixer.music.stop()

                som_game_over.play()

                tela.fill((0, 0, 0))
                fonte_game_over = pygame.font.SysFont("georgia", 50)
                texto_game_over = fonte_game_over.render("Game Over!", True, (255, 0, 0))
                retangulo_game_over = texto_game_over.get_rect(center=(largura // 2, altura // 2))
                tela.blit(texto_game_over, retangulo_game_over)

                fonte_mensagem_game_over = pygame.font.SysFont("georgia", 25)
                mensagem_game_over = fonte_mensagem_game_over.render("CJ e Big Smoke não correram do tsunami a tempo!", True, (255, 0, 0))
                retangulo_mensagem_game_over = mensagem_game_over.get_rect(center=(largura // 2, altura // 1.7))
                tela.blit(mensagem_game_over, retangulo_mensagem_game_over)
                pygame.display.flip()

                time.sleep(5)
                executando = False

        
    if next_level:
        pass
                        

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

    if mostrar_imagem_tsunami:
        fonte_pontuacao = pygame.font.SysFont("georgia", 30)
        texto_pontuacao = fonte_pontuacao.render(f"Pontuação: {pontuacao}", True, (255, 255, 255))
        tela.blit(texto_pontuacao, (20, 20))

        fonte_mensagem_v1 = pygame.font.SysFont("georgia", 25)
        mensagem_v1 = fonte_mensagem_v1.render("Um Tsunami está vindo!", True, (255, 255, 0))
        retangulo_mensagem_v1 = mensagem_v1.get_rect(center=(largura // 2, altura // 4))
        tela.blit(mensagem_v1, retangulo_mensagem_v1)

        fonte_mensagem_v2 = pygame.font.SysFont("georgia", 25)
        mensagem_v2 = fonte_mensagem_v2.render("Aperte a seta para a esquerda para pontuar e fugir do tsunami!", True, (255, 255, 0))
        retangulo_mensagem_v2 = mensagem_v2.get_rect(center=(largura // 2, altura // 3 ))
        tela.blit(mensagem_v2, retangulo_mensagem_v2)

    if pontuacao >= 94:
        pygame.mixer.music.stop()
        som_vitoria.play()

        fonte_mensagem = pygame.font.SysFont("georgia", 35)
        mensagem = fonte_mensagem.render("VOCE CONSEGUIU CORRER DO TSUNAMI!", True, (255, 255, 0))
        retangulo_mensagem = mensagem.get_rect(center=(largura // 2, 95))
        tela.blit(mensagem, retangulo_mensagem)

        pygame.draw.rect(tela, cor_botao_teste, botao_teste)
        fonte_botao_teste = pygame.font.SysFont("georgia", 30)
        texto_botao_teste = fonte_botao_teste.render("IR PARA PRÓXIMO NÍVEL", True, (255, 255, 0))
        retangulo_botao_teste = texto_botao_teste.get_rect(center=botao_teste.center)
        tela.blit(texto_botao_teste, retangulo_botao_teste)

        if next_level:
            personagens.empty()
            som_vitoria.stop()
            tela.fill((0, 191, 255))
            #onda2 = Personagem("tsunami.png", largura // 0.8, altura // 1.3, escala=0.30)
            #onda3 = Personagem("tsunami.png", largura * 4 // 4, altura // 1.3, escala=0.20)
            sprite_casa1_nextlevel = Casa("house1.png", largura // 2, altura // 1.2, escala=0.4)
            sprite_casa2_nextlevel = Casa("house2.png", largura // 10.5, altura // 1.17, escala=0.4)
            sprite_grama_nextlevel = Personagem("grama.png", largura // 5, altura // 1.17, escala=1)
            sprite_areia_nextlevel = Personagem("areia.png", largura // 1.3, altura // 1.1, escala=0.4)
            cj_next_level = Personagem("cj.png", largura // 1.2, altura // 1.25, escala_cj, tipo="CJ")
            big_smoke_next_level = Personagem("bigsmoke.png", largura * 6 // 8, altura // 1.25, escala_bigsmoke, tipo='Big Smoke')
            helicoptero_sprite = Helicoptero("helicopter.png", largura // 3.5, altura // 1.17, escala=0.3)
            personagens.add(sprite_casa1_nextlevel, sprite_casa2_nextlevel, sprite_grama_nextlevel, sprite_areia_nextlevel, helicoptero_sprite, cj_next_level, big_smoke_next_level)
            personagens.draw(tela)
            fonte_mensagem_proxnivel = pygame.font.SysFont("georgia", 25)
            mensagem_proxnivel = fonte_mensagem_proxnivel.render("Clique no helicóptero para subir e fugir do tsunami!", True, (255, 255, 0))
            retangulo_mensagem_proxnivel = mensagem_proxnivel.get_rect(center=(largura // 2, altura // 5 ))
            tela.blit(mensagem_proxnivel, retangulo_mensagem_proxnivel)

        
    if display_victory_message:
        tela.fill((0, 0, 0))
        fonte_mensagem_vitoria = pygame.font.SysFont("georgia", 30)
        fonte_msg_gameover = pygame.font.SysFont("georgia", 50)
        mensagem_go = fonte_msg_gameover.render("GAME OVER", True, (0, 255, 0))
        mensagem_vitoria1 = fonte_mensagem_vitoria.render("VITÓRIA!!!", True, (255, 255, 255))
        mensagem_vitoria2 = fonte_mensagem_vitoria.render("VOCÊ VOOU COM O HELICÓPTERO E FUGIU!!!", True, (255, 255, 255))
        mensagem_pontuacao = fonte_mensagem_vitoria.render(f"Pontuação final: {pontuacao}", True, (255, 255, 255))
        retangulo_mensagem_go = mensagem_go.get_rect(center=(largura // 2, altura // 5))
        retangulo_mensagem_vitoria1 = mensagem_vitoria1.get_rect(center=(largura // 2, altura // 3))
        retangulo_mensagem_vitoria2 = mensagem_vitoria2.get_rect(center=(largura // 2, altura // 2))
        retangulo_mensagem_pontuacao = mensagem_pontuacao.get_rect(center=(largura // 2, altura // 1.5))
        tela.blit(mensagem_go, retangulo_mensagem_go)
        tela.blit(mensagem_vitoria1, retangulo_mensagem_vitoria1)
        tela.blit(mensagem_vitoria2, retangulo_mensagem_vitoria2)
        tela.blit(mensagem_pontuacao, retangulo_mensagem_pontuacao)
        pygame.display.flip()

    pygame.display.flip()

pygame.mixer.music.stop()
pygame.mixer.quit()

pygame.quit()
sys.exit()