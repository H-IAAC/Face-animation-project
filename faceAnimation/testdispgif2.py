from flask import Flask, request, jsonify
from threading import Thread
import pygame
from pygame.locals import *
from moviepy.editor import VideoFileClip
import numpy as np

app = Flask(__name__)

class AnimationPlayer:
    def __init__(self):
        self.playing = False
        self.thread = None

    def play_animation(self, gif_path):
        pygame.init()
        clip = VideoFileClip(gif_path)
        frames = clip.iter_frames(fps=clip.fps)
        num_frames = int(clip.fps * clip.duration)

        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Animated GIF')
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

        clock = pygame.time.Clock()

        self.playing = True
        frame_count = 0

        while self.playing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.playing = False

            frame = next(frames)
            pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            pygame_frame = pygame.transform.scale(pygame_frame, (screen_width, screen_height))

            screen.blit(pygame_frame, (0, 0))
            pygame.display.flip()

            frame_count += 1
            if frame_count == num_frames:
                self.playing = False

            clock.tick(clip.fps)

        pygame.quit()

    def start_animation(self, gif_path):
        if not self.playing:
            self.thread = Thread(target=self.play_animation, args=(gif_path,))
            self.thread.start()
        else:
            self.playing = False
            self.thread.join()
            self.start_animation(gif_path)

    def stop_animation(self):
        self.playing = False
        if self.thread:
            self.thread.join()

animation_player = AnimationPlayer()

@app.route('/start_animation', methods=['POST'])
def start_animation():
    data = request.get_json()
    gif_path = data.get('animation')

    if gif_path:
        animation_player.start_animation(gif_path)
        return jsonify({'status': 'success', 'message': 'Animation started.'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request. Missing "animation" field in JSON.'})

@app.route('/stop_animation', methods=['POST'])
def stop_animation():
    animation_player.stop_animation()
    return jsonify({'status': 'success', 'message': 'Animation stopped.'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
