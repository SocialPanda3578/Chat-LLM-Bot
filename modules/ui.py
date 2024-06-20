import gradio as gr

from modules import (
    chat,
    prompt
)

# 当前布局的组件
gradio_components = {}

# llm 大模型列表
models = ["QianFan", "Spark-3.5"]

# AI 角色列表
roles = ["诗人", "厨师", "IT 专家"]


# 创建界面 ui
def create_ui():
    # 行布局
    with gr.Row():
        # 左侧对话框部分
        with gr.Column(scale=4):
            # 对话框，定义高度为 500
            gradio_components['chatbot'] = gr.Chatbot(height=500)

            # 下方的文本输入框和提交按钮
            with gr.Row():
                # 文本输入框
                gradio_components['bot_message'] = gr.Textbox(show_label=False, container=False,
                                                              placeholder="输入提问...", scale=5)
                # 提交按钮
                gradio_components['submit_btn'] = gr.Button("Submit", variant="primary", scale=1)
                # 清除按钮
                gradio_components['clear_btn'] = gr.ClearButton([gradio_components['chatbot']], scale=1)

        # 右侧配置部分
        with gr.Column(scale=1):
            # 模型下拉列表
            gradio_components['models'] = gr.Dropdown(choices=models, label="模型")
            # 温度配置，滑动条
            gradio_components['temperature'] = gr.Slider(minimum=0, maximum=2, value=0.3, step=0.1, label="Temperature")
            # prompt 角色选项
            gradio_components['prompt_radio'] = gr.Radio(roles, label="AI 角色", info="请选择你想要的 AI 角色")
            # 对应的角色系统提示词，默认不显示
            gradio_components['prompt_text'] = gr.Textbox(lines=10, label="角色系统提示词", visible=False)


# 绑定组件事件
def bind_event_handlers():

    # 模型切换
    gradio_components['models'].change(
        model_change, # 处理模型下拉列表切换
        inputs=gradio_components['models'],
        outputs=[gradio_components['chatbot']])

    # 提交按钮点击
    gradio_components['submit_btn'].click(
        submit_check,  # 校验函数
        inputs=[gradio_components['models'], gradio_components['bot_message']],
        outputs=[gradio_components['submit_btn'], gradio_components['clear_btn']]
    ).success(  # 校验成功
        add_text,  # 添加用户消息到对话框
        inputs=[gradio_components['bot_message'],
                gradio_components['chatbot']],
        outputs=[gradio_components['bot_message'],
                 gradio_components['chatbot']],
        queue=False
    ).then(  # 添加成功后，调用对话函数
        chat.bot,
        inputs=[gradio_components['chatbot'], gradio_components['models'], gradio_components['temperature'], gradio_components['prompt_text']],
        outputs=[gradio_components['chatbot']]
    ).success(  # 对话成功后，更新按钮状态
        lambda: [gr.update(value="Submit", interactive=True), gr.update(interactive=True)], None,
        [gradio_components['submit_btn'], gradio_components['clear_btn']]
    )

    # AI 角色切换
    gradio_components['prompt_radio'].change(
        prompt_radio_select,
        # 输入单选框内容
        inputs=[gradio_components['prompt_radio']],
        # 输出提示词到文本框
        outputs=[gradio_components['prompt_text']]
    )


# 模型切换事件
def model_change(model_name):
    print('model_change', model_name)
     # 清空对话框内容
    return gr.update(value=None)


# 提交按钮检测
def submit_check(model_name, message):
    if len(model_name) == 0:
        raise gr.Error("请先选择一个模型")

    if len(message) == 0:
        raise gr.Error("请输入提问内容")

    # 设置提交按钮和清除按钮不能点击状态
    return gr.update(value="Running", interactive=False), gr.update(interactive=False)


# 添加用户消息到对话框
def add_text(user_message, history):
    history = history or []
    # 同时清空输入框的内容
    return "", history + [[user_message, None]]


# 单选按钮选择
def prompt_radio_select(role):
    # 引用 prompt 模块的方法获取角色对应的提示词
    prompt_text = prompt.get_prompt(role)
    # 更新 prompt 文本框内容可见，并更新其内容
    return gr.update(visible=True, value=prompt_text)