from flask import Flask, request, jsonify
import pygame
from pygame.locals import *
from moviepy.editor import VideoFileClip

app = Flask(__name__)



class AnimationPlayer:
    def __init__(self):
        self.neutral_path = "animations/neutral.gif"
        self.current_path = self.neutral_path
        self.neutral_playing = True


    """
    Plays a single animation frame by frame using Pygame, then quits.
    """
    def play_animation(self, gif_path):

        #TODO: Get the pygame and screen init and ending out of this method, and onto something bigger
        #TODO: update the self.current_path variable
        pygame.init()
        pygame.display.set_mode(size=(1, 1), flags=pygame.HIDDEN)
        pygame.display.set_caption('Animated face')

        #TODO: Add the .close() method to the clip object
        clip = VideoFileClip(gif_path)
        frames = clip.iter_frames(fps=clip.fps)
        num_frames = int(clip.fps * clip.duration)

        screen = pygame.display.set_mode(size=(0, 0), flags=pygame.SCALED)
        #screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        clock = pygame.time.Clock()

        frame_count = 0

        while frame_count < num_frames:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            frame = next(frames)
            pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            #pygame_frame = pygame.transform.scale(pygame_frame, (screen_width, screen_height))

            screen.blit(pygame_frame, (0, 0))
            pygame.display.flip()

            frame_count += 1
            clock.tick(clip.fps)

        pygame.quit()

    def start_animation(self, gif_path):
        self.stop_neutral_animation()
        self.play_animation(gif_path)
        self.current_path = gif_path
        self.start_neutral_animation()

    #TODO: Is this even necessary?
    def start_neutral_animation(self):
        if self.current_path != self.neutral_path:
            self.play_animation(self.neutral_path)

    #TODO: Is this even necessary?
    def stop_neutral_animation(self):
        self.neutral_playing = False




# Define the route for starting the animation
@app.route('/start_animation', methods=['POST'])

def start_animation():
    data = request.get_json()
    gif_path = data.get('animation')

    if gif_path:

        #TODO: Is this global variable a good practice?
        animation_player.start_animation(gif_path)
        return jsonify({'status': 'success', 'message': 'Animation started.'})
    
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request. Missing "animation" field in JSON.'})



if __name__ == "__main__":

    # Initialize the AnimationPlayer instance
    animation_player = AnimationPlayer()
            
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
    
