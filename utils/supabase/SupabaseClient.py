import streamlit as st
from supabase import create_client, Client

class SupabaseClient:
    def __init__(self, table_name: str):
        # SupabaseのURLとAPIキーを設定
        self.url: str = st.secrets['SUPABASE_URL']
        self.key: str = st.secrets['SUPABASE_KEY']
        self.table_name = table_name
        self.client: Client = create_client(self.url, self.key)

    def select_all(self):
        """テーブルから全てのデータを選択して返す"""
        try:
            response = self.client.table(self.table_name).select("*").execute()
            return response.data
        except Exception as e:
            st.error(f"Error selecting data from {self.table_name}: {e}")
            return None

    def insert_data(self, data: dict):
        """テーブルにデータを挿入する"""
        try:
            response = self.client.table(self.table_name).insert(data).execute()
            return response.data
        except Exception as e:
            st.error(f"Error inserting data into {self.table_name}: {e}")
            return None
