import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake RPG Game")

# Define colors
bg_color = (0, 0, 0)
snake_color = (0, 255, 0)
food_color = (255, 0, 0)

# Load Guy Fieri image for the snake
snake_img = pygame.image.load("guy_fieri.png")
snake_img = pygame.transform.scale(snake_img, (80, 80))  # Increase size to 80x80 pixels

# Define snake properties
snake_size = 80  # Increase size to match the image dimensions
snake_speed = 10
snake_level = 1
snake_xp = 0
xp_needed = 10

# Define initial position of snake
snake_x = (screen_width // 2) - (snake_size // 2)
snake_y = (screen_height // 2) - (snake_size // 2)
snake_dx = 0
snake_dy = 0

# Define food properties
food_size = 20
food_x = random.randint(0, screen_width - food_size) // food_size * food_size
food_y = random.randint(0, screen_height - food_size) // food_size * food_size
food_dx = snake_speed
food_dy = snake_speed

# Define clock to control game speed
clock = pygame.time.Clock()

# Initialize score
score = 0
font = pygame.font.Font(None, 36)

# Load game over sound
game_over_sound = pygame.mixer.Sound("Snake Snake Snake.wav")

# Load level up sound
level_up_sound = pygame.mixer.Sound("Minecraft Level Up.mp3")

# Define microtransaction items and their prices
items = {
    "Super Speed": 5,
    "Extra XP": 10,
    "Mega Growth": 8,
    "Bonus Life": 15,
    "Glob": 20
}

# MP3 files for microtransaction
microtransaction_files = [
    "Buying Bonus Life.mp3",
    "Buying Extra XP.mp3",
    "Buying Mega Growth.mp3",
    "Buying Super Speed.mp3",
    "glob.mp3"
]

# Function to play a random microtransaction sound
def play_random_microtransaction_sound():
    sound_file = random.choice(microtransaction_files)
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

# Function to show microtransaction window
def show_microtransaction_window():
    pygame.draw.rect(screen, (128, 128, 128), (200, 200, 600, 400))
    pygame.draw.rect(screen, (0, 0, 0), (220, 220, 560, 360))
    title_text = font.render("Microtransactions", True, (255, 255, 255))
    screen.blit(title_text, (300, 220))
    y = 270
    for item, price in items.items():
        item_text = font.render(f"{item} - Price: ${price}", True, (255, 255, 255))
        screen.blit(item_text, (250, y))
        y += 40
    pygame.display.flip()

# Game loop
game_over = False
microtransaction_window = False
snake_segments = []  # List to store the snake's body segments
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if microtransaction_window:
                    microtransaction_window = False
                    screen.fill(bg_color)
                    screen.blit(snake_img, (snake_x, snake_y))
                    pygame.draw.rect(screen, food_color, (food_x, food_y, food_size, food_size))
                    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
                    level_text = font.render("Level: " + str(snake_level), True, (255, 255, 255))
                    xp_text = font.render("XP: " + str(snake_xp) + "/" + str(xp_needed), True, (255, 255, 255))
                    screen.blit(score_text, (10, 10))
                    screen.blit(level_text, (10, 50))
                    screen.blit(xp_text, (10, 90))
                    pygame.display.flip()
                    play_random_microtransaction_sound()
            elif event.key == pygame.K_UP and snake_dy != snake_size:
                snake_dx = 0
                snake_dy = -snake_size
            elif event.key == pygame.K_DOWN and snake_dy != -snake_size:
                snake_dx = 0
                snake_dy = snake_size
            elif event.key == pygame.K_LEFT and snake_dx != snake_size:
                snake_dx = -snake_size
                snake_dy = 0
            elif event.key == pygame.K_RIGHT and snake_dx != -snake_size:
                snake_dx = snake_size
                snake_dy = 0
            elif event.key == pygame.K_RETURN:
                if pygame.Rect(snake_x, snake_y, snake_size, snake_size).colliderect(
                        pygame.Rect(food_x, food_y, food_size, food_size)):
                    microtransaction_window = True
                    show_microtransaction_window()

    if not microtransaction_window:
        # Update snake position
        snake_x += snake_dx
        snake_y += snake_dy

        # Check collision with boundaries
        if snake_x < 0 or snake_x >= screen_width or snake_y < 0 or snake_y >= screen_height:
            game_over = True

        # Check collision with food
        if pygame.Rect(snake_x, snake_y, snake_size, snake_size).colliderect(
                pygame.Rect(food_x, food_y, food_size, food_size)):
            score += 1
            snake_xp += 1
            if snake_xp >= xp_needed:
                snake_level += 1
                snake_size += 10
                snake_speed += 2
                snake_xp = 0
                xp_needed *= 2
                level_up_sound.play()
            food_x = random.randint(0, screen_width - food_size) // food_size * food_size
            food_y = random.randint(0, screen_height - food_size) // food_size * food_size

            # Add a new segment to the snake's body
            snake_segments.append((snake_x, snake_y))

        # Update food position
        food_x += food_dx
        food_y += food_dy

        # Check collision with food and boundaries
        if food_x < 0 or food_x >= screen_width - food_size:
            food_dx *= -1
        if food_y < 0 or food_y >= screen_height - food_size:
            food_dy *= -1

        # Update the snake's body segments
        if len(snake_segments) > 0:
            snake_segments.insert(0, (snake_x, snake_y))
            if len(snake_segments) > snake_level:
                snake_segments.pop()

        # Refresh the screen
        screen.fill(bg_color)
        for segment in snake_segments:
            screen.blit(snake_img, segment)
        
        # Draw the snake's head separately
        screen.blit(snake_img, (snake_x, snake_y))

        pygame.draw.rect(screen, food_color, (food_x, food_y, food_size, food_size))

        # Display score, level, and XP
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        level_text = font.render("Level: " + str(snake_level), True, (255, 255, 255))
        xp_text = font.render("XP: " + str(snake_xp) + "/" + str(xp_needed), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(xp_text, (10, 90))

        # Update the display
        pygame.display.flip()

        # Control game speed
        clock.tick(snake_speed)

    # Display microtransaction window if active
    if microtransaction_window:
        show_microtransaction_window()

# Play game over sound
game_over_sound.play()

# Wait for the sound to finish
pygame.time.wait(int(game_over_sound.get_length() * 1000))

# Quit the game
pygame.quit()
