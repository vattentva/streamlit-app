from typing import List
import streamlit as st
from llm.langchain.chat_models.OpenAi import OpenAi
from utils import const, helper
from utils.qdrant.QdrantBase import QdrantBase
from utils.supabase.SubmitsTable import SubmitsTable
from views.common import app, debug

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.retrieval_qa.base import (RetrievalQA, BaseRetrievalQA)

from qdrant_client import QdrantClient
from wordcloud import WordCloud
import matplotlib.pyplot as plt

app(title='PDF Upload & Embedding')

client = SubmitsTable()
helper.api_call_limit(client=client, type=const.RequestType.PDF.value)

# st.cache_resource.clear()
# @st.cache_resource
# def get_qd_client():
#     return QdrantClient(
#         path=const.QD_PATH,
#         # url='', api_key=''
#     )

def get_pdf_text() -> List[str]:
    if uploaded_file := st.file_uploader(label='PDFファイルを選択', type='pdf'):
        pdf_reader = PdfReader(uploaded_file)
        text = '\n\n'.join([page.extract_text() for page in pdf_reader.pages])
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name='text-embedding-ada-002',
            # 適切な chunk size は質問対象のPDFによって変わるため調整が必要
            # 大きくしすぎると質問回答時に色々な箇所の情報を参照することができない
            # 逆に小さすぎると一つのchunkに十分なサイズの文脈が入らない
            chunk_size=250,
            chunk_overlap=0,
        )
        return text_splitter.split_text(text)
    else:
        return None

def page_pdf_upload_and_build_vector_db():
    container = st.container()
    with container:
        pdf_text = get_pdf_text()
        if pdf_text:
            with st.spinner("Loading PDF ..."):
                qd = QdrantBase()
                vector_list = qd.add_texts(pdf_text)
                st.write(vector_list)

def build_qa_model(llm=None) -> BaseRetrievalQA:
    qd = QdrantBase()
    retriever = qd.get_retriever()

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever,
        return_source_documents=True,
        verbose=True        
    )

def page_ask_my_pdf():
    container = st.container()
    response_container = st.container()

    model = OpenAi()
    llm = model.select_model()

    with container:
        answer = None
        if query := st.text_input("Question: ", key="input"):
            qa = build_qa_model(llm)
            if qa:
                with st.spinner("ChatGPT is typing ..."):
                    answer, cb = model.question(qa, query)

        if answer:
            with response_container:
                st.markdown("### Answer")
                st.markdown(answer['result'])

                source = answer['source_documents']
                st.info(f"Note: Responses were generated from {len(source)} documents")
                st.write(source)

            client.logging_request(const.RequestType.PDF.value, query, answer['result'], cb)

def plot_wordcloud(texts: str):
    # ワードクラウドの生成
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        font_path='./Arial Unicode.ttf'
    ).generate(texts)

    # ワードクラウドをプロット
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")

    st.title("Word Cloud of Point Texts")
    st.pyplot(fig)

qd = QdrantBase()

selection = st.sidebar.radio("Go to", ["Upload", "Question", "Search"])
if selection == "Upload":
    st.header('PDFファイルのテキストをベクトルDBに保存')
    page_pdf_upload_and_build_vector_db()
elif selection == "Question":
    st.header("質問をする")
    page_ask_my_pdf()
elif selection == "Search":
    st.header('ベクトルDB検索')
    if name := st.selectbox("Select collection name:", [] + qd.get_collections()):
        word_list = [x.payload['page_content'] for x in qd.get_points()[0]]
        words = " ".join(word_list)
        plot_wordcloud(words)

        # st.info(qd.get_points()[1])
        # if word := st.text_input('検索単語'):
        #     st.write(qd.search(query=word))

debug()
