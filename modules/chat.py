from models.qianfan import QianfanLlmEngine


# 聊天，适配不同的模型对话
def bot(history, model_name, temperature, prompt):
    if model_name == "QianFan":
        qianfanModel = QianfanLlmEngine()

        # 可迭代的 generator（生成器）对象
        for history_chunk in qianfanModel.chat(history=history, temperature=temperature, prompt=prompt):
            yield history_chunk