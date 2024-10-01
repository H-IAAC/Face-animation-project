import pygame
from pygame.locals import *
from moviepy.editor import VideoFileClip
import numpy as np

def display_gif(gif_path):
    pygame.init()

    # Load the GIF using moviepy
    clip = VideoFileClip(gif_path)
    frames = clip.iter_frames(fps=clip.fps)
    num_frames = int(clip.fps * clip.duration)

    # Set up Pygame display in full screen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Animated GIF')

    # Get the screen dimensions
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

    clock = pygame.time.Clock()

    running = True
    frame_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Get the next frame from the GIF
        frame = next(frames)

        # Convert NumPy array to Pygame surface
        pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Resize the frame to fit the screen dimensions
        pygame_frame = pygame.transform.scale(pygame_frame, (screen_width, screen_height))

        # Display the frame
        screen.blit(pygame_frame, (0, 0))
        pygame.display.flip()

        frame_count += 1
        if frame_count == num_frames:
            running = False

        # Cap the frame rate
        clock.tick(clip.fps)

    pygame.quit()

if __name__ == "__main__":
    gif_path = "animations/animation.gif"  # Replace with the path to your animated GIF
    display_gif(gif_path)
