"""
对冲基金持仓追踪系统
数据来源：SEC EDGAR 13F 报告
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="对冲基金持仓追踪",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_funds_list():
    """加载基金列表"""
    df = pd.read_csv('database/hedge_funds.csv')
    return df

@st.cache_data
def load_fund_data(quarter, fund_name):
    """加载特定基金的持仓数据"""
    file_path = f'database/{quarter}/{fund_name}.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    return None

@st.cache_data
def get_all_quarters():
    """获取所有季度目录"""
    quarters = []
    for item in os.listdir('database'):
        if item.startswith('20') and os.path.isdir(f'database/{item}'):
            quarters.append(item)
    return sorted(quarters, reverse=True)

def render_header():
    """渲染头部"""
    st.markdown('<div class="main-header">📊 对冲基金持仓追踪系统</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">追踪全球顶级对冲基金的持仓动向 | 数据来源：SEC EDGAR 13F</div>', unsafe_allow_html=True)

def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.title("🔍 导航菜单")
        
        page = st.radio(
            "选择功能",
            ["🏠 首页", "📈 基金持仓", "🔥 热门股票", "📊 行业分析", "ℹ️ 关于系统"]
        )
        
        st.divider()
        
        # 季度选择
        quarters = get_all_quarters()
        selected_quarter = st.selectbox("📅 选择季度", quarters, index=0)
        
        st.divider()
        
        # 数据说明
        st.info("""
        **数据说明**
        - 来源：SEC EDGAR 13F 报告
        - 更新：季度更新
        - 延迟：45天
        """)
        
        return page, selected_quarter

def render_home():
    """渲染首页"""
    st.markdown("""
    ## 🎯 欢迎来到对冲基金持仓追踪系统
    
    这是一个追踪全球顶级对冲基金持仓动向的数据平台。
    
    ### 📈 功能特点
    
    - 📊 **基金持仓分析** - 查看各对冲基金的最新持仓情况
    - 🔥 **热门股票追踪** - 发现被多家基金同时看好的股票
    - 📊 **行业分布分析** - 了解对冲基金的行业配置偏好
    - 🔄 **季度对比** - 追踪基金的增减持变化
    
    ### 🏢 覆盖基金
    
    系统覆盖 **197+** 家顶级对冲基金，包括：
    - Renaissance Technologies (文艺复兴科技)
    - Bridgewater Associates (桥水基金)
    - Pershing Square (潘兴广场)
    - 等更多知名机构
    
    ### ⚠️ 免责声明
    本网站提供的数据仅供参考，不构成投资建议。投资有风险，入市需谨慎。
    """)
    
    # 显示统计信息
    st.subheader("📊 数据统计")
    
    quarters = get_all_quarters()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📁 季度数据", len(quarters))
    with col2:
        funds = load_funds_list()
        st.metric("🏢 对冲基金", len(funds))
    with col3:
        # 计算总持仓数
        total_holdings = 0
        if quarters:
            latest_quarter = quarters[0]
            quarter_path = f'database/{latest_quarter}'
            if os.path.exists(quarter_path):
                total_holdings = len([f for f in os.listdir(quarter_path) if f.endswith('.csv')])
        st.metric("📈 持仓报告", total_holdings)

def render_fund_holdings(quarter):
    """渲染基金持仓页面"""
    st.header(f"📈 基金持仓分析 - {quarter}")
    
    # 加载基金列表
    funds_df = load_funds_list()
    
    # 基金选择
    fund_names = [f.replace('.csv', '') for f in os.listdir(f'database/{quarter}') if f.endswith('.csv')]
    fund_names = sorted(fund_names)
    
    if not fund_names:
        st.warning("该季度暂无数据")
        return
    
    selected_fund = st.selectbox("选择基金", fund_names, format_func=lambda x: x.replace('_', ' '))
    
    if selected_fund:
        # 加载数据
        data = load_fund_data(quarter, selected_fund)
        
        if data is not None and not data.empty:
            # 显示基金信息
            fund_info = funds_df[funds_df['Fund'] == selected_fund]
            if not fund_info.empty:
                manager = fund_info.iloc[0].get('Manager', 'N/A')
                st.subheader(f"🏢 {selected_fund.replace('_', ' ')} | 基金经理: {manager}")
            
            # 关键指标
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 持仓数量", len(data))
            with col2:
                if 'Value' in data.columns:
                    # 解析市值
                    total_value = 0
                    for val in data['Value']:
                        if isinstance(val, str):
                            if 'M' in val:
                                total_value += float(val.replace('M', '').replace('$', ''))
                            elif 'B' in val:
                                total_value += float(val.replace('B', '').replace('$', '')) * 1000
                    st.metric("💰 总持仓市值", f"${total_value:.0f}M")
            with col3:
                if 'Portfolio%' in data.columns:
                    max_weight = data['Portfolio%'].str.replace('%', '').astype(float).max()
                    st.metric("🎯 最大权重", f"{max_weight:.1f}%")
            
            st.divider()
            
            # 持仓表格
            st.subheader("📋 详细持仓")
            
            # 格式化显示
            display_df = data.copy()
            if 'Company' in display_df.columns:
                display_df['Company'] = display_df['Company'].str.title()
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                height=500
            )
            
            # 权重分布图
            st.subheader("📊 持仓权重分布")
            
            if 'Portfolio%' in data.columns and 'Ticker' in data.columns:
                top10 = data.nlargest(10, data['Portfolio%'].str.replace('%', '').astype(float))
                
                fig = px.pie(
                    top10,
                    values=top10['Portfolio%'].str.replace('%', '').astype(float),
                    names='Ticker',
                    title=f"前10大持仓 - {selected_fund.replace('_', ' ')}"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("无法加载该基金的持仓数据")

def render_hot_stocks(quarter):
    """渲染热门股票页面"""
    st.header(f"🔥 热门股票追踪 - {quarter}")
    
    # 加载所有基金的持仓
    all_holdings = []
    fund_names = [f.replace('.csv', '') for f in os.listdir(f'database/{quarter}') if f.endswith('.csv')]
    
    for fund in fund_names:
        data = load_fund_data(quarter, fund)
        if data is not None and not data.empty and 'Ticker' in data.columns:
            for _, row in data.iterrows():
                all_holdings.append({
                    'Fund': fund,
                    'Ticker': row.get('Ticker', 'N/A'),
                    'Company': row.get('Company', 'N/A'),
                    'Value': row.get('Value', 'N/A'),
                    'Delta': row.get('Delta', 'N/A')
                })
    
    if all_holdings:
        df = pd.DataFrame(all_holdings)
        
        # 统计热门股票
        hot_stocks = df.groupby('Ticker').agg({
            'Fund': 'count',
            'Company': 'first'
        }).reset_index()
        hot_stocks.columns = ['Ticker', '基金数量', '公司名称']
        hot_stocks = hot_stocks.sort_values('基金数量', ascending=False).head(20)
        
        st.subheader("🏆 最受关注的20只股票")
        st.dataframe(hot_stocks, use_container_width=True, hide_index=True)
        
        # 可视化
        fig = px.bar(
            hot_stocks.head(10),
            x='Ticker',
            y='基金数量',
            title='热门股票TOP10（被多少家基金持有）'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("暂无数据")

def render_sector_analysis(quarter):
    """渲染行业分析页面"""
    st.header(f"📊 行业分析 - {quarter}")
    st.info("行业分析功能需要GICS分类数据支持，正在开发中...")

def render_about():
    """渲染关于页面"""
    st.header("ℹ️ 关于系统")
    
    st.markdown("""
    ### 📊 对冲基金持仓追踪系统
    
    这是一个追踪全球顶级对冲基金持仓动向的数据平台。
    
    #### 📈 数据来源
    - **SEC EDGAR 13F 报告** - 季度披露的对冲基金持仓
    - **自动更新** - 通过GitHub Actions自动抓取最新数据
    
    #### 🏢 覆盖基金
    系统覆盖全球 **197+** 家顶级对冲基金。
    
    #### ⚠️ 数据说明
    - **13F报告**：季度更新，有45天延迟
    - **数据范围**：只包含美股多头持仓
    - **不包含**：空头、衍生品、非美股资产
    
    #### 💡 使用建议
    - 对冲基金持仓可以作为投资参考
    - 注意披露延迟（实际交易比报告早1.5-2个月）
    - 不要盲从，要有自己的判断
    
    #### 📧 联系我们
    如有问题或建议，欢迎反馈。
    """)

def main():
    """主函数"""
    render_header()
    page, selected_quarter = render_sidebar()
    
    if page == "🏠 首页":
        render_home()
    elif page == "📈 基金持仓":
        render_fund_holdings(selected_quarter)
    elif page == "🔥 热门股票":
        render_hot_stocks(selected_quarter)
    elif page == "📊 行业分析":
        render_sector_analysis(selected_quarter)
    elif page == "ℹ️ 关于系统":
        render_about()
    
    # 页脚
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>📊 对冲基金持仓追踪系统 | 数据来源：SEC EDGAR</p>
        <p style="font-size: 0.8rem;">⚠️ 免责声明：本网站仅供学习研究使用，不构成投资建议</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
