from sentence_transformers import SentenceTransformer
from helpers.split_text import *


class Vectorizer:

    def __init__(self):
        self.model = SentenceTransformer("bert-base-nli-mean-tokens")

    def vectorize_text(self, text, text_id, curr_vector_id, vector_to_text_id):
        segments = split_text(text)

        segments_embeddings = self.model.encode(segments)

        for i in range(len(segments)):
            vector_to_text_id[curr_vector_id + i] = text_id

        curr_vector_id += len(segments)

        return segments_embeddings, vector_to_text_id, curr_vector_id

    def vectorize(self, sentence):
        return self.model.encode([sentence])
