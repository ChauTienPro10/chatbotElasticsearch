from elasticsearch import Elasticsearch
import json

# Kết nối đến Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

# Kiểm tra kết nối
if es.ping():
    print("Elasticsearch is connected!")
else:
    print("Elasticsearch connection failed.")

# Tìm kiếm video với tiêu đề hoặc mô tả chứa từ khóa
def retrieve_documents(query):
    response = es.search(
        index="answer",  # Thay thế bằng tên chỉ mục của bạn
        body={
            "size": 5,  # Giới hạn số lượng tài liệu trả về
            "query": {
                "query_string": {
                    "query": query,
                    "fields": ["question"]  # Tìm kiếm trong các trường này
                }
            }
        }
    )
    return response['hits']['hits']

# Định dạng kết quả tìm kiếm
def format_results(documents):
    if not documents:
        return "Không tìm thấy tài liệu nào phù hợp với yêu cầu của bạn."
    
    formatted_results = []
    for doc in documents:
        source = doc['_source']
        title = source.get('title', 'Tiêu đề không có')
        description = source.get('description', 'Mô tả không có')
        course=source.get('course','khong co khoa hoc')
        formatted_results.append({
            # "Tiêu đề": title,
            # "Mô tả": description,
            # "Khóa học":course
            
        })

    return json.dumps(formatted_results, indent=4, ensure_ascii=False)


query = "Chau Duong"
documents = retrieve_documents(query)

# In kết quả được định dạng
formatted_output = format_results(documents)
print(documents)
