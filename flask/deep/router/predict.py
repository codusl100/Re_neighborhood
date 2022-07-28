# POST로 받은 이미지를 분류하는 API

from flask_restx import Namespace, Resource
#
#
#
import base64
predict_ns = Namespace('Predict', path='index.py', description='predict')
swagger_parser = predice_ns.parser()

model = ModelManager(CNN, 'models/predict.pt')

@predict_ns.route('/predict')
class Predict(Resource):

    @predict_ns.doc(responses={
        200: 'OK',
        204: 'Failed to find Object',
        400: 'Bad Request',
        500: 'Internal Server Error'
    })
    @predict_ns.expect(swagger_parser)
    def post(self):
        if "image" not in request.files:
            raise ValueError
        input_image = request.files["image"].read()
        if("Content-Transfer-Encoding" in request.headers and request.headers["Content-Transfer-Encoding"] == "base64"):
            input_image = base64.decodebytes(input_image)
        manager = ImageManager(input_image)

        tensor_image = manager.find_Object().crop_image().to_tensor().get_image()

        predicted = model.predict(tensor_image)

        Object_box = manager.get_Object()
        response = {
            "predict": predicted,
            "top": Object_box[0],
            "right": Object_box[1],
            "bottom": Object_box[2],
            "left": Object_box[3]
        }
        print(predicted)
        return response, 200
