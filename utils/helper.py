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
