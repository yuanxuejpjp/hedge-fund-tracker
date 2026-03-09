# 🚀 Render 部署指南

## 📋 项目说明

本项目是对冲基金持仓追踪系统的 Streamlit Web 版本，数据来源于 SEC EDGAR 13F 报告。

## 📁 关键文件

- `app.py` - Streamlit 主应用
- `requirements.txt` - Python 依赖
- `render.yaml` - Render 部署配置
- `database/` - 数据文件目录

## 🚀 部署步骤

### 1. 推送代码到 GitHub

```bash
git add app.py requirements.txt render.yaml DEPLOY.md
git commit -m "添加 Streamlit Web 界面和 Render 配置"
git push
```

### 2. 在 Render 上部署

1. 访问 https://dashboard.render.com
2. 点击 "New +" → "Web Service"
3. 选择你的 GitHub 仓库
4. 填写配置：
   - **Name**: hedge-fund-tracker（或其他名称）
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. 点击 "Create Web Service"

### 3. 等待部署完成

- 首次部署约需 2-3 分钟
- 部署完成后会显示访问链接

## 📊 功能特点

- 📈 **基金持仓分析** - 查看197+家对冲基金持仓
- 🔥 **热门股票追踪** - 发现被多家基金看好的股票
- 📊 **行业分布分析** - 了解基金行业配置偏好
- 🔄 **季度对比** - 追踪基金增减持变化

## ⚠️ 注意事项

1. **免费版限制**：
   - 实例会在15分钟不活动后休眠
   - 首次访问可能需要30秒唤醒

2. **数据更新**：
   - 数据存储在GitHub仓库中
   - 原项目的GitHub Actions会自动更新数据
   - 需要定期pull最新数据并重新部署

## 🔧 环境变量

无需额外配置环境变量即可运行。
