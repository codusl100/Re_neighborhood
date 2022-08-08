# 필수 패키지를 import합니다.
from flask import Flask, render_template, request
from keras.applications import ResNet50
from tensorflow.keras.utils import img_to_array
from keras.applications import imagenet_utils
from keras.models import load_model
from PIL import Image
import numpy as np
import flask
import io

# Flask 애플리케이션과 Keras 모델을 초기화합니다.
app = flask.Flask(__name__)
model = load_model('C:/Users/codus/PycharmProjects/hackathon/Re_neighborhood/data/h5/model-for-usedgoods.h5')

def load_model():
    # 미리 학습된 Keras 모델을 불러옵니다(여기서 우리는 ImageNet으로 학습되고 
    # Keras에서 제공하는 모델을 사용합니다. 하지만 쉽게 하기위해
    # 당신이 설계한 신경망으로 대체할 수 있습니다.)
    model = ResNet50(weights="imagenet")
    
def prepare_image(image, target):
    # 만약 이미지가 RGB가 아니라면, RGB로 변환해줍니다.
    if image.mode != "RGB":
        image = image.convert("RGB")

    # 입력 이미지 사이즈를 재정의하고 사전 처리를 진행합니다.
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # 처리된 이미지를 반환합니다.
    return image

@app.route("/predict", methods=["GET","POST"])
def predict():
    # view로부터 반환될 데이터 딕셔너리를 초기화합니다.
    data = {"success": False}

    # 이미지가 엔트포인트에 올바르게 업로드 되었는디 확인하세요
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # PIL 형식으로 이미지를 읽어옵니다.
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))

            # 분류를 위해 이미지를 전처리합니다.
            image = prepare_image(image, target=(224, 224))

            # 입력 이미지를 분류하고 클라이언트로부터 반환되는 예측치들의 리스트를 초기화 합니다.
            preds = model.predict(image)
            results = imagenet_utils.decode_predictions(preds)
            data["predictions"] = []

            # 결과를 반복하여 반환된 예측 목록에 추가합니다.
            for (imagenetID, label, prob) in results[0]:
                r = {"label": label, "probability": float(prob)}
                data["predictions"].append(r)

            # 요청이 성공했음을 나타냅니다.
            data["success"] = True

    # JSON 형식으로 데이터 딕셔너리를 반환합니다.
    return flask.jsonify(data)

# 실행에서 메인 쓰레드인 경우, 먼저 모델을 불러온 뒤 서버를 시작합니다.
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    load_model()
    app.run()