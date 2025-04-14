from clarifai_grpc.grpc.api import resources_pb2
from backend.config import CLIP_MODEL


def get_image_embedding(image_url):
    input_obj = resources_pb2.Input(
        data=resources_pb2.Data(
            image=resources_pb2.Image(url=image_url)
        )
    )
    image_prediction = CLIP_MODEL.predict(inputs=[input_obj])
    image_embeddings = image_prediction.outputs[0].data.embeddings
    image_vector = list(image_embeddings[0].vector)
    return image_vector

