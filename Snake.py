
import pygame
import random


#game settings
GAME_SIZE = 400
BLOCK_SIZE = GAME_SIZE / 40
GAP_SIZE = GAME_SIZE * 0.002
APPLE_COLOR = (255, 25, 55)
BACKGROUND_COLOR = (0, 0, 0)
YELLOW = (255, 255, 0)
LIME_GREEN = (0, 255, 0)
FOREST_GREEN = (0, 150, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GAME_FPS = 40

pygame.init()
clock = pygame.time.Clock()
game_display = pygame.display.set_mode((GAME_SIZE, GAME_SIZE))
score_font = pygame.font.SysFont('Comic Sans', int(GAME_SIZE * .065), True)
title_font = pygame.font.SysFont('Comic Sans', int(GAME_SIZE * .2), True)
title_press_start_font = pygame.font.SysFont('Comic Sans', int(GAME_SIZE * 0.1), True)
title_copyright_font = pygame.font.SysFont('Comic Sans', int(GAME_SIZE * 0.05), True)
pygame.display.set_caption(' SNEK ')

class Color_Cycler():
    def __init__(self, * colors):
        self.colors = []
        for color in colors:
            self.colors.append(color)
        self.cycle_count = 1
        self.color_change_frequency = 6
    def get_next_color(self):
        if self.cycle_count >= self.color_change_frequency:
            self.cycle_count = 1
        else:
            self.cycle_count += 1

        if self.cycle_count == self.color_change_frequency:
            next_color = self.colors.pop()
            self.colors.insert(0, next_color)
            return next_color
        else:
            return self.colors[0]



class Game_Object():
    def __init__(self, xcor, ycor, color):
        self.xcor = xcor
        self.ycor = ycor
        self.color = color
    def show_as_circle(self):
        pygame.draw.circle(game_display, self.color, (int(self.xcor + BLOCK_SIZE / 2), int(self.ycor + BLOCK_SIZE / 2)), int(BLOCK_SIZE / 2))
    def show_as_square(self):
        pygame.draw.rect(game_display, self.color, pygame.Rect(self.xcor + GAP_SIZE, self.ycor + GAP_SIZE, BLOCK_SIZE - GAP_SIZE * 2, BLOCK_SIZE - GAP_SIZE * 2))

class Snek():
    def __init__(self, xcor, ycor):
        self.is_alive = True
        self.score = 0
        self.direction = "RIGHT"
        self.body = [Game_Object(xcor, ycor, LIME_GREEN),
                    Game_Object(xcor - BLOCK_SIZE, ycor, BLUE),
                    Game_Object(xcor - BLOCK_SIZE * 2, ycor, LIME_GREEN)]
        self.previous_last_tail = self.body[len(self.body) - 1]
        self.color_counter = 0
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
    def move(self, color_cycler):
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


        self.body.insert(0, Game_Object(head_xcor, head_ycor, color_cycler.get_next_color()))
        self.previous_last_tail = self.body.pop()
    def refresh_RGB_cycled_colors(self, color_cycler):
        for i in range(len(self.body) -1, 0, -1):
            self.body[i].color = self.body[i-1].color
        self.body[0].color = color_cycler.get_next_color()
        
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

color_cycler = Color_Cycler(BLUE, LIME_GREEN, FOREST_GREEN, YELLOW, CYAN)
snek = Snek(BLOCK_SIZE * 5, BLOCK_SIZE * 5)
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

    title_text = title_font.render('| SNEK |', False, LIME_GREEN)
    title_press_start_text = title_press_start_font.render('PRESS TO START', False, CYAN)
    title_copyright_text = title_copyright_font.render('©2019 JOHN WILLIAM JONES III | TRUECODERS', False, BLUE)
    game_display.blit(title_text, (GAME_SIZE / 2 - title_text.get_width() / 2, 50))
    game_display.blit(title_press_start_text, (GAME_SIZE / 4 - title_press_start_text.get_width() / 10, 150))
    game_display.blit(title_copyright_text, (GAME_SIZE / 5 - title_copyright_text.get_width() / 7, 350))
    pygame.display.flip()
    clock.tick(GAME_FPS)
    

# Main Game Loop
FRAME_COUNTER = 0
while snek.is_alive:

    handle_events()

    game_display.blit(game_display, (0, 0))

    if FRAME_COUNTER % 2 == 0:
        snek.move(color_cycler)
        if snek.has_collided_with_wall() or snek.has_collided_with_itself():
            snek.is_alive = False
        if snek.has_eaten_apple(apple):
            snek.grow()
            snek.score += 1
            apple = Apple(snek.body)

    game_display.fill(BACKGROUND_COLOR)
    snek.show()
    apple.show()
    FRAME_COUNTER += 1
    snek.refresh_RGB_cycled_colors(color_cycler)

    score_text = score_font.render(str(snek.score), False, (255, 255, 255))
    game_display.blit(score_text, (0, 0))
    pygame.display.set_caption('SNEK | Score = ' + str(snek.score) + ' | Press P to pause')

    pygame.display.flip()

    if snek.is_alive == False:
        clock.tick(.7)
    
    clock.tick(GAME_FPS)


pygame.display.quit()
pygame.quit()