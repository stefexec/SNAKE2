# microtransactions.py

import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
bg_color = (0, 0, 0)

# Define font
font = pygame.font.Font(None, 36)

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
def show_microtransaction_window(screen):
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
