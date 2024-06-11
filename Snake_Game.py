import pygame
import sys
import random

#Initialize Pygame
pygame.init()

#Create game screen
width, height = 800, 800
block_size = 50
FONT = pygame.font.Font(None, block_size*2)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('The Snake Game')
clock = pygame.time.Clock()

#Create players snake
class Snake:
    def __init__(self):
        self.x, self.y = block_size, block_size
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, block_size, block_size)
        self.body = [pygame.Rect(self.x-block_size, self.y, block_size, block_size)]
        self.dead = False
    
    def update(self):
        global apple
        #If snake runs into border or self, it's game over
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, width) or self.head.y not in range(0, height):
                self.dead = True
        if self.dead:
            self.x, self.y = block_size, block_size
            self.xdir = 1
            self.ydir = 0
            self.head = pygame.Rect(self.x, self.y, block_size, block_size)
            self.body = [pygame.Rect(self.x-block_size, self.y, block_size, block_size)]
            self.dead = False
            apple = Apple()

        #Add movement logic to snake
        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.xdir * block_size
        self.head.y += self.ydir * block_size
        self.body.remove(self.head)

#Create Apple for snake to eat and grow
class Apple:
    def __init__(self):
        self.x = int(random.randint(0, width)/ block_size) * block_size
        self.y = int(random.randint(0, height)/ block_size) * block_size
        self.rect = pygame.Rect(self.x, self.y, block_size, block_size)

    def update(self):
        pygame.draw.rect(screen, 'red', self.rect)

#Create score and add position on screen
score = FONT.render('1', True, 'white')
score_rect = score.get_rect(center = (width/2, block_size))

snake = Snake()

apple = Apple()

#Make display remain open until exited
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #Create snake controls
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if snake.ydir != -1:
                        snake.ydir = 1
                    snake.xdir = 0
                elif event.key == pygame.K_UP:
                    if snake.ydir != 1:
                        snake.ydir = -1
                    snake.xdir = 0
                elif event.key == pygame.K_RIGHT:
                    if snake.xdir != -1:
                        snake.xdir = 1
                    snake.ydir = 0
                    
                elif event.key == pygame.K_LEFT:
                    if snake.xdir != 1:
                        snake.xdir = -1
                    snake.ydir = 0

    snake.update()
    screen.fill('black')
    apple.update()

    #Reflect the actual score count
    score = FONT.render(f'{len(snake.body)-1}', True, 'white')

    #Add snake to game
    pygame.draw.rect(screen, 'green', snake.head)
    for square in snake.body:
        pygame.draw.rect(screen, 'green', square)

    #Insert score count to screen
    screen.blit(score, score_rect)

    #Implement eating mechanism
    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.body.append(pygame.Rect(square.x, square.y, block_size, block_size))
        apple = Apple()

    pygame.display.update()
    clock.tick(10)

