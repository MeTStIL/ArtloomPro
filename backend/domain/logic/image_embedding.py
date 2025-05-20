from clarifai_grpc.grpc.api import resources_pb2
from backend.domain.logic.clarifai_token_manager import token_manager


@token_manager.clarifai_api_error_handler
def get_image_embedding(image_url):
    input_obj = resources_pb2.Input(
        data=resources_pb2.Data(
            image=resources_pb2.Image(url=image_url)
        )
    )
    clip_model = token_manager.get_model()
    image_prediction = clip_model.predict(inputs=[input_obj])
    image_embeddings = image_prediction.outputs[0].data.embeddings
    image_vector = list(image_embeddings[0].vector)
    return image_vector

