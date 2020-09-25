from flask import Flask, request, jsonify, make_response
from detector import detect

MyApp = Flask(__name__)

UPLOAD_FOLDER = 'public'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@MyApp.route('/', methods=['GET'])
def test_get():
    return ('Hello World')


@MyApp.route('/detect', methods=['POST'])
def save_image():
    if 'file' not in request.files:
        return jsonify({"data": 'File is not Exist!'}), 422

    file = request.files['file']

    if file.filename == '':
        return jsonify({"data": 'File is not Valid!'}), 422

    if file and allowed_file(file.filename):
        results = detect(file)
        return jsonify(results), 200


if __name__ == "__main__":
    MyApp.run()
