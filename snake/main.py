import pygame
from pygame.locals import *
import os
import time
import random

SIZE = 40

class Snake():
    def __init__(self, parent_screen, length) -> None:
        current_path = os.path.dirname(__file__) # Where your .py file is located
        resource_path = os.path.join(current_path, 'resources') # The resource folder path
        image_path = os.path.join(resource_path, 'images') # The image folder path
        
        self.parent_screen = parent_screen
        self.block = pygame.image.load(os.path.join(image_path, 'block.jpg')).convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'
        self.length = length

    def draw(self):
        self.parent_screen.fill((186, 255, 180))
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length +=1
        self.x.append(SIZE)
        self.y.append(SIZE)

    def move_left(self):
        self.direction = 'left'
    
    def move_right(self):
        self.direction = 'right'
    
    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]
        
        if self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'left':
            self.x[0] -= SIZE
        
        self.draw()
        


class Apple:

    def __init__(self, parent_screen) -> None:
        current_path = os.path.dirname(__file__) # Where your .py file is located
        resource_path = os.path.join(current_path, 'resources') # The resource folder path
        image_path = os.path.join(resource_path, 'images') # The image folder path

        self.apple = pygame.image.load(os.path.join(image_path, 'apple.jpg')).convert()
        self.parent_screen = parent_screen
        self.x =    120
        self.y =    120

    def draw(self):
        self.parent_screen.blit(self.apple,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,24)*SIZE
        self.y = random.randint(0,19)*SIZE
    
    
class Game():

    def __init__(self) -> None:
        pygame.init()

        pygame.mixer.init()
        
        self.surface = pygame.display.set_mode((1000,800))
        self.play_bg_music()
        self.surface.fill((186, 255, 180))
        self.snake = Snake(self.surface,5)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play(self):

        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        current_path = os.path.dirname(__file__) # Where your .py file is located
        resource_path = os.path.join(current_path, 'resources') # The resource folder path
        sound_path = os.path.join(resource_path, 'music') # The sound folder path

        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            
            self.snake.increase_length()
            self.apple.move()

            
            sound = pygame.mixer.Sound(os.path.join(sound_path, '1_snake_game_resources_ding.mp3'))
            pygame.mixer.Sound.play(sound)
        

        if self.wall_collision(self.snake.x[0],self.snake.y[0]):
            sound = pygame.mixer.Sound(os.path.join(sound_path, '1_snake_game_resources_crash.mp3'))
            pygame.mixer.Sound.play(sound)
            raise "Game Over"
            

        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                sound = pygame.mixer.Sound(os.path.join(sound_path, '1_snake_game_resources_crash.mp3'))
                pygame.mixer.Sound.play(sound)
                raise "Game Over"


    def play_bg_music(self):
        current_path = os.path.dirname(__file__) # Where your .py file is located
        resource_path = os.path.join(current_path, 'resources') # The resource folder path
        sound_path = os.path.join(resource_path, 'music') # The sound folder path

        pygame.mixer.music.load(os.path.join(sound_path, 'bg_music_1.mp3'))
        pygame.mixer.music.play()

    def is_collision(self,x1,y1,x2,y2):
        if x1 < x2 +SIZE and x1 >= x2:
            if y1 < y2 +SIZE and y1 >= y2:
                return True
        return False

    def wall_collision(self,x1,y1):
        if x1>=0 and x1<1000:
            if y1>=0 and y1<800:
                return False
        
        return True


    def display_score(self):
        font = pygame.font.SysFont("arial",30)
        score = font.render(f"score: {self.snake.length - 5}", True, (0,200,200))
        self.surface.blit(score , (800,10))

    def show_game_over(self):
        self.surface.fill((186, 255, 180))
        font = pygame.font.SysFont("arial",30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length -5}", True, (0,255,255))
        self.surface.blit(line1,(200,300))
        line2 = font.render(f"To play again, press enter, to exit press cross on top right corner.", True, (0,255,255))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface,5)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause= False

        while running:
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running == False
                        break
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                    
                elif event.type == pygame.QUIT:
                    running == False
                    exit(0)
                        
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.3)


    


if __name__ == "__main__":
    
    game = Game()
    game.run()
  


