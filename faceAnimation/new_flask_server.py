import pygame
from flask import Flask, request, jsonify
import threading
from queue import Queue, Empty
from pygame.locals import *
from moviepy import *



class GifServer:

    def __init__(self):

        self.app = Flask(__name__)
        self.animation_queue = Queue()
        self.stop_event = threading.Event()  # Event to stop display thread
        self.default_animation_path = "animations/neutral.gif"
        self.current_path = self.default_animation_path
        self.setup_route()

        return
    

    def setup_route(self):
        '''
        Function accessed via /display_animation url.
        It receives a JSON with the path to the animation to be displayed,
        and handles the signal to the animation thread.
        '''
        @self.app.route('/start_animation', methods=['POST'])
        def start_animation():

            data = request.get_json()
            gif_path = data.get('animation')

            if gif_path:
                self.animation_queue.put(gif_path)
                return jsonify({'status': 'success', 'message': 'Animation started.'})
            
            else:
                return jsonify({'status': 'error', 'message': 'Invalid request. Missing "animation" field in JSON.'})


    def gif_display(self):
        pygame.init()
        screen = pygame.display.set_mode(size=(0, 0))
        pygame.display.set_caption('Animated face')

        while True:

            if self.animation_queue.empty():
               self.current_path = self.default_animation_path
            else:
                self.current_path = self.animation_queue.get()
                
            clip = VideoFileClip(self.current_path)
            frames = clip.iter_frames(fps=clip.fps)
            num_frames = int(clip.fps * clip.duration)

            screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

            clock = pygame.time.Clock()

            frame_count = 0
            while frame_count < num_frames:

                #check for user closing the window
                for event in pygame.event.get():
                    if event.type == QUIT:
                        clip.close()
                        pygame.quit()
                        return

                frame = next(frames)
                pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                pygame_frame = pygame.transform.scale(pygame_frame, (screen_width, screen_height))

                screen.blit(pygame_frame, (0, 0))
                pygame.display.flip()

                frame_count += 1
                clock.tick(clip.fps)
            
            clip.close()


    def run_server(self):
        
        thread_gif_display = threading.Thread(target=self.gif_display, daemon=True)
        thread_gif_display.start()

        # !! debug=True summons 2 screens instead of 1 !!
        self.app.run(port=5000, debug=False, use_reloader=False)

        #Run this at the deployment server, in order to open up the server to the network:
        #app.run(host='0.0.0.0', port=5000, debug=False)
        
        return



if __name__ == "__main__":

    gif_server = GifServer()
    gif_server.run_server()
