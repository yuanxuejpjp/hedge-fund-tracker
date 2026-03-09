#!/usr/bin/env python3
"""
启动脚本 - 用于 Render 部署
"""
import os
import sys
import subprocess

# 设置环境变量
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_ENABLECORS'] = 'false'
os.environ['STREAMLIT_BROWSER_GATHERUSAGESTATS'] = 'false'
os.environ['STREAMLIT_SERVER_PORT'] = os.environ.get('PORT', '8501')

# 启动 Streamlit
print("Starting Streamlit app...")
print(f"PORT: {os.environ.get('PORT', '8501')}")

subprocess.run([
    sys.executable, '-m', 'streamlit', 'run', 'app.py',
    '--server.port', os.environ.get('PORT', '8501'),
    '--server.address', '0.0.0.0',
    '--server.headless', 'true'
])
