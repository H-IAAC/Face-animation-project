from flask import Flask, request, jsonify
import threading
import pygame
from pygame.locals import *
from moviepy.editor import VideoFileClip

app = Flask(__name__)



'''
Function accessed via /display_animation url.
It receives a JSON with the path to the animation to be displayed,
and handles the signal to the animation thread.
'''
@app.route('/start_animation', methods=['POST'])
def start_animation():
    data = request.get_json()
    gif_path = data.get('animation')

    if gif_path:

        return jsonify({'status': 'success', 'message': 'Animation started.'})
    
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request. Missing "animation" field in JSON.'})



if __name__ == "__main__":

    thread_animation = threading.Thread(target=start_animation)
    
    app.run(port=5000, debug=True)

    #Run this at the deployment server, in order to open up the server to the network:
    #app.run(host='0.0.0.0', port=5000, debug=True)