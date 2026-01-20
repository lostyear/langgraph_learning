from sentence_transformers import SentenceTransformer
from functools import lru_cache


@lru_cache(maxsize=1)
def get_embedding_model(
    name="all-MiniLM-L6-v2", cache_folder="./.models"
) -> SentenceTransformer:
    model = SentenceTransformer(name, cache_folder=cache_folder)
    return model


if __name__ == "__main__":
    model = get_embedding_model("Qwen/Qwen3-Embedding-0.6B")
    texts = ["小明在A公司工作，负责行政", "小红在B公司工作，负责人力"]
    target = ["小明是A公司的行政人员", "小红是C公司的运营人员"]
    emb = model.encode(texts, normalize_embeddings=True)
    t_emb = model.encode(target, normalize_embeddings=True)

    matrix = emb @ t_emb.T

    for i, item in enumerate(texts):
        for j, t in enumerate(target):
            print(f"simlar {matrix[i][j]}: A: {item}, B:{t}")
