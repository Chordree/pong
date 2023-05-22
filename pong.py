import pygame
import random  # random was only use here to vary collision effect

pygame.init()
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT ))
pygame.display.set_caption('pong')
FPS = 60  # Frames per Seconds 
WHITE = 255, 255, 255
BLACK = (0, 0, 0)
paddle_width, paddle_height = 20, 100
ball_radius = 8
text_font = pygame.font.SysFont('comicsans', 50)
playername_font = pygame.font.SysFont('comicsans', 30) #use any font of your choice , got this from Tim
player1_name = input('player1 enter your name:')
player2_name = input('player2 enter your name:')

winning_score = 10

class Paddle():
    colour = WHITE
    dist = 4
    def __init__(self, x, y, width, height):
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.width = width
        self.height = height
    def draw(self, wn):
        pygame.draw.rect(wn, self.colour, (self.x, self.y, self.width, self.height))    
        #  check the importance of this first wn...added to this fuction 
    def move(self, up = True):
        if up:
            self.y -= self.dist
        else:
            self.y += self.dist       

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y      


class Ball():
    max_vel = 5
    colour = WHITE
    
    def __init__(self, x, y, rad):
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.radius = rad
        self.x_vel = self.max_vel
        self.y_vel = 0

    def draw(self, wn):
        pygame.draw.circle(wn, self.colour, (self.x, self.y), self.radius)    

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel    

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.y_vel = 0
        self.x_vel *= 1  #see to change this to 1 latter on .i.e losser serves
        # you can change this to -1 ..i.e winners serves depending on your specifications/ choice 



def draw(win, paddles, ball, l_score, r_score, nam1, nam2):
    win.fill(BLACK)

    l_score = text_font.render(f'{l_score}', 1, WHITE)
    r_score = text_font.render(f'{r_score}', 1, WHITE)
    nam1 = playername_font.render(f'{nam1}', 1, WHITE)
    nam2 = playername_font.render(nam2, 1, WHITE)
    win.blit(l_score, (WIDTH/4, 20))
    win.blit(r_score, (WIDTH * (3/4), 20))
    win.blit(nam1, (WIDTH * (1/4), 1))  # use .get len of names to centralise the name under the scores 
    win.blit(nam2, (WIDTH * (3/4), 1))

    for paddl in paddles:
        paddl.draw(win)
    # ball.draw(win) #  this should be removed later on ..just see the diff when it is drawn here and below
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 0:
            pygame.draw.rect(win, WHITE, (WIDTH/2 - 5, i, 10, HEIGHT/20))
    ball.draw(win)
    pygame.display.update()


def handle_pdlmovement(keys, left_pdl, right_pdl):
    if keys[pygame.K_w] and left_pdl.y >= 0:
        left_pdl.move(up= True)
    if keys[pygame.K_s] and left_pdl.y <= HEIGHT - paddle_height:
        left_pdl.move(up= False) 
    if keys[pygame.K_UP] and right_pdl.y >=0:
        right_pdl.move(up= True) 
    if keys[pygame.K_DOWN] and right_pdl.y <= HEIGHT - paddle_height:
        right_pdl.move(up= False)       

def handle_collision(bal, left_pdl, right_pdl):
    if bal.y + bal.radius >= HEIGHT:
        bal.y_vel *= -1
    elif bal.y - bal.radius <= 0:
        bal.y_vel *= -1 
    if bal.x_vel <= 0:
        if left_pdl.y <= bal.y <= left_pdl.y + left_pdl.height:
            if bal.x - bal.radius <= left_pdl.x + left_pdl.width:
                bal.x_vel *= -1
                middle_y1 = (left_pdl.y + left_pdl.height) / 2 
                middle_y2 = left_pdl.y + left_pdl.height / 2
                middle_y = random.choice((middle_y1, middle_y2))
                 # try switching middle y var based on random .choice.. so the collision effect is more dynamic  
                diff_in_y = middle_y - bal.y 
                reduction_factor = (left_pdl.height / 2) / bal.max_vel
                y_vel = diff_in_y / reduction_factor
                bal.y_vel = -1 * y_vel
    else:
        if  right_pdl.y <= bal.y <= right_pdl.y + right_pdl.height:
            if bal.x + bal.radius >= right_pdl.x:
                bal.x_vel *= -1
                middle_y1 = (right_pdl.y + right_pdl.height) / 2
                middle_y2 = right_pdl.y + right_pdl.height / 2
                middle_y = random.choice((middle_y1, middle_y2))
                diff_in_y = middle_y - bal.y 
                reduction_factor = (right_pdl.height / 2) / bal.max_vel
                y_vel = diff_in_y / reduction_factor
                bal.y_vel = -1 * y_vel    # see to this and understand the collision principle 
                # check importance of changing the velocity to negative ..introduce random 



def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT/2 - paddle_height/2, paddle_width, paddle_height)
    right_paddle = Paddle(WIDTH - 10 - paddle_width, HEIGHT/2 - paddle_height/2, paddle_width, paddle_height)
    ball = Ball(WIDTH/2, HEIGHT/2, ball_radius)
    left_score, right_score = 0, 0
    name1, name2 = player1_name, player2_name 

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score, name1, name2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_pdlmovement(keys, left_paddle, right_paddle,)
        # handle_collision(ball, left_paddle, right_paddle)  # see if to move this after ball movement 
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        if left_score >= 10 or right_score >=10 :
            # add a statement to display winner 
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            pygame.time.delay(4500) # note time is in milli-seconds 
            left_score = 0
            right_score = 0

    pygame.quit()



main()    
