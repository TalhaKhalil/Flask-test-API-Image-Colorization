# from flask import Flask 
# app = Flask(__name__)
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
# @app.route('/',method = ['POST'])
# def get_response():
#     return 
# ==================request and response JSON 
from flask import Flask, render_template, request, url_for, jsonify,Response
# import jsonpickle
import numpy as np
import cv2
from PIL import Image
from skimage import color
import base64
import os , io , sys

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/tests/endpoint', methods=['POST'])
def my_test_endpoint():
    input_json = request.get_json(force=True) 
    # force=True, above, is necessary if another developer 
    # forgot to set the MIME type to 'application/json'
    print('data from client:', input_json)
    dictToReturn = {'answer':42}
    return jsonify(dictToReturn)

@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    files = r.files['image']
    print(files)
    nparr = np.fromstring(r.data, np.uint8)
    print(nparr)
    # decode image
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....

    # build a response dict to send back to client
    # response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
    #             }
    # encode response using jsonpickle
    # response_pickled = jsonpickle.encode(response)
    response = "Fetched Image"

    return Response(response=response, status=200)
@app.route("/im_size", methods=["POST"])
def process_image():
    file = request.files['image']
    # Read the image via file.stream
    img = Image.open(file.stream)
    img = np.array(img)
    # img = color.rgb2gray(img)
    # img = Image.fromarray(img)
    # img.save("grey.jpg")
    # print("saved")
    img = Image.fromarray(img.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return jsonify({'status':str(img_base64)})
    #return jsonify({'msg': 'success'})

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      print("image response =>"+str(f))
      response = "Fetched Image"
    #   f.save(secure_filename(f.filename))

      return Response(response=response, status=200)
if __name__ == '__main__':
    app.run(debug=True)
#=====================POST and GET image===================
# from flask import Flask, request, Response
# import jsonpickle
# import numpy as np
# import cv2

# # Initialize the Flask application
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# # route http posts to this method
# @app.route('/api/test', methods=['POST'])
# def test():
#     r = request
#     # convert string of image data to uint8
#     nparr = np.fromstring(r.data, np.uint8)
#     # decode image
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # do some fancy processing here....

#     # build a response dict to send back to client
#     response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
#                 }
#     # encode response using jsonpickle
#     response_pickled = jsonpickle.encode(response)

#     return Response(response=response_pickled, status=200, mimetype="application/json")

# # @app.route('/predict/',methods=['GET','POST'])
# # def predict():
# # 	response = "For ML Prediction"
# # return response	

# # start flask app
# app.run(host="0.0.0.0", port=5000)

