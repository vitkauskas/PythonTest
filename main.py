# -*- coding: utf-8 -*- 
# support russian character
import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory, \
    jsonify
from werkzeug.utils import secure_filename

import numpy as np
#import tensorflow.keras as keras
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential, load_model, save_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image

# Инициализируем Flask
app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'


# Загрузка модели нейронной сети
#model = load_model("model_mnist.h5")
model = load_model("data/model_mnist.h5") # вариант для диска

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413
    
@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return '', 204

@app.route('/hello')
def hello():
    return "Привет, Мир!"

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

# Задаем функцию Predict
@app.route('/predict')
def predict_page():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('predict.html', files=files)

@app.route('/predict', methods=["GET","POST"])
def predict():
    data = {"success": False}

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
#        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

        print(uploaded_file.filename)

        img_ = image.load_img(uploaded_file.filename, target_size=(28, 28))
        img_arr = image.img_to_array(img_)

        # нормализация данных подаваемых в сеть
        img_arr = img_arr.astype('float32') / 255
        # расчет модели 
        img_arr = np.dot(np.array(img_arr[..., :3]), [0.2989, 0.5870, 0.1140])[..., np.newaxis]
        img_arr = np.expand_dims(img_arr, axis=0)
        
        img_arr = img_arr.reshape(1,28,28,1)

        image_datagen = image.ImageDataGenerator(
            featurewise_center=True, featurewise_std_normalization=True)
        image_datagen.fit(img_arr)
        image_datagen.standardize(img_arr)

        # Записываем значение prediction в data["prediction"]
        data["prediction"] = str( np.argmax(model.predict(img_arr)) )
        #Записываем статус в data["success"]
        data["success"] = True
    
    #Возвращаем результат json format 
    return jsonify(data) 
