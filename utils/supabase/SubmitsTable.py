from utils.supabase.SupabaseClient import SupabaseClient

class SubmitsTable(SupabaseClient):
    def __init__(self):
        super().__init__('submits')

    def insert_prompt(self, type: int, prompt: str, user_name: str, is_success: bool):
        """submitsテーブルに新しいプロンプトを挿入する"""
        data = {
            'type': type,
            'prompt': prompt,
            'user_name': user_name,
            'is_success': is_success,
        }
        return self.insert_data(data)
