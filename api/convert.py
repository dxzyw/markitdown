from http.server import BaseHTTPRequestHandler
import json
from markitdown import MarkItDown

def process_file(file_content, file_type):
    md = MarkItDown()
    result = md.convert(file_content)
    return result.text_content

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 获取内容长度
        content_length = int(self.headers['Content-Length'])
        # 读取请求体
        post_data = self.rfile.read(content_length)
        
        try:
            # 处理文件
            result = process_file(post_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "success": True,
                "markdown": result
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "success": False,
                "error": str(e)
            }
            self.wfile.write(json.dumps(response).encode())
