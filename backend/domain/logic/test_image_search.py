import numpy as np
from clarifai.client.model import Model
from clarifai_grpc.grpc.api import resources_pb2

PAT = "9db5fdcc208f445994f98d350337f291"
CLIP_MODEL_URL = "https://clarifai.com/clarifai/main/models/multilingual-multimodal-clip-embed"
model = Model(url=CLIP_MODEL_URL, pat=PAT)


def get_image_embedding(image_url):
    input_obj = resources_pb2.Input(
        data=resources_pb2.Data(
            image=resources_pb2.Image(url=image_url)
        )
    )
    image_prediction = model.predict(inputs=[input_obj])
    image_embeddings = image_prediction.outputs[0].data.embeddings
    image_vector = list(image_embeddings[0].vector)
    return image_vector


def get_text_embedding(text_input):
    input_obj = resources_pb2.Input(
        data=resources_pb2.Data(
            text=resources_pb2.Text(raw=text_input)
        )
    )
    text_prediction = model.predict(inputs=[input_obj])
    text_embeddings = text_prediction.outputs[0].data.embeddings
    text_vector = list(text_embeddings[0].vector)
    return text_vector


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def save_image_embeddings(filename, image_urls):
    with open(filename, 'a', encoding='utf-8') as f:
        for i, url in enumerate(image_urls, start=1):
            try:
                image_vector = get_image_embedding(url)
                vector_str = ",".join(str(x) for x in image_vector)
                f.write(f"{i}: URL={url} | Embedding=[{vector_str}]\n")
                print(f"Сохранён эмбеддинг для {url}")
            except Exception as e:
                print(f"Ошибка при обработке {url}: {e}")


def load_image_embeddings(filename):
    embeddings = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                parts = line.split(" | ")
                url_part = parts[0]
                emb_part = parts[1]
                url = url_part.split("URL=")[1].strip()
                emb_str = emb_part.replace("Embedding=[", "").replace("]", "")
                vector = [float(x) for x in emb_str.split(",") if x.strip() != ""]
                embeddings.append((url, vector))
            except Exception as e:
                print(f"Ошибка при парсинге строки: {line}\n{e}")
    return embeddings


embeddings_filename = "image_embeddings.txt"

# ОДИН РАЗ: сохранить эмбеддинги изображений (если необходимо)
# image_urls = [f"https://storage.yandexcloud.net/artloom-storage/{i}.jpg" for i in range(1, 101)]
# save_image_embeddings(embeddings_filename, image_urls)

stored_embeddings = load_image_embeddings(embeddings_filename)
print("Эмбеддинги изображений загружены из файла.")

text_input = input("Введите текстовое описание: ")
text_vector = get_text_embedding(text_input)
print("Получен эмбеддинг текста.")

results = []
for url, img_vector in stored_embeddings:
    sim = cosine_similarity(img_vector, text_vector)
    distance = 1 - sim
    results.append((url, sim, distance))

results.sort(key=lambda x: x[2])

top_n = 5
top_results = results[:top_n]

html = """
<html>
<head>
    <meta charset="utf-8">
    <title>Результаты поиска изображений</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f7f7f7; }}
        .container {{ display: flex; flex-wrap: wrap; justify-content: center; }}
        .card {{
            background: #fff; 
            border: 1px solid #ddd; 
            border-radius: 4px; 
            margin: 10px; 
            padding: 10px; 
            width: 220px; 
            text-align: center;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
        }}
        .card img {{ max-width: 200px; height: auto; border-radius: 4px; }}
        .card a {{ text-decoration: none; color: #337ab7; }}
    </style>
</head>
<body>
    <h2 style="text-align: center;">Топ {n} изображений, похожих на текст</h2>
    <div class="container">
""".format(n=top_n)

for i, (url, sim, distance) in enumerate(top_results, start=1):
    html += f"""
        <div class="card">
            <img src="{url}" alt="Image {i}">
            <p><strong>Изображение #{i}</strong></p>
            <p>URL: <a href="{url}" target="_blank">{url}</a></p>
            <p>Сходство: {sim:.4f}</p>
            <p>Расстояние: {distance:.4f}</p>
        </div>
    """

html += """
    </div>
</body>
</html>
"""

results_filename = "results.html"
with open(results_filename, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nРезультаты сохранены в файле {results_filename}.")