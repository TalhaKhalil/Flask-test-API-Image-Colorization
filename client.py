print("hello")
import base64
import requests 
from PIL import Image 
import cloudinary
url = 'http://127.0.0.1:5000/im_size'
my_img = {'image': open('test.jpg', 'rb')}
print(my_img)
r = requests.post(url, files=my_img)
print("posting image ")
resp = r.json()

# convert server response into JSON format.
rnew = resp['status']
img = base64.b64decode(rnew)
print(img)
