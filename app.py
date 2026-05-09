import os
from openai import OpenAI
from flask import Flask, request, render_template_string

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>课堂内容智能整理助手</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, "Microsoft YaHei", sans-serif;
            background: #f4f7fb;
            color: #222;
        }
        .container {
            width: 880px;
            margin: 45px auto;
            background: white;
            padding: 36px;
            border-radius: 18px;
            box-shadow: 0 8px 22px rgba(0,0,0,0.08);
        }
        h1 {
            text-align: center;
            color: #1f3b73;
            margin-bottom: 8px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 28px;
            line-height: 1.7;
        }
        textarea {
            width: 100%;
            height: 210px;
            padding: 14px;
            border: 1px solid #ccc;
            border-radius: 10px;
            font-size: 15px;
            line-height: 1.7;
            resize: vertical;
            box-sizing: border-box;
        }
        button {
            margin-top: 16px;
            width: 100%;
            padding: 13px;
            border: none;
            border-radius: 10px;
            background: #2f6fed;
            color: white;
            font-size: 17px;
            cursor: pointer;
        }
        button:hover {
            background: #1f55c8;
        }
        .example {
            background: #f8fbff;
            border-left: 5px solid #2f6fed;
            padding: 15px 18px;
            border-radius: 8px;
            color: #555;
            line-height: 1.8;
            margin-bottom: 22px;
        }
        .result {
            margin-top: 28px;
            background: #f8fbff;
            border-left: 5px solid #2f6fed;
            padding: 22px;
            border-radius: 10px;
            line-height: 1.8;
            white-space: pre-wrap;
        }
        .arch {
            margin-top: 28px;
            background: #fff8ed;
            border-left: 5px solid #f0a429;
            padding: 20px;
            border-radius: 10px;
            line-height: 1.8;
        }
        .arch h2 {
            color: #8a5a00;
            margin-top: 0;
        }
        .error {
            margin-top: 25px;
            background: #fff1f1;
            border-left: 5px solid #d33;
            padding: 18px;
            border-radius: 8px;
            color: #8a0000;
            line-height: 1.7;
        }
        .footer {
            margin-top: 30px;
            color: #999;
            text-align: center;
            font-size: 13px;
        }
        .small-title {
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>课堂内容智能整理助手</h1>
        <div class="subtitle">
            输入课堂记录、讲义片段或学习材料，系统将调用大模型生成摘要、知识点、复习建议和测试题。
        </div>

        <div class="example">
            <span class="small-title">示例输入：</span><br>
            云计算主要包括 IaaS、PaaS 和 SaaS 三种服务模式。IaaS 提供服务器、存储和网络等基础设施资源；
            PaaS 提供应用开发和部署平台；SaaS 则是用户可以直接使用的软件服务。随着人工智能的发展，
            云服务还出现了 AI IaaS、AI PaaS、MaaS 和 AI SaaS 等新模式。
        </div>

        <form method="post">
            <textarea name="class_text" placeholder="请在这里粘贴课堂内容或学习材料……">{{ class_text }}</textarea>
            <button type="submit">开始智能整理</button>
        </form>

        {% if error %}
        <div class="error">
            {{ error }}
        </div>
        {% endif %}

        {% if result %}
        <div class="result">
{{ result }}
        </div>
        {% endif %}

        <div class="arch">
            <h2>本应用对应的智能化云服务四层架构</h2>
            <div><b>AI IaaS：</b>底层云计算资源为应用运行和模型推理提供算力支撑。</div>
            <div><b>AI PaaS：</b>本项目使用 Render 部署 Flask Web 应用，实现云端运行和公网访问。</div>
            <div><b>MaaS：</b>后端调用阿里云百炼兼容 OpenAI 接口，由通义千问模型完成课堂内容整理。</div>
            <div><b>AI SaaS：</b>用户直接通过网页使用“课堂内容智能整理助手”，获得摘要、知识点和测试题。</div>
        </div>

        <div class="footer">
            云计算课程大作业演示系统 | Flask + Render + 阿里云百炼
        </div>
    </div>
</body>
</html>
"""


def organize_class_content(class_text):
    prompt = f"""
你是一个面向大学生的课堂内容整理助手。请根据用户提供的课堂内容，生成结构化学习材料。

请严格按照以下格式输出：

一、课堂内容摘要
用一段话概括这段课堂内容的主要意思。

二、关键知识点
用 4-6 条列出最重要的知识点，每条尽量简洁。

三、复习建议
给出 3 条适合学生课后复习的建议。

四、自测题
生成 3 道题，包括 2 道简答题和 1 道选择题，并给出参考答案。

五、适合记录到笔记中的总结
用比较自然的学生笔记风格，总结这段内容。

用户提供的课堂内容如下：
{class_text}
"""

    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "你是一个认真、清晰、适合大学生使用的学习助手。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )

    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    class_text = ""

    if request.method == "POST":
        class_text = request.form.get("class_text", "").strip()

        if not class_text:
            error = "请输入课堂内容后再点击整理。"
        elif not os.getenv("DASHSCOPE_API_KEY"):
            error = "没有检测到 DASHSCOPE_API_KEY 环境变量，请先在 Render 中配置阿里云百炼 API Key。"
        else:
            try:
                result = organize_class_content(class_text)
            except Exception as e:
                error = f"调用大模型时出现错误：{str(e)}"

    return render_template_string(
        PAGE_TEMPLATE,
        result=result,
        error=error,
        class_text=class_text
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
