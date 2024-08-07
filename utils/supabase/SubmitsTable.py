from typing import Optional
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
        
