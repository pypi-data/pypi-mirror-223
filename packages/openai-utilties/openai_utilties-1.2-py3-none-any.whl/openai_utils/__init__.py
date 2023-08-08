import openai
import numpy as np

api_key: str = ""


def AskGPT(model: str, context: list) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=context
    )
    return response["choices"][0]["message"]["content"]


def GetEmbedding(String: str) -> list:
    data = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=String
    )
    return data["data"][0]["embedding"]


def GetEmbeddingDistance(Embedding1: list, Embedding2: list) -> int:
    data1 = np.array(Embedding1)
    data2 = np.array(Embedding2)
    total = data1 - data2
    num = 0
    for i in total:
        num += i
    return abs(num)
