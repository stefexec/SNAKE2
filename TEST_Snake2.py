import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
SNAKE_SIZE = 20
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BG_COLOR = (0, 0, 0)
SPEED = 5
SHREK_SPEED = 1

# Load the Shrek image
shrek_image = pygame.image.load('shrek.png')
shrek_rect = shrek_image.get_rect()
shrek_rect.right = WIDTH  # start from the right side of the screen

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the snake and food
snake = [pygame.Rect(WIDTH / 2, HEIGHT / 2, SNAKE_SIZE, SNAKE_SIZE)]
food = pygame.Rect(random.randint(0, WIDTH - SNAKE_SIZE), random.randint(0, HEIGHT - SNAKE_SIZE), SNAKE_SIZE, SNAKE_SIZE)

def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, segment)

def draw_food():
    pygame.draw.rect(screen, FOOD_COLOR, food)

def main():
    clock = pygame.time.Clock()
    dx, dy = 0, 0  # the direction of the snake
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dx, dy = 0, -SPEED
                elif event.key == pygame.K_DOWN:
                    dx, dy = 0, SPEED
                elif event.key == pygame.K_LEFT:
                    dx, dy = -SPEED, 0
                elif event.key == pygame.K_RIGHT:
                    dx, dy = SPEED, 0

        # Move the snake
        head = snake[0].copy()
        head.move_ip(dx, dy)
        snake.insert(0, head)

        # Check if snake has hit Shrek
        if snake[0].colliderect(shrek_rect):
            print("Game Over")
            pygame.quit()
            sys.exit()

        # Check if snake has eaten the food
        if snake[0].colliderect(food):
            # Spawn new food
            food.x = random.randint(0, WIDTH - SNAKE_SIZE)
            food.y = random.randint(0, HEIGHT - SNAKE_SIZE)
        else:
            # If no food eaten, remove the tail of the snake
            snake.pop()

        # Move Shrek to the left
        shrek_rect.move_ip(-SHREK_SPEED, 0)

        # Clear the screen and draw everything
        screen.fill(BG_COLOR)
        draw_snake()
        draw_food()
        screen.blit(shrek_image, shrek_rect.topleft)
        pygame.display.flip()

        # Limit the game to 60 frames per second
        clock.tick(60)

if __name__ == "__main__":
    main()
