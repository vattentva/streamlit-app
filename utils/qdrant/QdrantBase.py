import streamlit as st
from typing import List
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStoreRetriever

from qdrant_client import QdrantClient, models

from utils import const

class QdrantBase():
    def __init__(self):
        self.COLLECTION_NAME = const.QD_COLLECTION_NAME
        self.client = QdrantClient(
            url=st.secrets.get('QDRANT_URL', ''),
            api_key=st.secrets.get('QDRANT_API_KEY', ''),
        )
        # コレクションが存在しなければ作成
        if not self.client.collection_exists(self.COLLECTION_NAME):
            self.create_collection()
    
    def get_collections(self) -> List[str]:
        collections = self.client.get_collections().collections
        # コレクション名をリストとして抽出
        return [collection.name for collection in collections]
    
    def create_collection(self):
        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        )

    def get_vector_store(self) -> Qdrant:
        return Qdrant(
            client=self.client,
            collection_name=self.COLLECTION_NAME,
            embeddings=OpenAIEmbeddings()
        )
    
    def get_points(self):
        # コレクション内の全ポイントを取得
        all_points = self.client.scroll(collection_name=self.COLLECTION_NAME)
        # ポイントデータのリスト
        return [point for point in all_points]
    
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
            collection_name=self.COLLECTION_NAME,
        )
    
    def get_retriever(self, k = 10) -> VectorStoreRetriever:
        return self.get_vector_store().as_retriever(
            search_type="similarity", # "mmr", "similarity_score_threshold"
            search_kwargs={"k":k}    # 文書を何個取得するか (default: 4)
    )
