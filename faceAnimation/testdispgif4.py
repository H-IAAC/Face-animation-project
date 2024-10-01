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

    def play_animation(self, gif_path):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

        clip = VideoFileClip(gif_path)
        frames = clip.iter_frames(fps=clip.fps)
        num_frames = int(clip.fps * clip.duration)

        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Animated GIF')
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        clock = pygame.time.Clock()

        frame_count = 0

        while frame_count < num_frames:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            frame = next(frames)
            pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            pygame_frame = pygame.transform.scale(pygame_frame, (screen_width, screen_height))

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

    def start_neutral_animation(self):
        if self.current_path != self.neutral_path:
            self.play_animation(self.neutral_path)

    def stop_neutral_animation(self):
        self.neutral_playing = False

@app.route('/start_animation', methods=['POST'])
def start_animation():
    data = request.get_json()
    gif_path = data.get('animation')

    if gif_path:
        animation_player.start_animation(gif_path)
        return jsonify({'status': 'success', 'message': 'Animation started.'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request. Missing "animation" field in JSON.'})

if __name__ == "__main__":
    animation_player = AnimationPlayer()
    app.run(host='0.0.0.0', port=5000)
