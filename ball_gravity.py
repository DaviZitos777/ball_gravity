import pygame
import typing
import random
# Iniciar pygame
pygame.init()
# janela
janela_x = 1200
janela_y = 800
janela = pygame.display.set_mode((janela_x, janela_y))
running = True
dt = 0
clock = pygame.time.Clock()

# Bola

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Vetor que armazenará as cores aleatorias
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

class Bola:
    def __init__(self, x, y, acX = 0, acY = 0):
        self.pos_x = x
        self.pos_y = y
        self.raio = 20
        
        # Força da gravidade
        self.gravity = random.randint(1000, 2000)
        # Aceleração
        self.speed_y = acY
        self.speed_x = acX
        # Coeficiente de elasticidade (1 a bola volta com toda a força, 0 a bola não volta, 0.5 a bola volta com metade da força e etc...)
        self.bounce_coefficient = random.randint(4, 9) / 10
        # Resistencia do ar para a bola parar de se mover horizontalmente alguma hora
        self.air_resistance = random.randint(50, 100)
        # Cor aleatoria
        self.color = colors[random.randint(0, len(colors) - 1)]
    def fisica(self):
        # X
        # A resistencia o ar aumenta a velocidade para esquerda até chegar em zero se estiver se acelerando para direita
        if self.speed_x > 0:
            self.speed_x -= self.air_resistance * dt
        # A resistencia o ar aumenta a velocidade para direita até chegar em zero se estiver se acelerando para esquerda
        elif self.speed_x < 0:
            self.speed_x += self.air_resistance * dt
        # A resistencia para de agir quando a velocidade é zero ou proximo disso
        else:
            self.speed_x = 0
        # Aplica a aceleração(com resistencia) a posição
        self.pos_x += self.speed_x * dt
        
        # Se bater na lateral direita reflete a aceleração + absorção de força pela a parede
        if self.pos_x > (janela_x - self.raio):
            self.pos_x = (janela_x - self.raio)
            self.speed_x = -self.speed_x * self.bounce_coefficient
        # Se bater na lateral esquerda reflete a aceleração + absorção de força pela a parede
        if self.pos_x < (0 + self.raio):
            self.pos_x = (0 + self.raio)
            self.speed_x = -self.speed_x * self.bounce_coefficient
        # Y
        # Gravidade puxa a bola SEMPRE para baixo indenpendente de se mover para cima ou baixo sempre estará tornando a velocidade negativa
        self.speed_y += self.gravity * dt
        # Aplica a aceleração com gravidade a posição
        self.pos_y += self.speed_y * dt
        # Se a bola bater no chão reflete a velocidade da bola invertendo a força + coeficiente de elasticidade
        # Obs: gravidade continua puxando tornando a força para cima cada vez menor
        # até continuar ai pro chão denovo
        if self.pos_y > (janela_y - self.raio):
            self.pos_y = (janela_y - self.raio)
            self.speed_y = -self.speed_y * self.bounce_coefficient
        # Se a bola bater no teto reflete a velocidade da bola invertendo a força + coeficiente de elasticidade
        if self.pos_y < (0 + self.raio):
            self.pos_y = (0 + self.raio)
            self.speed_y = -self.speed_y * self.bounce_coefficient
    # Metodo para desenhar a bola
    def draw(self):
        pygame.draw.circle(janela, self.color, (self.pos_x, self.pos_y), self.raio)
# Lista de bolas
bolas: typing.List[Bola] = []

# Botão

Botão_largura = 65
Botão_altura = 20
Botão_fonte = pygame.font.SysFont("arial", 15, True)

class Botão:
    def __init__(self, x, y, str, func = -1):
        global Botão_largura, Botão_altura
        self.rect = pygame.Rect(x, y, Botão_largura, Botão_altura)
        self.content = str
        self.func = func
    def logic(self, event_list: typing.List[pygame.event.Event]):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if callable(self.func):
                        self.func()
    def draw(self):
        pygame.draw.rect(janela, branco, self.rect)
        janela.blit(Botão_fonte.render(self.content, False, preto), (self.rect.x, self.rect.y))
def limpar_bolas():
    global bolas
    bolas.clear()

botao_reiniciar = Botão(10, 10, "Reiniciar", limpar_bolas)

while running:
    # Delta time (não pode ser muito alto porque se o FPS cair demais a fisica pode ser interrompida por causa de valores decimais minusculos
    # sendo multiplicados por valores decimais gigantescos)
    dt = min(clock.tick(60) / 1000, 1 / 30)
    event_list: typing.List[pygame.event.Event] = []
    # Gerenciador de eventos
    for event in pygame.event.get():
        event_list.append(event)
        # Detecta saída
        if event.type == pygame.QUIT:
            running = False
        # Espalha bolas ao clicar
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not botao_reiniciar.rect.collidepoint(pygame.mouse.get_pos()):
                bolas.append(Bola(list(pygame.mouse.get_pos())[0], list(pygame.mouse.get_pos())[1], 0, 0))
    # Aplica fisica a todas as bolas
    for bola in bolas:
        bola.fisica()
    # Lógica do botão
    botao_reiniciar.logic(event_list)
    # Renderização:
    
    # Preenche a tela com preto
    janela.fill((0, 0, 0))
    # Desenha todas as bolas
    for bola in bolas:
        bola.draw()
    # Desenhar o botão
    botao_reiniciar.draw()
    
    # Desenhar texto
    janela.blit(Botão_fonte.render(f"Quantidade de bolas: {len(bolas)}", False, branco), (10, 40))
    
    # Renderizar o frame
    pygame.display.flip()
    # Limpar a lista de eventos
    event_list.clear()