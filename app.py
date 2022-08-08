from flask import Flask, render_template, request
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.utils import img_to_array
from keras.models import load_model
from PIL import Image
import io

model = load_model('C:/Users/codus/PycharmProjects/hackathon/Re_neighborhood/data/h5/model-for-usedgoods.h5')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        
        return render_template('index.html')

    if request.method == 'POST':
        img = request.files["file"].read()
        img = Image.open(io.BytesIO(img))
        img = img.resize((256, 256))
        img = img_to_array(img)
        img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
        pred = model_for_man.predict(img)
        label = pred.argmax()

        return render_template("index.html", label=label)
    
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    app.run()