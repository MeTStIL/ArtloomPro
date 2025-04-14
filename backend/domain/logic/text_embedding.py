from clarifai_grpc.grpc.api import resources_pb2
from backend.config import CLIP_MODEL


def get_text_embedding(text_input):
    input_obj = resources_pb2.Input(
        data=resources_pb2.Data(
            text=resources_pb2.Text(raw=text_input)
        )
    )
    text_prediction = CLIP_MODEL.predict(inputs=[input_obj])
    text_embeddings = text_prediction.outputs[0].data.embeddings
    text_vector = list(text_embeddings[0].vector)
    return text_vector
