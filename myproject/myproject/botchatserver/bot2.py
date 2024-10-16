import json
import google.generativeai as genai
import os
from .elasticSearch import format_results_course,retrieve_documents_course,retrieve_documents_teacher,format_results_teacher
os.chdir(r'.\myproject\botchatserver')
file_path = os.path.join( 'data.json')
# Cấu hình API key
genai.configure(api_key="AIzaSyBOmcgOscejzKVGg3sGIrELioWWxeeyUAg")

# Cấu hình model
generation_config = {
  "temperature": 0.1,  # Giảm nhiệt độ để mô hình ít sáng tạo hơn
  "top_p": 0.9,
  "top_k": 50,
  "max_output_tokens": 500,
}

# Thêm hướng dẫn hệ thống để chỉ trả lời dựa trên lịch sử
system_instruction = """
Bạn là trợ lý AI và chỉ được trả lời dựa trên các câu trả lời có sẵn trong lịch sử chat. 
Bạn không được trả lời quá 50 ký tự.
Nếu không có câu trả lời phù hợp, hãy trả lời: "Tôi không thể trả lời vấn đề của bạn."
"""

# Tạo mô hình với hướng dẫn hệ thống
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction=system_instruction,
)

# Đọc lịch sử từ tệp data.json
with open(file_path, 'r', encoding='utf-8') as file:
    chat_data = json.load(file)
# Bắt đầu phiên trò chuyện với lịch sử từ data.json
chat_session = model.start_chat(history=chat_data["history"])

# Gửi câu hỏi
require_question="Hãy cho biết mục đích của câu hỏi sau liên quan đến chủ đề khóa học hay chủ đề giáo viên hay chủ đề khuyến mãi bạn chỉ cần trả lời 'course' hoặc 'teacher' hoặc 'sales'. nếu không có chủ đề nào liên quan hãy trả lời 'no topic':"
user_question =  "'hiện có mã giảm giá nào?' "
# response = chat_session.send_message(require_question+' '+user_question)

# # In ra kết quả phản hồi
# print(response.text)


def handle_string(_text):
    if not _text or _text=='':
        return None
    
    if len(_text) > 100:
        return "câu hỏi của bạn quá dài!"
    else:
        res=chat_session.send_message(require_question+' '+_text)
        return res.text
    

def answer(question,topic):
    if(topic=='no topic'):
        res=chat_session.send_message(question)
        return json.dumps({"title":res.text}, ensure_ascii=False)
    else:
        if (topic=='course'):
            documents=retrieve_documents_course(question)
            formatted_output = format_results_course(documents)
            return formatted_output
        elif(topic=='teacher'):
            documents=retrieve_documents_teacher(question)
            formatted_output = format_results_teacher(documents)
            return formatted_output
        else:
            return json.dumps({"title":topic}, ensure_ascii=False)
