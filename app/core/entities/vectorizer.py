import torch
from transformers import BertTokenizer, BertModel

class Vectorizer:

    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
        self.model = BertModel.from_pretrained("neuralmind/bert-base-portuguese-cased")

    def split_text(self, text, max_tokens=512):
        tokens = self.tokenizer.tokenize(text)
        segments = []
        for i in range(0, len(tokens), max_tokens):
            segment = tokens[i:i + max_tokens]
            if len(segment) < max_tokens:
                segment += [''] * (max_tokens - len(segment))  # Padding
            segments.append(segment)
        return segments
    
    def vectorize(self, text):
        all_embeddings = []

        segments = self.split_text(text)
        for segment in segments:
            input_ids = self.tokenizer.convert_tokens_to_ids(segment)
            input_ids = torch.tensor([input_ids])

            with torch.no_grad():
                outputs = self.model(input_ids)
                segment_embeddings = outputs.last_hidden_state.squeeze(0)  # Remove batch dimension
                all_embeddings.append(segment_embeddings)

        concatenated_embeddings = torch.cat(all_embeddings, dim=0)
        return concatenated_embeddings.numpy()