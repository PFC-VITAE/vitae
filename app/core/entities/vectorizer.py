from helpers.split_text import *
from transformers import AutoModel, AutoTokenizer
import numpy as np

class Vectorizer:

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
        self.model = AutoModel.from_pretrained('neuralmind/bert-base-portuguese-cased')

    def create_embedding_cls(self, text):
        tokens = self.tokenizer.encode_plus(text, max_length=500, truncation=True,
                                    padding='max_length', return_tensors='pt')
        outputs = self.model(**tokens)
        return outputs.last_hidden_state[0][0].detach().numpy().reshape(1,-1)

    def vectorize_text_bertimbau(self, text, text_id, curr_vector_id, vector_to_text_id):
        segments = split_text(text)
        segments_embeddings = np.empty((0, 768))

        for seg in segments: 
            segments_embeddings = np.vstack((segments_embeddings, self.create_embedding_cls(seg)))

        for i in range(len(segments)):
            vector_to_text_id[curr_vector_id + i] = text_id

        curr_vector_id += len(segments)

        return segments_embeddings, vector_to_text_id, curr_vector_id
    


