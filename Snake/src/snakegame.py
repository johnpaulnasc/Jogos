import pygame
from pygame.locals import *
from sys import exit
from random import randint


pygame.init()

pygame.mixer.music.set_volume(0.1)
musica_de_fundo = pygame.mixer.music.load('BoxCat Games - eCommerce.mp3')
pygame.mixer.music.play(-1)

barulho_colisao = pygame.mixer.Sound('smw_1-up.wav')

largura = 640
altura = 480

x_snake = int(largura/2)
y_snake = int(altura/2)

velocidade = 10
x_controle = velocidade
y_controle = 0


x_comida = randint(40, 600)
y_comida = randint(50, 430)

pontos = 0
fonte = pygame.font.SysFont('arial', 40, bold=True, italic=True)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("SNAKE!!")
relogio = pygame.time.Clock() 
lista_snake = []
comprimento_inicial = 5
morreu = False

def aumenta_snake(lista_snake):
    for XeY in lista_snake:
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 20, 20))

def reinicia_jogo():
    global pontos, comprimento_inicial, x_snake, y_snake, lista_snake, lista_cabeca, x_comida, y_comida, morreu
    pontos = 0
    comprimento_inicial = 5
    x_snake = int(largura/2)
    y_snake = int(altura/2)
    lista_snake = []
    lista_cabeca = []
    x_comida = randint(40, 600)
    y_comida = randint(50, 430)
    morreu = False


while True:
    relogio.tick(30)
    tela.fill((255, 255, 255))
    mensagem = f'Pontos: {pontos}'
    texto_formatado = fonte.render(mensagem, False, (0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = -velocidade
                    y_controle = 0
            if event.key == K_d:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            if event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                 y_controle = -velocidade
                 x_controle = 0
            if event.key == K_s:
                if y_controle == -velocidade:
                    pass
                else:
                    y_controle = velocidade
                    x_controle = 0
                

    x_snake = x_snake + x_controle
    y_snake = y_snake + y_controle

    
    snake = pygame.draw.rect(tela, (0, 255, 0), (x_snake, y_snake, 20, 20))
    comida = pygame.draw.rect(tela, (255, 0, 0), (x_comida, y_comida, 20, 20))

    if snake.colliderect(comida):
        x_comida = randint(40, 600)
        y_comida = randint(50, 430)
        pontos = pontos + 1
        barulho_colisao.play()
        comprimento_inicial = comprimento_inicial + 1

    lista_cabeca = []
    lista_cabeca.append(x_snake)
    lista_cabeca.append(y_snake)
    
    lista_snake.append(lista_cabeca)

    if lista_snake.count(lista_cabeca) > 1:
        fonte2 = pygame.font.SysFont('arial', 20, True, True)
        mensagem1 = 'GAME OVER!'
        mensagem2 = ' Pressione a tecla R para jogar novamente'
        texto_formatado1 = fonte2.render(mensagem1, True, (0, 0, 0))
        texto_formatado2 = fonte2.render(mensagem2, True, (0, 0, 0))
        
        ret_texto1 = texto_formatado1.get_rect()
        ret_texto2 = texto_formatado2.get_rect()
        
        morreu = True
        while morreu:
            tela.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reinicia_jogo()

            ret_texto1.center = (320 , 240)
            ret_texto2.center = (320, 300)
            tela.blit(texto_formatado1, ret_texto1)
            tela.blit(texto_formatado2, ret_texto2)
            pygame.display.update()

    if x_snake > largura:
        x_snake = 0
    if x_snake < 0:
        x_snake = largura
    if y_snake < 0:
        y_snake = altura
    if y_snake > altura:
        y_snake = 0

    if len(lista_snake) > comprimento_inicial:
        del lista_snake[0]

    aumenta_snake(lista_snake)
        
    tela.blit(texto_formatado, (400, 40))
    
    pygame.display.update()
    
