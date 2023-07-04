# game.py
import webbrowser
import pygame
import random
import microtransactions  # Import the microtransactions module
import time
import random

# Determine if the DLC is activated
DLC_ACTIVATED = random.random() < 0.25  # 20% chance of DLC being activated

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake RPG Game")

# Load background image
background_img = pygame.image.load("American Flag.png")
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Set colors
snake_color = (0, 255, 0)
food_color = (0, 255, 0)

# Load Guy Fieri image for the snake
snake_img = pygame.image.load("guy_fieri.png")
snake_img = pygame.transform.scale(snake_img, (40, 40))  # Increase size to 40x40 pixels

# Define snake properties
snake_size = 40  # Increase size to match the image dimensions
snake_speed = 30 if DLC_ACTIVATED else 20
snake_level = 1
snake_xp = 0
xp_needed = 10

# Define initial position of snake
snake_x = screen_width // 2
snake_y = screen_height // 2
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

# Define snake body
snake_body = []
snake_length = 1

# Define momentum properties
momentum = 0.1
snake_dx_momentum = 0
snake_dy_momentum = 0

# Define how many segments behind the head to ignore for collision
ignore_segments = 7

# Add lore
lore_font = pygame.font.Font(None, 24)
lore_text = [
    "In the dystopian city of Flavortown, Guy Fieri, now a mighty snake, fights against time and the system.",
    "The food has been taken over by a corrupt corporate entity, turning it into red power cubes.",
    "These cubes increase Guy's size and energy, but they're a scarce resource, heavily guarded, and dangerous to reach.",
    "Will he be able to conquer the system or will he succumb to its oppressive mechanisms?",
    "The path is treacherous, the stakes are high, but our Flavortown hero won't give up!",
]
screen.fill((0, 0, 0))  # Clear screen
for i, line in enumerate(lore_text):
    text = lore_font.render(line, True, (255, 255, 255))
    screen.blit(text, (10, 10 + i*30))  # Adjust 30 for line spacing
pygame.display.flip()
pygame.time.wait(10000)  # Show lore for 10 seconds

# Game loop
game_over = False
microtransaction_window = False
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if microtransaction_window:
                    microtransaction_window = False
                    screen.blit(background_img, (0, 0))
                    screen.blit(snake_img, (snake_x, snake_y))
                    pygame.draw.rect(screen, food_color, (food_x, food_y, food_size, food_size))
                    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
                    level_text = font.render("Level: " + str(snake_level), True, (255, 255, 255))
                    xp_text = font.render("XP: " + str(snake_xp) + "/" + str(xp_needed), True, (255, 255, 255))
                    screen.blit(score_text, (10, 10))
                    screen.blit(level_text, (10, 50))
                    screen.blit(xp_text, (10, 90))
                    pygame.display.flip()
                    microtransactions.play_random_microtransaction_sound()
            if event.key == pygame.K_UP and snake_dy_momentum != snake_size:
                snake_dx_momentum = 0
                snake_dy_momentum = -snake_size
            elif event.key == pygame.K_DOWN and snake_dy_momentum != -snake_size:
                snake_dx_momentum = 0
                snake_dy_momentum = snake_size
            elif event.key == pygame.K_LEFT and snake_dx_momentum != snake_size:
                snake_dx_momentum = -snake_size
                snake_dy_momentum = 0
            elif event.key == pygame.K_RIGHT and snake_dx_momentum != -snake_size:
                snake_dx_momentum = snake_size
                snake_dy_momentum = 0
            elif event.key == pygame.K_RETURN:
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
                    snake_length += 1
                    microtransaction_window = True

    if not microtransaction_window:

        if DLC_ACTIVATED:  # Check if DLC is activated
        # Generate a random RGB color for the food
            food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Modify current snake velocity based on momentum
        snake_dx += (snake_dx_momentum - snake_dx) * momentum
        snake_dy += (snake_dy_momentum - snake_dy) * momentum

        # Ensure that velocity does not exceed max speed
        snake_dx = max(-snake_speed, min(snake_speed, snake_dx))
        snake_dy = max(-snake_speed, min(snake_speed, snake_dy))

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

            # Add a new body part at the end of the snake
            if snake_body:
                snake_body.append(snake_body[-1])
            else:
                snake_body.append((snake_x, snake_y))
        
            snake_length += 1
            microtransaction_window = True


        # Update food position
        food_x += food_dx
        food_y += food_dy

        # Check collision with food and boundaries
        if food_x < 0 or food_x >= screen_width - food_size:
            food_dx *= -1
        if food_y < 0 or food_y >= screen_height - food_size:
            food_dy *= -1

        # Update snake body
        snake_body.insert(0, (snake_x, snake_y))
        if len(snake_body) > snake_length:
            snake_body.pop()

        # Check collision with snake body
        for body_part in snake_body[ignore_segments:]:
            if pygame.Rect(snake_x, snake_y, snake_size, snake_size).colliderect(
                    pygame.Rect(body_part[0], body_part[1], snake_size, snake_size)):
                game_over = True

        # Refresh the screen
        screen.blit(background_img, (0, 0))
        for body_part in snake_body:
            screen.blit(snake_img, body_part)
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
        microtransactions.show_microtransaction_window(screen)

# Define the credits
credits_font_normal = pygame.font.Font("Roboto-Italic.ttf", 36)
credits_font_bold = pygame.font.Font("Roboto-Bold.ttf", 36)
credits_lines = [
    {"text": "SNAKE 2", "font": credits_font_bold},
    {"text": "Powered by Twitch Chat", "font": credits_font_normal},
    {"text": "Developed by YOU", "font": credits_font_normal},
    {"text": "Physics Engine by Pygame", "font": credits_font_normal},
    {"text": "Microtransaction Technology by Microtransactions Module", "font": credits_font_normal},
    {"text": "Artwork 'Borrowed' from the Internet", "font": credits_font_normal},
    {"text": "Incredible Sound Design by Random Sounds from the Web", "font": credits_font_normal},
    {"text": "Special Thanks to Guy Fieri for Inspiration", "font": credits_font_normal},
    {"text": "And a Huge Thanks to YOU for Playing!", "font": credits_font_normal},
    {"text": "", "font": credits_font_normal},
    {"text": "If you enjoyed the game, please purchase our DLC, Tears of the Kingdom", "font": credits_font_normal},
]

# Play game over sound
game_over_sound.play()

# Display the credits
screen.fill((0, 0, 0))  # Clear screen
for i, line in enumerate(credits_lines):
    text = line["font"].render(line["text"], True, (255, 255, 255))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + i*50 - len(credits_lines)*50 // 2))  # Center the text
pygame.display.flip()

# Wait for the credits to be displayed
pygame.time.wait(10000)  # Show credits for 10 seconds

# Wait for the sound to finish
pygame.time.wait(int(game_over_sound.get_length() * 1000))

# Open the YouTube video
webbrowser.open("https://www.nintendo.com/store/products/the-legend-of-zelda-tears-of-the-kingdom-switch/")

time.sleep(5)
webbrowser.open("https://www.youtube.com/watch?v=3B21d32wn9s&ab_channel=PointCrow")
time.sleep(1)
webbrowser.open("https://www.youtube.com/watch?v=3B21d32wn9s&ab_channel=PointCrow")
time.sleep(1)
webbrowser.open("https://www.youtube.com/watch?v=3B21d32wn9s&ab_channel=PointCrow")
time.sleep(1)
webbrowser.open("https://www.youtube.com/watch?v=3B21d32wn9s&ab_channel=PointCrow")
time.sleep(1)
webbrowser.open("https://www.youtube.com/watch?v=3B21d32wn9s&ab_channel=PointCrow")

# Quit the game
pygame.quit()
