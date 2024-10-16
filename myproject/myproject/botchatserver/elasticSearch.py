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
def retrieve_documents_course(query):
    response = es.search(
        index="course",  # Thay thế bằng tên chỉ mục của bạn
        body={
            "size": 1,  # Giới hạn số lượng tài liệu trả về
            "query": {
                "query_string": {
                    "query": query,
                    "fields": ["question","title","description"]  # Tìm kiếm trong các trường này
                }
            }
        }
    )
    return response['hits']['hits']

def retrieve_documents_teacher(query):
    response = es.search(
        index=["answer","teacher"], # Thay thế bằng tên chỉ mục của bạn
        body={
            "size": 1,  # Giới hạn số lượng tài liệu trả về
            "query": {
                "query_string": {
                    "query": query,
                    "fields": ["question","name","major"]  # Tìm kiếm trong các trường này
                }
            }
        }
    )
    return response['hits']['hits']


# định dạng kết quả cho tìm kím giáo viên
def format_results_teacher(documents):
    if not documents:
        return "Không tìm thấy tài liệu nào phù hợp với yêu cầu của bạn."
    doc = documents[0]
    source = doc['_source']
    formatted_results={
            "type":"teacher",
            "name": source.get('name','Không tìm thấy'),
            "major": source.get('major','không tìm thấy'),
            "level":source.get('level','không tìm thấy')
        }
    return json.dumps(formatted_results, ensure_ascii=False)

# Định dạng kết quả tìm kiếm
def format_results_course(documents):
    if not documents:
        return "Không tìm thấy tài liệu nào phù hợp với yêu cầu của bạn."
    
    doc = documents[0]
    source = doc['_source']
    title = source.get('title', 'Tiêu đề không có')
    description = source.get('description', 'Mô tả không có')
    price=source.get('price','')
    duration=source.get('duration','')
    teacherId=source.get('teacher','')
    level=source.get('level','')
    id=doc['_id']
    teacherInfor = (es.get(index="teacher", id=teacherId))['_source']  
    teacher=teacherInfor.get('name','')
    formatted_results={
            "type":"course",
            "title": title,
            "description": description,
            "id":id,
            "price":price,
            "duration": duration,
            "teacher":teacher,
            "level":level
        }

    # rep = 'Có phải bạn muốn tìm khóa học '
    
    # Lặp qua từng khóa học trong danh sách và nối tiêu đề bằng "hoặc"
    # rep += ' hoặc '.join([rs['title'] and rs['id'] for rs in formatted_results])

    return json.dumps(formatted_results, ensure_ascii=False)


query = " hóa học luyện thi 8 điểm"
documents = retrieve_documents_course(query)

# In kết quả được định dạng
formatted_output = format_results_course(documents)
print(formatted_output)
