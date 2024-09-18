def handle_string(_text):
    if not _text or _text=='':
        return None
    
    if _text.length > 100:
        return "câu hỏi của bạn quá dài!"
    else:
        return _text