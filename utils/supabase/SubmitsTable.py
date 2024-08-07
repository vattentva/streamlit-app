import streamlit as st
from datetime import datetime, timedelta
from utils.supabase.SupabaseClient import SupabaseClient

class SubmitsTable(SupabaseClient):
    def __init__(self):
        super().__init__('submits')

    def insert_prompt(
            self,
            type: int,
            prompt: str,
            response: str,
            user_name: str,
            is_success: bool,
            total_cost: float,
            prompt_tokens: int,
            completion_tokens: int,
        ):
        """submitsテーブルに新しいプロンプトを挿入する"""
        return self.insert_data({
            'type': type,
            'prompt': prompt,
            'response': response,
            'user_name': user_name,
            'is_success': is_success,
            'total_cost': total_cost,
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
        })
    
    def select_usage_count(self):
        start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        response = (
            self.get_client()
            .select("count", count="exact")
            .eq("type", "2")
            .eq("user_name", st.session_state.name)
            .eq("is_success", True)
            .gte("created_at", start_of_day.isoformat())
            .lt("created_at", end_of_day.isoformat())
            .execute()
        )
        return response.count        
