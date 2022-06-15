import pygame
import os
import random

# [ATENÇÃO!]
# Esse código não é de minha autoria, apenas foi objeto de estudo. 
# Peguei esse código de um evento produzido pelo canal Hashtag Programação o qual pegou de outro canal
# O conteúdo desse código entra no escopo de Programação orientada a objetos. Usando conceitos como classe e afins
# Atento que estou no inicio de estudo e é possivel que haja más explicações e equívocos.

TELA_LARGURA = 500
TELA_ALTURA  = 800  
# Definição do tamanho da tela de jogo(semelhante a uma tela de celular/mobile)

IMAGEM_CANO       = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png'))) # Uso de funcoes do pygame para :
IMAGEM_CHAO       = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png'))) #  1 Aumentar a escala da imagem adicionada pelo .tranform.scale2x (dobrando o tamanho[2x]);
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))   #  2 Dar load em uma imagem atraves do [pygame.image.load("NOME_IMAGEM")];
                                                                                                 #   2.1 Como os arquivos estao em pastas diferentes, a extesao os trata de juntar a pasta das imagens para a do jogo [os.path.join('PASTA','ARQUIVO')] 
IMAGENS_PASSARO   = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))), # Mesma coisa das outras atribuicoes, entretanto, como o passaro muda de posicao dependendo do estado dele, ele tem 3 imagens (Subindo, Pairando, Caindo)
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))), # Essas imagens entram na mesma constanto em formato de lista, podendo ser acessada atraves do index IMAGENS_PASSARO[0...2]
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png')))  
]

pygame.font.init() # Incremento da fonte no jogo (Tabela de pontuacao)
FONTE_PONTOS = pygame.font.SysFont('arial',50) # Definicao da fonte atraves de funcoes do pygame

# Definicao dos objetos do jogo, ou seja, o que ira se mover dentro do jogo e seus respectivos atributos.
# Cada elemento sera uma classe dentro do python e tera seus atributos definidos e seus métodos(o que ele pode fazer, suas funcoes)


class Passaro:
    IMGS = IMAGENS_PASSARO
    # animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x               = x       # Posição inicial no eixo x
        self.y               = y       # Posição inicial no eixo y
        self.angulo          = 0       # angulo de posiçãod do passaro
        self.velocidade      = 0       # velocidade de movimentação
        self.altura          = self.y  # altura do passaro na tela
        self.tempo           = 0       # tempo de animação, para o movimento do pássaro
        self.contagem_imagem = 0       # saber qual imagem está sendo usada (1...3)
        self.imagem          = self.IMGS[0] # qual imagem ele começa

    def pular(self):
        self.velocidade = -10.5         # Velocidade de movimentação do pássaro
        self.tempo = 0                  # É o tempo de animação do pássaro. A cada pulo, esse tempo zera e a medida que vai decorrendo, o passaro se movimenta para baixo(animação dele caindo) até pular novamente, onde o tempo zera e tudo recomeça
        self.altura = self.y            # Posição dele no mapa

        #Adendo: O deslocamento dos elementos do jogo se faz em um plano cartesiano com o eixo Y invertido. Ou seja, para subir, descresce o Y, e para descer, aumenta. (pouco confuso)
    def mover(self):
        # Calcular o deslocamento:
        self.tempo += 1
        deslocamento = (1.5 * (self.tempo**2)) + (self.velocidade * self.tempo)  # O calculo do deslocamento se da baseado na fórmula: S = So + (Vo*t) + (a*t**2)/2 . Conhecida como Sorvetão na fisica, sendo a formula de deslocamento no espaço dentro de um certo tempo

        # Restrigir o deslocamento:
        if deslocamento > 16: #Serve para definir um deslocamento máximo para o pássaro
            deslocamento = 16 
        elif deslocamento < 0: # Ajuste para aumentar o deslocamento e facilitar o jogo
            deslocamento -= 2 

        self.y += deslocamento

        # Angulo do pássaro
        if deslocamento < 0 or self.y < (self.altura + 50): # Se a nova posição Y(pós pulo) dele ainda estiver acima da ultima (pre pulo), o pássaro se manterá com o angulo para cima
            if self.angulo < self.ROTACAO_MAXIMA:           # Colocar o pássaro sempre com o máximo angulo até começar virar para baixo()
                self.angulo = self.ROTACAO_MAXIMA
        else: 
            if self.angulo > -90:                           # Mantém o pássaro no angulo máximo para baixo, ou seja, virado totalmente para o chão (-90°)
                self.angulo -= self.VELOCIDADE_ROTACAO

        
    def desenhar(self,tela ):
        # Definir qual imagem do pássaro usar
        self.contagem_imagem += 1

        if self.contagem_imagem   < self.TEMPO_ANIMACAO:    # Essas condições servem para definir a animação de bater de asas do pássaro. 
            self.imagem = self.IMGS[0]                      # A parti do tempo de animação*4 + 1, o contador zera para manter a animação em loop enquanto o jogo estiver rodando.
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= (self.TEMPO_ANIMACAO*4) + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0
  

        # Se o pássaro estiver caindo, a asa não vai bater, logo mantendo a animação simulando queda(asa para cima)
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2  
        
        # Desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)     # Função para por na tela a imagem do pássaro e rotacionar ela. Ou seja, é a função que torna visível o elemento e seus atributos
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center # Pega o ponto central da imagem
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)          # Cria um "retangulo", uma espécie de "hitbox" em volta do desenho para poder desenha-lo na tela
        tela.blit(imagem_rotacionada, retangulo.topleft)                           # Põem na tela, de fato, a imagem se baseando no aresta do topo a esquerda do retângulo (top-left)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)  # Cria uma máscara de colisão no pássaro. Essa de fato é uma hitbox em volta dos pixeis próprios do pássaro em vez de criar um retângulo em volta do elemento. Ele testa se houve colisão precisa com a imagem do pássaro.


class Cano:
    DISTANCIA = 200  # Distancia entre os canos. Tomando aqui dois como um. Os canos de baixo e de cima como um e essa é a distância entre eles
    VELOCIDADE = 5   # Velocidade de movimentação deles


    def __init__ (self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0        # Altura do cano de cima
        self.pos_base = 0        # Altura do cano de baixo
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)  # flipar a imagem(inverter ela). Sendo o primeiro valor a imagem do cano, o segundo se desejamos inverter no eixo X e o terceiro se desejamos inverter no eixo Y.
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False      # Se o cano passou do pássaro
        self.definir_altura()


    def definir_altura(self):
        self.altura = random.randrange(50,450)                     # Define uma altura aleatória dentro de um range limitado dos 800pixeis de altura da tela
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()  # A posição do topo é a altura dele menos o tamanho do cano
        self.pos_base = self.altura + self.DISTANCIA               # É a posição do cano_topo com a diferença de 200 pixeis

    def mover(self):
        self.x -= self.VELOCIDADE   # Como a base de localização do pygame é um plano cartesiano, para mover algo da direita para esquerda, subtrai x para que ele vá até o centro, dai o  '-='.


    def desenhar(self,tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))  # função que irão por o elemento na tela(desenha-lo), usando a imagem e sua coordenada na tela
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro) :
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))  # Calcula a distância entre o pássaro e o cano de cima/baixo e retorna em coordenadas.
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)  # .overlap identifica se houve colisão entre pixeis. Testando se há dois píxeis no mesmo lugar retornando um booleano (True, False)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)  

        if base_ponto or topo_ponto:   # Testa o conflito. Se houve ou não colisão entre o passaro e algum cano
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5
    LARGURA    = IMAGEM_CHAO.get_width()  # Pega a largura do chão
    IMAGEM     = IMAGEM_CHAO

    def __init__(self, y):
        self.y  = y
        self.x1 = 0                       # Definição do primeiro chão
        self.x2 = self.x1 + self.LARGURA  # Definição do segundo. 
                                          # Tais definições servem para manter a 'loopicidade' da animação do chão, tendo dois que ficam passando pela tela
        
    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0 :   #Testa para saber se o chão saiu da tela, caso True, o chão move para a posição inicial à direita
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0 :
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))  # função que irão por o elemento na tela(desenha-lo), usando a imagem e sua coordenada na tela
        tela.blit(self.IMAGEM, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0)) # Desenhar o fundo da tela, a imagem de background
    for passaro in passaros:             # Adaptado para poder suportar mais de um pássaro dentro do jogo
        passaro.desenhar(tela)
    for cano in canos:                   # Pode haver mais de um cano na tela
        cano.desenhar(tela)
    
    texto = FONTE_PONTOS.render(f'Pontuação: {pontos}', 1, (255,255,255))   # Criação do texto. Ultiliza do 'f' antes da string para criar uma fstring e adicionar variáveis dentro dela. O 1 para deixar o texto formatado e redondinho e por ultimo a cor representada por valores em RGB,sendo ali, branco
    tela.blit(texto, ((TELA_LARGURA - 10 - texto.get_width()), 10 ))        # Poder desenhar o texto na tela.
    chao.desenhar(tela)
    pygame.display.update()     # Poder fazer a atualização da tela


def main():    # Função principal do jogo, em que será definida onde ficarão todos os elementos do jogo e o relógio para conferir o tempo do jogo
    passaros = [Passaro(230, 350)]                
    chao     = Chao(730)
    canos    = [Cano(700)]
    tela     = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos   = 0
    relogio  = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)   # Quantos de fps o jogo estara rodando, taxa de atualizações por segundo
        # Parte de interação com o usuário:
        for evento in pygame.event.get():       # Para cada evento da lista de eventos que ocorrem no computador enquanto seu jogo está rodando
            if evento.type == pygame.QUIT:      # Se o usuário clicar para sair do jogo
                rodando = False     
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # [MODIFICAÇÃO] Saber se o Usuário apertou Esc para sair do jogo 
                    rodando = False
                    pygame.quit() 
                    quit()
            if evento.type == pygame.KEYDOWN:      # Se o usuário aperta Space para poder fazer o pássaro pular
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
        
        # Movimetação dos elementos:
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos  = []
        for cano in canos:
            for i, passaro in enumerate(passaros):  # Se houve uma colisão, esse passaro sairá da tela
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x: # Se a variável cano.passou é falsa e o X do pássaro é maior que o X do cano, então cano.passou vira verdadeiro e adiconar_cano também, adiconando outro cano na tela
                    cano.passou = True
                    adicionar_cano = True

            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)
        
        if adicionar_cano:   # Se verdadeiro, aumenta a pontuação e adiona outro cano
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:   # Remove o cano que ja passou
            canos.remove(cano)
 
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:  # Choque com o chão ou o pássaro voou para fora da tela
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)


if __name__ == '__main__':   # Se o arquivo for executado manualmente, ele irá rodar automáticamente. 
    main()                          
    
        



