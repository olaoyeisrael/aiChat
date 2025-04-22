# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer('all-MiniLM-L6-v2')

# # def embed_chunks(chunks):
# #     embeddings = model.encode(chunks, convert_to_tensor=True)
# #     return [{"text": chunk, "embedding": emb.tolist()} for chunk, emb in zip(chunks, embeddings)]
# def embed_chunks(chunks):
#     if isinstance(chunks, str):
#         chunks = [chunks]
#     return model.encode(chunks, convert_to_tensor=False).tolist()

# def embed_query(query):
#     return model.encode(query).tolist()

# services/embedder.py

from transformers import AutoTokenizer, AutoModel
import torch

# Load model & tokenizer
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size())
    return (token_embeddings * input_mask_expanded).sum(1) / input_mask_expanded.sum(1)

def embed_chunks(texts: list[str]) -> list[list[float]]:
    """Convert text chunks into dense vector embeddings"""
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    pooled = mean_pooling(model_output, encoded_input['attention_mask'])
    return pooled.tolist()

def embed_query(query: str) -> list[float]:
    return embed_chunks([query])[0]