from flask import Flask, request, jsonify
from flask_cors import CORS
import test
import requests

app = Flask(__name__)
CORS(app)

image_ready = False
image_path = "satellite_image.png"

@app.route("/")
def index():
  return "Fukc"

@app.route("/image", methods=["POST"])
def gen_image():

  body = request.get_json()

  addy = body["address"]
  print(addy)
  test.get_storefront_img(addy)

  return jsonify({"image_path": "Image generation Complete"})

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5001, debug=True)
