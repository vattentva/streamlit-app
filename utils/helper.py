import streamlit as st

from utils.supabase.SubmitsTable import SubmitsTable
from utils.supabase.SupabaseClient import SupabaseClient

def api_call_limit(client: SubmitsTable, type: int):
    """
    API呼び出しの制限数を超えた場合の処理
    """
    MAX_CALLS = st.secrets.get('MAX_CALLS', 5)
    today_call_count = client.select_usage_count(type)
    with st.sidebar:
        st.info(f"Usage: {today_call_count} / {MAX_CALLS}")
    if today_call_count > MAX_CALLS:
        st.info("使用回数が制限を超えました。")
        st.stop()

def split_text(text: str) -> str:
    """
    日本語の文末区切りで改行する
    """
    special_words = ["ます。", "ました。", "です。", "でした。"]
    # 結果を格納するリスト
    result = []
    buffer = ""
    
    for char in text:
        buffer += char
        if char == ' ':
            result.append(buffer.strip())
            buffer = ""
        elif any(buffer.endswith(special_word) for special_word in special_words):
            result.append(buffer.strip())
            buffer = ""

    if buffer:
        result.append(buffer.strip())
    
    result_text = '\n'.join(result)
    return result_text
