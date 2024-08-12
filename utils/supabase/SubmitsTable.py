import streamlit as st
from datetime import datetime, timedelta
from utils.supabase.SupabaseClient import SupabaseClient
from langchain_community.callbacks.openai_info import OpenAICallbackHandler

class SubmitsTable(SupabaseClient):
    def __init__(self):
        super().__init__('submits')

    def logging_request(
            self,
            type: int,
            prompt: str,
            response: str,
            callback_handler: OpenAICallbackHandler,
        ):
        """
        submitsテーブルにAPIリクエストのログを記録
        """
        return self.insert_data({
            'type': type,
            'prompt': prompt,
            'response': response,
            'user_name': st.session_state.get('name', ''),
            'is_success': True if response else False,
            'total_cost': callback_handler.total_cost,
            'prompt_tokens': callback_handler.prompt_tokens,
            'completion_tokens': callback_handler.completion_tokens,
        })
    
    def select_usage_count(self, type: int):
        start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        response = (
            self.get_client()
            .select("count", count="exact")
            .eq("type", str(type))
            .eq("user_name", st.session_state.name)
            .eq("is_success", True)
            .gte("created_at", start_of_day.isoformat())
            .lt("created_at", end_of_day.isoformat())
            .execute()
        )
        return response.count        
