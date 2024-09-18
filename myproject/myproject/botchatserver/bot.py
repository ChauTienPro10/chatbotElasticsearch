import google.generativeai as genai
import json
from elasticSearch import retrieve_documents,format_results
# Configure the API key
genai.configure(api_key="AIzaSyBOmcgOscejzKVGg3sGIrELioWWxeeyUAg")

# Create the model with customized settings
generation_config = {
    "temperature": 0.7,  # Lower for more deterministic, concise answers
    "top_p": 0.9,        # Sampling parameter
    "top_k": 50,         # Number of options considered at each sampling step
    "max_output_tokens": 500,  # Adjust depending on the desired length of response
}

# Customize system behavior
system_instruction = """
You only answer the questions that have been prepared in Histoty, other questions answer "Tôi chưa có thông tin này"
"""

# Create the GenerativeModel with instructions
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=system_instruction,
)

# Start a chat session with initial history

with open('data.json', 'r', encoding='utf-8') as file:
    chat_data = json.load(file)


# Bắt đầu phiên trò chuyện với lịch sử từ data.json
chat_session = model.start_chat(history=chat_data["history"])

user_question = " Thầy Chau Duong Phat Tien?"
question1="tôi muốn luyện thi"
documents = retrieve_documents(user_question)
# print(format_results(documents))
if documents:
    relevant_info = "\n".join([doc["_source"].get("title") or doc["_source"].get("answer", "Không có tiêu đề hoặc tên") for doc in documents])
    system_response = f"Các thông tin liên quan: {relevant_info}"
    print(system_response)
    response=chat_session.send_message(user_question)
    print(response.text)
else:
    response = chat_session.send_message(user_question)
    print(response.text)

