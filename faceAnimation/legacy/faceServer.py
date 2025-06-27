from flask import Flask, request, jsonify
from PIL import Image, ImageTk, ImageSequence
import tkinter as tk
import threading
import os

app = Flask(__name__)

current_animation_path = None
animation_event = threading.Event()


class UpdatingLabel(tk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.photo_images = []

    def update_image(self, image):
        photo = ImageTk.PhotoImage(image)
        self.photo_images.append(photo)
        self.configure(image=photo)
        self.image = photo


def display_animation(animation_path, label, root):
    global current_animation_path

    if current_animation_path:
        # Stop the current animation
        root.destroy()

    current_animation_path = animation_path

    # Create the UpdatingLabel instance
    label = UpdatingLabel(root)
    label.pack()

    # Open the GIF file
    gif = Image.open(animation_path)

    def update_frame(iterator):
        try:
            frame = next(iterator)
            label.update_image(frame)
            root.after(gif.info['duration'], update_frame, iterator)
        except StopIteration:
            root.destroy()

    # Display the first frame and start the update loop
    iterator = ImageSequence.Iterator(gif)
    update_frame(iterator)


def run_flask_server():
    app.run(debug=True)


@app.route('/display_animation', methods=['POST'])
def display_animation_request():
    global current_animation_path, animation_event

    data = request.get_json()

    if 'animation' not in data:
        return jsonify({'error': 'Invalid request. Missing "animation" field in JSON.'}), 400

    animation_path = data['animation']

    if not os.path.isfile(animation_path):
        return jsonify({'error': f'File not found: {animation_path}'}), 404

    # Signal the main thread to display the animation
    current_animation_path = animation_path
    animation_event.set()

    return jsonify({'success': f'Animation "{animation_path}" is being displayed.'})


def main():
    global current_animation_path, animation_event

    while True:
        animation_event.wait()

        root = tk.Tk()
        root.attributes('-fullscreen', True)

        # Start the animation loop in a new thread
        label = UpdatingLabel(root)
        threading.Thread(target=display_animation, args=(current_animation_path, label, root)).start()

        # Clear the signal
        animation_event.clear()

        root.mainloop()


if __name__ == '__main__':
    # Start the main loop in a separate thread
    threading.Thread(target=main).start()

    # Run the Flask app in the main thread
    run_flask_server()
