import sys

import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Time Example")

# Create a font object
font = pygame.font.Font(None, 36)  # None uses the default system font


# Function to render time text onto a surface
def render_time_text(time_elapsed):
    text_surface = font.render(
        "Time elapsed: {:.2f} seconds".format(time_elapsed), True, (0, 0, 0)
    )
    return text_surface


# Get the start time of the game
start_time = pygame.time.get_ticks()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the current time
    current_time = pygame.time.get_ticks()

    # Calculate the time elapsed since the beginning of the game (in seconds)
    time_elapsed = (
        current_time - start_time
    ) / 1000.0  # Convert milliseconds to seconds

    # Create a surface to display time text
    time_surface = render_time_text(time_elapsed)

    # Blit the time surface onto the screen
    screen.fill((255, 255, 255))  # Fill screen with white color
    screen.blit(
        time_surface, (20, 20)
    )  # Blit time surface onto screen at specified position

    # Update the display
    pygame.display.update()
