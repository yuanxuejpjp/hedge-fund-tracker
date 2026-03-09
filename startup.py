"""
启动脚本 - 用于 Render 部署
"""
import os
import sys

# 设置 Streamlit 环境变量
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_ENABLECORS'] = 'false'
os.environ['STREAMLIT_BROWSER_GATHERUSAGESTATS'] = 'false'

# 获取端口
port = os.environ.get('PORT', '8501')

# 启动 Streamlit
cmd = f"streamlit run app.py --server.port={port} --server.address=0.0.0.0 --server.headless=true"
print(f"Starting: {cmd}")
os.system(cmd)
