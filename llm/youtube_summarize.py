import streamlit as st
from llm.langchain.chat_models.OpenAi import OpenAi
from utils import const, helper
from utils.supabase.SubmitsTable import SubmitsTable
from views.common import app, debug

from langchain_community.document_loaders import YoutubeLoader
from langchain_core.documents import Document

app(title='Youtube Summarize')
st.markdown('**Youtube動画のURLを入力し、要約を行います。**')

client = SubmitsTable()
helper.api_call_limit(client=client, type=const.RequestType.YOUTUBE.value)

def get_document(url) -> list[Document]:
    with st.spinner("Fetching Content ..."):
        loader = YoutubeLoader.from_youtube_url(
            url,
            add_video_info=True,  # タイトルや再生数も取得できる
            language=['en', 'ja']  # 英語→日本語の優先順位で字幕を取得
        )
        return loader.load()  # Document

model = OpenAi()
llm = model.select_model()
output_text = None

container = st.container()
response_container = st.container()

with container:
    if url := st.text_input("Youtube URL: "):
        document = get_document(url)
        with st.spinner("ChatGPT is typing ..."):
            output_text, cb_handler = model.summarize(llm, document)
            client.logging_request(const.RequestType.YOUTUBE.value, document[0].page_content, output_text, cb_handler)

if output_text:
    with response_container:
        st.markdown("## Summary")
        st.write(output_text)
        st.markdown("---")
        st.markdown("## Original Text")
        st.write(document)

debug()
