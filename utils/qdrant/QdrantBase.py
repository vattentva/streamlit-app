from typing import List
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStoreRetriever

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from utils import const

class QdrantBase():
    def __init__(self, client: QdrantClient):
        self.client = client
    
        # すべてのコレクション名を取得
        collection_names = [c.name for c in self.get_all_collections()]
        # コレクションが存在しなければ作成
        if const.QD_COLLECTION_NAME not in collection_names:
            self.create_collection(const.QD_COLLECTION_NAME)

    def get_vector_store(self) -> Qdrant:
        return Qdrant(
            client=self.client,
            collection_name=const.QD_COLLECTION_NAME,
            embeddings=OpenAIEmbeddings()
        )
    
    def search(self, query: str = '') -> List[Document]:
        return self.get_vector_store().similarity_search(query=query)
    
    def add_texts(self, texts: List[str]) -> List[str]:
        return self.get_vector_store().add_texts(texts)
    
    def from_texts(self, texts: List[str]) -> List[str]:
        """
        以下のようにもできる。この場合は毎回ベクトルDBが初期化される
        LangChain の Document Loader を利用した場合は `from_documents` にする
        """
        return self.get_vector_store().from_texts(
            texts,
            OpenAIEmbeddings(),
            path=const.QD_PATH,
            collection_name=const.QD_COLLECTION_NAME,
        )
    
    def get_retriever(self, k = 10) -> VectorStoreRetriever:
        return self.get_vector_store().as_retriever(
            search_type="similarity", # "mmr", "similarity_score_threshold"
            search_kwargs={"k":k}    # 文書を何個取得するか (default: 4)
    )
    
    def get_all_collections(self):
        return self.client.get_collections().collections
    
    def create_collection(self, name: str):
        self.client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

