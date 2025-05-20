from clarifai_grpc.grpc.api import resources_pb2
from backend.domain.logic.clarifai_token_manager import token_manager


@token_manager.clarifai_api_error_handler
def get_text_embedding(text_input: str):
    input_obj = resources_pb2.Input(
        data=resources_pb2.Data(
            text=resources_pb2.Text(raw=text_input)
        )
    )
    clip_model = token_manager.get_model()
    text_prediction = clip_model.predict(inputs=[input_obj])
    text_embeddings = text_prediction.outputs[0].data.embeddings
    text_vector = list(text_embeddings[0].vector)
    return text_vector
