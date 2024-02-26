import sys

import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Game Over Example")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Create a font object
font = pygame.font.Font(None, 64)


# Function to display "Game Over" message and restart button
def game_over():
    # Draw the textbox
    pygame.draw.rect(screen, red, (150, 200, 500, 200))

    # Render and display "Game Over" text
    game_over_text = font.render("Game Over", True, black)
    text_rect = game_over_text.get_rect(center=(screen_width // 2, 250))
    screen.blit(game_over_text, text_rect)

    # Render and display "Restart" button
    restart_text = font.render("Restart", True, black)
    restart_rect = restart_text.get_rect(center=(screen_width // 2, 350))
    pygame.draw.rect(screen, white, restart_rect)
    screen.blit(restart_text, restart_rect)


# Main loop
game_over_flag = False
while not game_over_flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            restart_rect = pygame.Rect(screen_width // 2 - 100, 300, 200, 100)
            if restart_rect.collidepoint(mouse_pos):
                # If restart button is clicked, set game_over_flag to True to exit the loop
                game_over_flag = True

    # Clear the screen
    screen.fill(white)

    # Display "Game Over" message and restart button
    game_over()

    # Update the display
    pygame.display.update()

# Game loop (restarts the game)
# Add your game logic here...
