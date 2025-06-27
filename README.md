# Face animation project

This repo is home to the facial expression script for the automated wheelchair project in LCA-FEEC, Unicamp (State University of Campinas). It is intended to be used with a Raspberry pi.

The project works in the following manner: a pygame window displays a fullscreen, default gif continuously. There is also a Flask local webserver running, always listening for the new gif to display.
If it receives an instruction to change gifs, the requisition is put in a queue and is executed. In case of multiple requisitions, they are put in the queue and displayed one after the other sequentially, and once the queue is empty, the default gif resumes playing.
To send a gif requisition, one must first obtain the IP address of the device, and make a POST request to http://IP\_address/start\_animation with the following format:

{
    "animation": "animations/gif_name.gif"
}

The script is configured to run any gif inside the "animations" folder, if provided the correct name (the current gifs are just a proof of concept). One should see a response "animation started" from the request. The "Postman" application was used to test this project.

Note to run the project:
There is a Venv in the Raspberry pi with the libraries. Also, there is a bash script in the Desktop that automates launching it and the script (called faceAnimation/new\_flask\_server.py). Just run the Desktop script in order to execute the web server.

