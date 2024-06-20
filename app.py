import gradio as gr

# 引入模块脚本
from modules import (
    ui,
)

# 使用 Blocks 布局
with gr.Blocks() as demo:

    # markdown 组件
    gr.Markdown(
        """
        # AI 聊天机器人
        选择一个 LLM 模型来聊天
        """
    )

    # 创建 ui 界面
    ui.create_ui()
    # 绑定组件事件
    ui.bind_event_handlers()

# 启动入口
if __name__ == "__main__":
    # 启动排队
    demo.queue()
    demo.launch()