import qianfan

import sys
import os
from dotenv import load_dotenv, find_dotenv

# 防止相对路径导入出错
sys.path.append(os.path.join(os.path.dirname(__file__)))

load_dotenv(find_dotenv('.env'))


class QianfanLlmEngine:

    def __init__(
            self,
    ):
        # 初始化模型，并输入对应的 API KEY 信息
        self.llm = qianfan.ChatCompletion(ak=os.getenv("QIANFAN_AK"), sk=os.getenv("QIANFAN_SK"))

    def chat(
            self,
            history, # 聊天记录
            model_name: str = "ERNIE-Speed-128k", # 默认使用 ERNIE-Bot-turbo 模型
            temperature: float = 0.3,
            prompt: str = "" # 提示词
    ):

        chat_history = []

        # 调整为 qianfan 对话消息结构
        if len(history):
            for his in history:
                # history 最后一条记录为 add_text 函数添加的消息，其中 his[0] 为用户提交的消息，his[1] 为 None
                if his[1] is None:
                    content = his[0]
                    # 如果界面有传入 prompt 提示词，则拼接到提问内容中
                    if len(prompt):
                        # 只有当第一次聊天时才整合 prompt 提示词
                        if len(history) == 1:
                            content = prompt + ' 我的第一个请求是：' + content
                    user_message = {"content": content, "role": "user"}
                    chat_history.append(user_message)
                else:
                    # 数组中的其余部分则为聊天记录
                    user_message = {"content": his[0], "role": "user"}
                    chat_history.append(user_message)

                    model_message = {"content": his[1], "role": "assistant"}
                    chat_history.append(model_message)

        print('chat_history', chat_history)

        response = self.llm.do(model=model_name, messages=chat_history, temperature=temperature, stream=True)
        # 将最后一条记录 his[1] 为 None 的值设置为空字符串
        history[-1][1] = ""
        for chunk in response:
            # 并将返回的流数据添加其中
            history[-1][1] += chunk['body']['result']
            # 返回整个聊天记录数组
            yield history