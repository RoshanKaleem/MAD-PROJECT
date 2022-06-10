from flask import Flask, request, send_file, jsonify, url_for
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from io import BytesIO
import numpy as np
from matplotlib import pyplot as plt
import io
import chardet

from io import BytesIO
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from base64 import encodebytes
import base64
from model import load_model, generate_caption
from index import index_caption, search_caption
import uuid

transformer = load_model()
app = Flask(__name__)
CORS(app)


api = Api(app)


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode(
        'ascii')  # encode as base64
    return encoded_img


class Users(Resource):
    # methods go here

    def get(self):
        # reuslt  contains list of path images
        encoded_imges = []
        for _ in range(0, 3):
            encoded_imges.append("http://10.0.2.2:5000" +
                                 url_for('static', filename='img.png'))
        return encoded_imges

    def post(self):

        img = request.files['picture']

        img = plt.imread(img)
        # img.save("img.png")
        im = Image.fromarray(img)
        path = f"static/{uuid.uuid4().hex}.jpg"
        im.save(path)
        x = generate_caption(path, transformer)
        index_caption(x, path)
        return x[9:]


class images(Resource):
    def post(self):
        print(request.json["title"])
        response = search_caption(request.json["title"])
        encoded_imges = []
        for i in response:
            encoded_imges.append("http://10.0.2.2:5000/" + i)
        print(encoded_imges)
        if len(encoded_imges) > 0:
            return encoded_imges
        else:
            encoded_imges.append("http://10.0.2.2:5000/static/4.jpg")
            encoded_imges.append("http://10.0.2.2:5000/static/3.jpg")
            encoded_imges.append("http://10.0.2.2:5000/static/2.jpg")
            encoded_imges.append("http://10.0.2.2:5000/static/1.jpg")
                
            return encoded_imges
      




api.add_resource(Users, '/users')   # methods go here

api.add_resource(images, '/images')

if __name__ == '__main__':
    app.run()
