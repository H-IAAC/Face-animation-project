import os
import json
from flask import Flask, request, jsonify
import pygame
from pygame.locals import *

app = Flask(__name__)

# Set the path to the directory where your GIFs are stored
GIF_DIRECTORY = r'animations'

# Initialize Pygame
pygame.init()

# Set display mode to full screen
screen = pygame.display.set_mode((0, 0), FULLSCREEN)

def display_gif(gif_path):
    gif_path = os.path.join(GIF_DIRECTORY, gif_path)
    try:
        gif = pygame.image.load(gif_path)
        screen.blit(gif, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5000)  # Adjust the delay as needed
        return True
    except pygame.error as e:
        print(f"Error loading GIF: {e}")
        return False

@app.route('/display', methods=['POST'])
def display():
    data = request.get_json()

    if 'animation' not in data:
        return jsonify({'error': 'Invalid JSON format'}), 400

    animation_path = data['animation']
    success = display_gif(animation_path)

    if success:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'error': 'Failed to display GIF'}), 500

if __name__ == '__main__':
    app.run(debug=True)
