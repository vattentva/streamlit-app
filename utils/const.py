from enum import Enum

class RequestType(Enum):
    CHAT = 2
    SUMMARY = 3
    YOUTUBE = 4
    PDF = 5

SYSTEM_MESSAGE = 'You are a helpful assistant.'

LLM_PAGES = [
    {'path': 'llm/langchain_openai.py', 'title': 'Chatアプリ'},
    {'path': 'llm/website_summarize.py', 'title': 'Webサイト要約'},
    {'path': 'llm/youtube_summarize.py', 'title': 'YouTube要約'},
    {'path': 'llm/pdf_upload_embedding.py', 'title': 'PDF要約'},
]

# Qdrant
QD_PATH = './storage/local'
QD_COLLECTION_NAME = 'my_collection'
