import os
import streamlit as st
import torch
from transformers import AutoModel, AutoTokenizer
import tcvectordb
from tcvectordb.model.document import Document, Filter, SearchParams

# 使用绝对路径，指向模型文件所在的目录
MODEL_PATH = 'Crawling_VectorDB_LLM/chatglm3-6b'
TOKENIZER_PATH = MODEL_PATH  # 分词器路径通常与模型路径相同

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# 检查路径是否存在
if not os.path.exists(MODEL_PATH):
    raise OSError(f"Model path does not exist: {MODEL_PATH}")

# 设置页面标题、图标和布局
st.set_page_config(
    page_title="我的AI知识库",
    page_icon=":robot:",
    layout="wide"
)

# 搜索函数定义
def searchTvdb(txt):
    conn_params = {
        'url':'http://lb-340v4o4i-9of4pnthr82vg3uc.clb.ap-guangzhou.tencentclb.com:50000',
        'key':'38k1Sgm1MWI1vlLe0eTR5SGPkDY9ZP0GL0u7LCkw',
        'username':'root',
        'timeout':20
        }

    vdb_client = tcvectordb.VectorDBClient(
            url=conn_params['url'],
            username=conn_params['username'],
            key=conn_params['key'],
            timeout=conn_params['timeout'],
        )
    db = vdb_client.database('crawlingdb')
    coll = db.collection('tencent_knowledge')
    embeddingItems = [txt]
    search_by_text_res = coll.searchByText(embeddingItems=embeddingItems,limit=3, params=SearchParams(ef=100))
    return search_by_text_res.get('documents')

# 将列表转换为字符串
def listToString(doc_lists):
    str = ""
    for i, docs in enumerate(doc_lists):
        for doc in docs:
            str += doc["text"]
    return str

# 加载ChatGLM模型和分词器
@st.cache_resource
def get_model():
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, trust_remote_code=True)
    model = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True)
    model = model.to(DEVICE).eval()
    return tokenizer, model

# 初始化模型
tokenizer, model = get_model()

# 初始化会话状态
if "history" not in st.session_state:
    st.session_state.history = []
if "past_key_values" not in st.session_state:
    st.session_state.past_key_values = None

# 对话模式切换函数
def on_mode_change():
    mode = st.session_state.dialogue_mode
    text = f"已切换到 {mode} 模式。"
    st.session_state.history = []
    st.session_state.past_key_values = None
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    st.toast(text)

# 设置对话模式选择
dialogue_mode = st.sidebar.selectbox(
    "请选择对话模式",
    ["腾讯云知识库对话", "正常LLM对话(支持历史)"],
    on_change=on_mode_change,
    key="dialogue_mode"
)

# 设置模型生成参数
max_length = st.sidebar.slider("max_length", 0, 32768, 8000, step=1)
top_p = st.sidebar.slider("top_p", 0.0, 1.0, 0.8, step=0.01)
temperature = st.sidebar.slider("temperature", 0.0, 1.0, 0.8, step=0.01)

# 清理会话历史按钮
buttonClean = st.sidebar.button("清理会话历史", key="clean")
if buttonClean:
    st.session_state.history = []
    st.session_state.past_key_values = None
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    st.rerun()

# 渲染聊天历史记录
for i, message in enumerate(st.session_state.history):
    if message["role"] == "user":
        with st.chat_message(name="user", avatar="user"):
            st.markdown(message["content"])
    else:
        with st.chat_message(name="assistant", avatar="assistant"):
            st.markdown(message["content"])

# 输入框和输出框
with st.chat_message(name="user", avatar="user"):
    input_placeholder = st.empty()
with st.chat_message(name="assistant", avatar="assistant"):
    message_placeholder = st.empty()

# 获取用户输入
prompt_text = st.chat_input("请输入您的问题")

# 处理用户输入并生成回复
if prompt_text:
    mode = st.session_state.dialogue_mode
    template_data = ""

    if mode == "腾讯云知识库对话":
        result = searchTvdb(prompt_text)
        str_data = listToString(result)
        template_data = f"请按照\"{prompt_text}\"进行总结,内容是：{str_data[:20000]}"
    else:
        template_data = prompt_text

    input_placeholder.markdown(prompt_text)
    history = st.session_state.history
    past_key_values = st.session_state.past_key_values
    history = []

    # 更新 stream_chat 调用，添加 device 参数
    for response, history, past_key_values in model.stream_chat(
        tokenizer,
        template_data,
        history,
        past_key_values=past_key_values,
        max_length=max_length,
        top_p=top_p,
        temperature=temperature,
        return_past_key_values=True,
        device=DEVICE  # 添加此参数
    ):
        message_placeholder.markdown(response)

    if mode != "腾讯云知识库对话":
        st.session_state.history = history
        st.session_state.past_key_values = past_key_values
    else:
        endString = ""
        for doc in result[0]:
            endString += f"\n\n{doc['title']}     {doc['id']}"
        response += f"\n\n参考链接：\n\n\n{endString}"
    message_placeholder.markdown(response)
