from flask import Flask, render_template, Response

from camera import Camera


app = Flask(__name__)
fake_camera = Camera()


@app.route('/')
def index():
    return render_template('index.html')


def stream(camera):
    while True:
        frame = camera.get_frame()
        yield '--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


@app.route('/video_feed')
def video_feed():
    return Response(stream(fake_camera), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9594, debug=False)
