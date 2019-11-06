# main.py

from flask import Flask, render_template, Response
from camera import VideoCamera

app = Flask(__name__)
objcam=VideoCamera()
@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        frame = VideoCamera.get_frame(objcam)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def gen2():
    """Returns a single image frame"""
    frame = VideoCamera.get_frame(objcam)
    yield frame

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image.jpg')
def image():
    """Returns a single current image for the webcam"""
    return Response(gen2(), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8082', debug=False)