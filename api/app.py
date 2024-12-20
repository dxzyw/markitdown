from flask import Flask
from seo import seo
import os

app = Flask(__name__,template_folder="../templates", static_folder="../static")

# 配置
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'your-secret-key'),
    MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 限制上传文件大小为16MB
)

# 注册蓝图
app.register_blueprint(seo)

# 导入视图
from views import *

if __name__ == '__main__':
    # 确保上传目录存在
    os.makedirs('uploads', exist_ok=True)
    
    # 启动应用
    app.run(debug=True) 