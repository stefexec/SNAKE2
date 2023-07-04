import pygame
import time
import random

# set up some constants
WIDTH = 1920
HEIGHT = 1080
SNAKE_SIZE = 20
SNAKE_SPEED = 10  # Lower this number to make the snake move slower

# define the snake and food classes
class Snake:
    def __init__(self):
        self.size = SNAKE_SIZE
        self.color = pygame.Color("Green")
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = "RIGHT"

    def move(self):
        head = self.body[0]
        if self.direction == "UP":
            new_head = (head[0], head[1] - self.size)
        elif self.direction == "DOWN":
            new_head = (head[0], head[1] + self.size)
        elif self.direction == "LEFT":
            new_head = (head[0] - self.size, head[1])
        else:
            new_head = (head[0] + self.size, head[1])

        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        # Add two new parts to the body instead of one for a bigger grow
        self.body.append(self.body[-1])
        self.body.append(self.body[-1])

class Food:
    def __init__(self):
        self.size = SNAKE_SIZE
        self.color = pygame.Color("Red")
        self.position = (random.randint(0, WIDTH - self.size), random.randint(0, HEIGHT - self.size))

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    snake = Snake()
    food = Food()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN:
                    snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT:
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    snake.direction = "RIGHT"

        snake.move()

        if snake.body[0] == food.position:
            snake.grow()
            food = Food()

        if snake.body[0] in snake.body[1:] or snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT:
            running = False

        screen.fill(pygame.Color("Black"))
        for part in snake.body:
            pygame.draw.rect(screen, snake.color, pygame.Rect(part[0], part[1], snake.size, snake.size))
        pygame.draw.rect(screen, food.color, pygame.Rect(food.position[0], food.position[1], food.size, food.size))
        pygame.display.flip()

        clock.tick(SNAKE_SPEED)

    pygame.quit()

if __name__ == "__main__":
    main()
