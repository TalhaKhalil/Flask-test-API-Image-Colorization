from flask import Flask, render_template, request, url_for, jsonify,Response
# import jsonpickle
import numpy as np
import cv2
from PIL import Image
from skimage import color
import base64
import os , io , sys
import cloudinary 
from PIL import Image
import requests
from io import BytesIO
from cloudinary.uploader import upload
app = Flask(__name__)

os.chdir(os.path.join(os.path.dirname(sys.argv[0]), '.'))
if os.path.exists('settings.py'):
    exec(open('settings.py').read())

cloudinary.config( 
  cloud_name = "drqzgt17b", 
  api_key = "762526682378155", 
  api_secret = "9vDOTnh0rNd4i7KmfObjxYGS-C4" 
)
# def upload(file, **options)

def read_img_url(url, size = (256,256)):
    
    """
    Read and resize image directly from a url
    """
    response = requests.get(url)
    #print(response.content)
    
    img = Image.open(BytesIO(response.content))
    #print(img)

    return img

@app.route('/') #aws.com/ will return hello world on browser
def hello_world():
    return 'Hello, World!'

@app.route('/tests/endpoint', methods=['POST']) #aws.com/tests/endpoint # client will send an image and this function will return a text in json
def my_test_endpoint():
    input_json = request.get_json(force=True) 
    # force=True, above, is necessary if another developer 
    # forgot to set the MIME type to 'application/json'
    url = input_json["url"]
    
    print('URL =>', url)
    img=read_img_url(url)
    print("fetched image")
    img = img.convert('L')
    img.save("greyoutput.jpg")
    res = upload("C:/Users/AALY/myproject/greyoutput.jpg")
    print(res)
    dictToReturn = {'url':res["url"]}
    return jsonify(dictToReturn)

@app.route('/api/test', methods=['POST']) # client will send an image server shall return some string text 
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
@app.route("/im_size", methods=["POST"]) # client will send image to server will return image as well 
def process_image():
    file1 = request
    print(file1)
    file = request.files['image'] 
    print(file)
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

