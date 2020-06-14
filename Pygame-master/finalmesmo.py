#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:04:17 2020

@author: Alex
"""

INIT = 0
GAME = 1
INSTRUCOES = 2
QUIT = 3

VERD = (160, 231, 190)
VERM = (205, 44, 65)
AZUL = (139, 165, 235)
AMAR = (204, 173, 26)
LISTA_CORES=[VERM, AMAR, VERD, AZUL]


# Importando as bibliotecas usadas.
import pygame
import random
from os import path

# Estabelece a pasta que contem as imagens.
img_dir = path.join(path.dirname(__file__), 'Imagens')
fnt_dir = path.join(path.dirname(__file__), 'Fonte')

# informaçoes gerais do jogo.
WIDTH = 1200 # Largura da tela
HEIGHT = 700 # Altura da tela
FPS = 30 # Frames por segundo

# Define algumas variáveis com as cores básicas
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL1 = (0, 0, 255)
AMARELO = (255, 255, 0)

#criando a classe dos frutinhas
class Pontinhos(pygame.sprite.Sprite):
    
    #Construtor da classe
    def __init__(self, x, y):
        arquivo_cores = ["ponto_vermelho.jpg", "ponto_amarelo.jpg", "ponto_verde.jpg", "ponto_azul.jpg"]
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a foto de fundo.
        self.cor = random.randint(0,3)
        player_img = pygame.image.load(path.join(img_dir, arquivo_cores[self.cor])).convert()

        self.image = player_img
        
        # Botando imagem em escala.
        self.image = pygame.transform.scale(player_img, (60, 60))
        
        # Deixando transparente.
        self.image.set_colorkey(BRANCO)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Centraliza embaixo da tela.
        self.rect.x = x
        self.rect.y = y
        
        # Velocidade de movimento
        self.speedx = 0
        
    # Metodo que atualiza posição
    def update(self):
        self.rect.x += self.speedx
        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Pygame")

def jogo(screen):
    jogadas_maximas = []
    jogadas_maximas.append({"jogada": 5, "cor" :[0, 5, 0, 0]})
    jogadas_maximas.append({"jogada": 5, "cor" :[2, 0, 0, 2]})
    jogadas_maximas.append({"jogada": 15, "cor" :[2, 2, 2, 0]})
    jogadas_maximas.append({"jogada": 10, "cor" :[2, 2, 2, 2]})
    jogadas_maximas.append({"jogada": 5, "cor" :[2, 0, 0, 0]})

    for conta_fase, params in enumerate(jogadas_maximas):
        res = qual_fase(screen, conta_fase + 1)
        if res == QUIT:
            break
        
        res = level(screen, params["jogada"], params["cor"])
        if res == QUIT:
            break
        
    return QUIT

def level(screen, qtd_jogadas, cores):
    pontuacao = [0, 0, 0, 0]
    
    score_fonte = pygame.font.Font(path.join(fnt_dir, "DK Lemon Yellow Sun.otf"), 28)
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    
    
    # Carrega o fundo do jogo
    inicio = pygame.image.load(path.join(img_dir, 'tela_inicial.jpg')).convert()
    inicio = pygame.transform.scale(inicio,(WIDTH, HEIGHT))
    
    background = pygame.image.load(path.join(img_dir, 'fundo.png')).convert()
    background = pygame.transform.scale(background,(WIDTH, HEIGHT))
    background_rect = background.get_rect()
    
    #Carrega imagem quadrado
    quadrado = pygame.image.load(path.join(img_dir, 'quadrado.png')).convert()
    quadrado.set_colorkey(BRANCO)
    quadrado = pygame.transform.scale(quadrado,(600, 600))
    
    
    # Cria um grupo de sprites e adiciona a nave.
    all_sprites = pygame.sprite.Group()
    
    x_init = 345 
    y_init = HEIGHT-7*79
    
    x = x_init
    y = y_init
    tamanho_bolinha = 76
    tabuleiro_bolinha = []
    for e in range(7):
        linha_bolinha = []
        for i in range(7):
            a1 = Pontinhos(x, y)
            all_sprites.add(a1)
            linha_bolinha.append(a1)
            x += tamanho_bolinha
        tabuleiro_bolinha.append(linha_bolinha)
        y += tamanho_bolinha
        x = x_init
        
    
    lista_pontinhos = []
    cor = None
    
    qnt_jogadas = qtd_jogadas
    jogadas_amar = 0
    
    # Loop principal.
    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                posy = event.pos[1]
                j_frutinha = int((posx - x_init)/tamanho_bolinha)
                i_frutinha = int((posy- y_init)/tamanho_bolinha)
                
                if i_frutinha >= 0 and i_frutinha < 7 \
                    and j_frutinha >= 0 and j_frutinha < 7 \
                    and tabuleiro_bolinha[i_frutinha][j_frutinha]:
                    if len(lista_pontinhos) == 0:
                        cor = tabuleiro_bolinha[i_frutinha][j_frutinha].cor
                        lista_pontinhos.append((i_frutinha, j_frutinha, cor, posx,posy))
                    else:
                        nova_cor = tabuleiro_bolinha[i_frutinha][j_frutinha].cor

                        if len(lista_pontinhos) == 1 and cor != nova_cor:
                            lista_pontinhos = []
                            cor = tabuleiro_bolinha[i_frutinha][j_frutinha].cor
                            if e not in lista_pontinhos:
                                lista_pontinhos.append((i_frutinha, j_frutinha, cor, posx,posy))
                        else:
                            nova_cor = tabuleiro_bolinha[i_frutinha][j_frutinha].cor
                            ultima_frutinha = lista_pontinhos[-1]
                            nova_frutinha = (i_frutinha, j_frutinha, nova_cor, posx, posy)
                            diferenca = (abs(ultima_frutinha[0] - i_frutinha), abs(ultima_frutinha[1] - j_frutinha))
                            if diferenca in [(1, 0), (0, 1)] and ultima_frutinha[2] == nova_cor and not nova_frutinha in lista_pontinhos:
                                lista_pontinhos.append(nova_frutinha)
                    print(lista_pontinhos)
                       
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(lista_pontinhos) > 1:
                        pontuacao[cor] += len(lista_pontinhos)
                        for b in lista_pontinhos:
                            i_frutinha = b[0]
                            j_frutinha = b[1]
                            tabuleiro_bolinha[i_frutinha][j_frutinha].kill()
                            tabuleiro_bolinha[i_frutinha][j_frutinha] = None                            
                        lista_pontinhos = []
                        qnt_jogadas -= 1
                        cor = None
                        if qnt_jogadas == 0:
                            running = False
                        
                        
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False

        for j in range(7):
            p = 6
            q = 6
            while p >= 0:
                
                if tabuleiro_bolinha[p][j] != None:
                    tabuleiro_bolinha[q][j] = tabuleiro_bolinha[p][j]
                    tabuleiro_bolinha[q][j].rect.x = x_init + j*tamanho_bolinha
                    tabuleiro_bolinha[q][j].rect.y = y_init + q*tamanho_bolinha
                    q -= 1
                p -= 1
                
            while q >= 0:
                a1 = Pontinhos(x_init + j*tamanho_bolinha, y_init + q*tamanho_bolinha)
                all_sprites.add(a1)
                tabuleiro_bolinha[q][j] = a1
                q -= 1
                

        # Depois de processar os eventos.
        # Atualiza a ação de cada sprite.
        all_sprites.update()
    
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(PRETO)
        screen.blit(background, background_rect)
        screen.blit(quadrado, [300, 100])
        all_sprites.draw(screen)
        
        for i in range(1, len(lista_pontinhos)):
            ba = lista_pontinhos[i - 1]
            bb = lista_pontinhos[i]
            
            xa = ba[1] * tamanho_bolinha + (x_init + 30.5)
            ya = ba[0] * tamanho_bolinha + (y_init + 30.5)
            
            xb = bb[1] * tamanho_bolinha + (x_init + 30.5)
            yb = bb[0] * tamanho_bolinha + (y_init + 30.5)

            cor_usada = LISTA_CORES[cor]
            
            pygame.draw.line(screen, cor_usada, (xa, ya), (xb, yb), 10)
                    
      
        text_surface = score_fonte.render(f"SCORE: {jogadas_amar}", True, PRETO)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH-110,  110)
        screen.blit(text_surface, text_rect)

        text_surface = score_fonte.render(f"JOGADAS: {qnt_jogadas}", True, PRETO)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH-105, 150)
        screen.blit(text_surface, text_rect)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

        # Monta o score.
        jogadas_amar = 0
        for k in range(len(cores)):
            if pontuacao[k] <= cores[k]:
                jogadas_amar += pontuacao[k]
            else:
                jogadas_amar += cores[k]
        
        # Checa se o objetivo foi atingido:
        venceu = True
        for k in range(len(cores)):
            if pontuacao[k] < cores[k]:
                venceu = False
        
        if venceu:
            return screen # Mudar isso!
        
    
    return QUIT


def screen_init(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(img_dir, 'tela_inicial.jpg')).convert()
    background_rect = background.get_rect()

    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False

            if event.type == pygame.KEYUP:
                state = GAME
                running = False
                
            if pygame.mouse.get_pressed()[0]:
                
                #Pega a posição do click
                x,y = pygame.mouse.get_pos()
                if (x > 405 and y > 285) and (x > 405 and y < 434) and (x < 770 and y < 434) and (x < 770 and y > 285):
                     state = GAME
                     running = False
                elif (x > 405 and y > 484) and (x > 405 and y < 622) and (x < 747 and y < 629) and (x < 741 and y > 475):
                     state = INSTRUCOES
                     running = False


                print("click {0},{1}".format(x,y))
                
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(PRETO)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state


def inst(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    background = pygame.image.load(path.join(img_dir, 'objetivo.jpg')).convert()
    background_rect = background.get_rect()

    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
                
            if pygame.mouse.get_pressed()[0]:
                
                #Pega a posição do click                    
                x,y = pygame.mouse.get_pos()
                if (x > 885 and y > 576) and (x > 893 and y < 662) and (x < 1117 and y < 668) and (x < 1114 and y > 571):
                     state = GAME #nivel1
                     running = False

                print("click {0},{1}".format(x,y))
                
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(PRETO)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state

def qual_fase(screen, numero_fases):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    tela = "nivel{0}.jpg".format(numero_fases)
    background = pygame.image.load(path.join(img_dir, tela)).convert()
    background_rect = background.get_rect()

    running = True
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
                
            if pygame.mouse.get_pressed()[0]:
                x,y = pygame.mouse.get_pos()
                if (x > 885 and y > 576) and (x > 893 and y < 662) and (x < 1117 and y < 668) and (x < 1114 and y > 571):
                    state = GAME
                    running = False
                    
        screen.fill(PRETO)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state


try:
    state = INIT
    while state != QUIT:
        if state == INIT:
            state = screen_init(screen)
        elif state == GAME:
            state = jogo(screen)
        elif state == INSTRUCOES:
            state = inst(screen)
        else:
            state = QUIT
finally:
    pygame.quit()


