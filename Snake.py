#KJHLKJHKLJKLH
import pygame

BLOCK_SIZE = 20
SNEK_COLOR = (0, 255, 0,)
APPLE_COLOR = (255, 0, 0)

pygame.init()
clock = pygame.time.Clock()
game_display = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('SNEK')


class Snek():
    def __init__(self, xcor, ycor):       
        self.if_alive = True
        self.direction = "RIGHT"
        self.snek = [(xcor, ycor),
                    (xcor - BLOCK_SIZE, ycor),
                    (xcor - BLOCK_SIZE * 2, ycor)]
    def show(self):
        for snek_Segment in self.snek:
            pygame.draw.rect(game_display, SNEK_COLOR, pygame.Rect(snek_Segment[0], snek_Segment[1], BLOCK_SIZE, BLOCK_SIZE))
    def move(self):
        head_xcor = self.snek[0][0]
        head_ycor = self.snek[0][1]
        if self.direction == "RIGHT":
            new_xcor = head_xcor + BLOCK_SIZE
            self.snek.insert(0, (new_xcor, head_ycor))
        elif self.direction == "LEFT":
            new_xcor = head_xcor - BLOCK_SIZE
            self.snek.insert(0, (new_xcor, head_ycor))
        elif self.direction == "UP":
            new_ycor = head_ycor - BLOCK_SIZE
            self.snek.insert(0, (head_xcor, new_ycor))
        elif self.direction == "DOWN":
            new_ycor = head_ycor + BLOCK_SIZE
            self.snek.insert(0, (head_xcor, new_ycor))

        self.snek.pop()

class Apple():
    def __init__(self):
        self.xcor = 30
        self.ycor = 80
    def show(self):
        pygame.draw.rect(game_display, APPLE_COLOR, pygame.Rect(self.xcor, self.ycor, BLOCK_SIZE, BLOCK_SIZE))

snek = Snek(145, 200)
apple = Apple()

#Main Game Loop
while snek.if_alive:

    for event in pygame.event.get():       
        if event.type == pygame.QUIT:
            snek.if_alive = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snek.direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                snek.direction = "RIGHT"
            elif event.key == pygame.K_UP:
                snek.direction = "UP"
            elif event.key == pygame.K_DOWN:
                snek.direction = "DOWN"
            
    game_display.blit(game_display, (0, 0))

    snek.move()

    game_display.fill((0, 0, 0))
    snek.show()
    apple.show()

    pygame.display.flip()

    clock.tick(15)

pygame.quit()