
import pygame
import random


#game settings
GAME_SIZE = 400
BLOCK_SIZE = GAME_SIZE / 40
SNEK_COLOR = (0, 255, 0,)
APPLE_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
GAME_FPS = 20

pygame.init()
clock = pygame.time.Clock()
game_display = pygame.display.set_mode((GAME_SIZE, GAME_SIZE))
score_font = pygame.font.SysFont('Comic Sans', int(GAME_SIZE * .065), True)
title_font = pygame.font.SysFont('Comic Sans', int(GAME_SIZE * .2), True)
pygame.display.set_caption('SNEK')


class Game_Object():
    def __init__(self, xcor, ycor, color):
        self.xcor = xcor
        self.ycor = ycor
        self.color = color
    def show_as_circle(self):
        pygame.draw.circle(game_display, self.color, (int(self.xcor + BLOCK_SIZE / 2), int(self.ycor + BLOCK_SIZE / 2)), int(BLOCK_SIZE / 2))
    def show_as_square(self):
        pygame.draw.rect(game_display, self.color, pygame.Rect(self.xcor, self.ycor, BLOCK_SIZE, BLOCK_SIZE))

class snek():
    def __init__(self, xcor, ycor):
        self.is_alive = True
        self.score = 0
        self.direction = "RIGHT"
        self.body = [Game_Object(xcor, ycor, SNEK_COLOR),
                    Game_Object(xcor - BLOCK_SIZE, ycor, SNEK_COLOR),
                    Game_Object(xcor - BLOCK_SIZE * 2, ycor, SNEK_COLOR)]
        self.previous_last_tail = self.body[len(self.body) - 1]
    def grow(self):
        self.body.append(self.previous_last_tail)

    def show(self):
        for body_part in self.body:
            body_part.show_as_square()
    def set_direction_right(self):
        if self.direction != "LEFT":
            self.direction = "RIGHT"
    def set_direction_left(self):
        if self.direction != "RIGHT":
            self.direction = "LEFT"
    def set_direction_up(self):
        if self.direction != "DOWN":
            self.direction = "UP"
    def set_direction_down(self):
        if self.direction != "UP":
            self.direction = "DOWN"
    def move(self):
        head_xcor = self.body[0].xcor
        head_ycor = self.body [0].ycor
        if self.direction == "RIGHT":
            head_xcor = head_xcor + BLOCK_SIZE
        elif self.direction == "LEFT":
            head_xcor = head_xcor - BLOCK_SIZE
        elif self.direction == "UP":
            head_ycor = head_ycor - BLOCK_SIZE
        elif self.direction == "DOWN":
            head_ycor = head_ycor + BLOCK_SIZE


        self.body.insert(0, Game_Object(head_xcor, head_ycor, SNEK_COLOR))
        self.previous_last_tail = self.body.pop()
    def has_collided_with_wall(self):
        head = self.body[0]
        if head.xcor < 0 or head.ycor < 0 or head.xcor + BLOCK_SIZE > GAME_SIZE or head.ycor + BLOCK_SIZE > GAME_SIZE:
            return True
        return False
    def has_eaten_apple(self, apple_in_question):
        head = self.body[0]
        if head.xcor == apple_in_question.body.xcor and head.ycor == apple_in_question.body.ycor:
            return True
        return False
    def has_collided_with_itself(self):
        head = self.body[0]
        for i in range(1, len(self.body)):
            if head.xcor == self.body[i].xcor and head.ycor == self.body[i].ycor:
                return True
        return False
        
class Apple():
    def __init__(self, snek_Segment):
        self.body = self.get_RNG_generated_game_object()
        while self.apple_is_on_snek(snek_Segment):
            self.body = self.get_RNG_generated_game_object()

    def get_RNG_generated_game_object(self):
        xcor = random.randrange(0, GAME_SIZE / BLOCK_SIZE) * BLOCK_SIZE
        ycor = random.randrange(0, GAME_SIZE / BLOCK_SIZE) * BLOCK_SIZE
        return Game_Object(xcor, ycor, APPLE_COLOR)

    def apple_is_on_snek(self, snek_Segment):
        for snek_part in snek_Segment:
            if snek_part.xcor == self.body.xcor and snek_part.ycor == self.body.ycor:
                return True             
    def show(self):
        self.body.show_as_circle()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            snek.is_alive = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snek.set_direction_left()
            elif event.key == pygame.K_RIGHT:
                snek.set_direction_right()
            elif event.key == pygame.K_UP:
                snek.set_direction_up()
            elif event.key == pygame.K_DOWN:
                snek.set_direction_down()
            elif event.key == pygame.K_p:
                pause_game()             

def pause_game():
    game_is_paused = True
    while game_is_paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snek.is_alive = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_is_paused = False
            pygame.display.update()
            clock.tick(5)

snek = snek(BLOCK_SIZE * 5, BLOCK_SIZE * 5)
apple = Apple(snek.body)

# Title Screen
show_title_screen = True
while show_title_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            snek.is_alive = False
            show_title_screen = False
        if event.type == pygame.KEYDOWN:
            show_title_screen = False

    title_text = title_font.render('SNEK', False, SNEK_COLOR)
    game_display.blit(title_text, (GAME_SIZE / 2 - title_text.get_width() / 2, 50))
    pygame.display.flip()
    clock.tick(GAME_FPS)
    

# Main Game Loop
while snek.is_alive:

    handle_events()

    game_display.blit(game_display, (0, 0))

    snek.move()
    if snek.has_collided_with_wall() or snek.has_collided_with_itself():
        snek.is_alive = False
    if snek.has_eaten_apple(apple):
        snek.grow()
        snek.score += 1
        apple = Apple(snek.body)

    game_display.fill(BACKGROUND_COLOR)
    snek.show()
    apple.show()

    score_text = score_font.render(str(snek.score), False, (255, 255, 255))
    game_display.blit(score_text, (0, 0))
    pygame.display.set_caption('SNEK | Score = ' + str(snek.score) + ' | Press P to pause')

    pygame.display.flip()

    if snek.is_alive == False:
        clock.tick(.7)
    
    clock.tick(GAME_FPS)


pygame.display.quit()
pygame.quit()