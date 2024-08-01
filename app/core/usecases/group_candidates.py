from ..interfaces.object_store import IObjectStore

class GroupCandidates:
      
    def __init__(self, storage: IObjectStore):
        self.storage = storage
    
    def vectorize_texts(self, texts, tokenizer, model):
        pass

    def execute(self):
        pass
