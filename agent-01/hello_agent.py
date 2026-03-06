from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek


load_dotenv()

# -------------------------------
# 1. 定义一个简单的“工具” —— 让Agent有能力“行动”
# -------------------------------
@tool
def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

@tool
def get_mood() -> str:
    """随机返回今天的心情（模拟外部环境感知）"""
    import random
    moods = ["超级开心", "有点疲惫但还行", "元气满满", "哲学模式启动"]
    return random.choice(moods)

tools = [get_current_time, get_mood]

# -------------------------------
# 2. 创建大模型
# -------------------------------
llm = ChatDeepSeek(model="deepseek-chat", temperature=0.7)

system_prompt = """你是一个有个性、活泼的AI助手。
现在你要用最有趣、最符合当前时间和心情的方式向主人问好。
可以调用工具获取时间和心情来增加趣味性。
语气要自然，像真人朋友一样。"""

# -------------------------------
# 3. 创建Agent
# -------------------------------
from langgraph.prebuilt import create_react_agent as create_react_agent_v1
agent_executor = create_react_agent_v1(llm, tools, prompt=system_prompt)

# -------------------------------
# 4. 运行！
# -------------------------------
response = agent_executor.invoke({"messages": [{"role": "user", "content": "现在向我打个招呼吧！"}]})

print("\n最终回答：")
print(response["messages"][-1].content)

