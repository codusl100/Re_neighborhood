from flask import Flask, render_template, request
from tensorflow.keras.utils import img_to_array
from keras.models import load_model
from PIL import Image
import flask
import io
#import boto3

AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""
BUCKET_NAME = ""

#s3 = boto3.client('s3',
#        aws_access_key_id = AWS_ACCESS_KEY,
#        aws_secret_access_key = AWS_SECRET_KEY)

app = flask.Flask(__name__)
# export model
model = load_model('C:/Users/codus/PycharmProjects/hackathon/Re_neighborhood/data/h5/model-for-usedgoods.h5')

@app.errorhandler(404)
def page_not_found(error):

	return render_template('404.html'), 404

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        
        return render_template('index.html')

    if request.method == 'POST':
        img = request.files["file"].read()
        img = Image.open(io.BytesIO(img)).convert("RGB")
        img = img.resize((256, 256))
        img = img_to_array(img)
        img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
        pred = model.predict(img)
        label = pred.argmax()
        label = 'p' + str(label)
        print(label)

        return render_template("index.html", label=label)
    
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    app.run(debug=True)