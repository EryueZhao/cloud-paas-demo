from flask import Flask, request

app = Flask(__name__)

PRODUCTS = {
    "阿里云 ECS": {
        "level": "IaaS",
        "function": "提供云服务器、存储、网络等基础设施资源。",
        "advantages": "配置灵活，中文文档完善，适合国内网站部署和课程实验。",
        "limits": "用户仍然需要自己管理操作系统、运行环境和应用部署。",
        "scenes": "网站部署、教学实验、企业业务系统、数据库服务器。"
    },
    "Amazon EC2": {
        "level": "IaaS",
        "function": "提供弹性云服务器实例，可以根据业务需求选择不同实例类型。",
        "advantages": "全球区域覆盖广，实例类型丰富，适合国际化业务。",
        "limits": "注册、支付和英文文档对部分学生来说有一定门槛。",
        "scenes": "全球网站、大数据处理、机器学习、高性能计算。"
    },
    "Render": {
        "level": "PaaS",
        "function": "通过连接 GitHub 仓库，将 Web 应用部署到云端。",
        "advantages": "部署流程简单，不需要直接管理服务器，适合课程演示和小型项目。",
        "limits": "免费实例性能有限，高级功能需要付费。",
        "scenes": "Web 应用部署、课程项目展示、个人开发测试。"
    },
    "阿里云 SAE": {
        "level": "PaaS",
        "function": "提供 Serverless 应用托管能力，支持应用部署、弹性伸缩和日志监控。",
        "advantages": "减少服务器运维工作，适合应用快速上线。",
        "limits": "需要按照平台规则配置应用，底层自由度不如 IaaS。",
        "scenes": "Web 应用、微服务应用、企业应用托管。"
    },
    "Zapier": {
        "level": "IPaaS",
        "function": "连接不同应用，实现跨平台自动化流程。",
        "advantages": "不需要写复杂接口代码，就能完成应用之间的数据流转。",
        "limits": "复杂流程和高级功能可能需要付费。",
        "scenes": "自动化办公、数据同步、跨系统通知。"
    },
    "简道云": {
        "level": "APaaS",
        "function": "通过零代码或低代码方式搭建表单、流程和管理应用。",
        "advantages": "上手快，适合非专业开发者搭建简单业务系统。",
        "limits": "复杂业务逻辑和高度定制化界面不够灵活。",
        "scenes": "信息收集、审批流程、项目管理、内部业务系统。"
    },
    "Microsoft 365": {
        "level": "SaaS",
        "function": "提供 Word、Excel、PowerPoint、OneDrive、Teams 等在线办公服务。",
        "advantages": "文档处理能力强，跨设备同步和多人协作方便。",
        "limits": "部分功能需要订阅，在线协作依赖网络。",
        "scenes": "论文写作、小组作业、办公协作、文件共享。"
    },
    "钉钉": {
        "level": "SaaS",
        "function": "提供消息沟通、视频会议、在线文档、审批和组织管理等功能。",
        "advantages": "适合组织协同，功能集中，国内用户使用方便。",
        "limits": "功能较多，个人轻量使用时可能显得复杂。",
        "scenes": "班级通知、企业办公、团队协作、线上会议。"
    },
    "阿里云百炼": {
        "level": "MaaS",
        "function": "提供大模型调用和应用开发能力。",
        "advantages": "开发者不用自己训练和部署大模型，就可以调用模型能力。",
        "limits": "模型效果和调用成本受平台限制。",
        "scenes": "智能问答、文本总结、内容生成、知识库应用。"
    },
    "通义听悟": {
        "level": "AI SaaS",
        "function": "提供音视频转写、摘要生成和会议纪要整理等智能功能。",
        "advantages": "普通用户可以直接使用 AI 能力，不需要关心底层模型。",
        "limits": "对平台功能依赖较强，个性化控制有限。",
        "scenes": "课堂录音整理、会议纪要、音视频内容分析。"
    }
}


def analyze_product(name):
    name = name.strip()

    if name in PRODUCTS:
        return PRODUCTS[name]

    for product_name, info in PRODUCTS.items():
        if name.lower() in product_name.lower() or product_name.lower() in name.lower():
            return info

    return {
        "level": "暂未识别",
        "function": "系统中暂时没有该产品的详细信息。",
        "advantages": "可以继续补充产品知识库，让系统支持更多云服务产品。",
        "limits": "当前版本采用简单规则匹配，还没有真正接入大模型 API。",
        "scenes": "适合作为课程演示版本，后续可以接入 MaaS 平台进一步完善。"
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    product_name = ""

    if request.method == "POST":
        product_name = request.form.get("product_name", "")
        result = analyze_product(product_name)

    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>云服务学习助手</title>
        <style>
            body {{
                font-family: Arial, "Microsoft YaHei", sans-serif;
                background: #f4f7fb;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 760px;
                margin: 60px auto;
                background: white;
                padding: 35px;
                border-radius: 16px;
                box-shadow: 0 6px 18px rgba(0,0,0,0.08);
            }}
            h1 {{
                text-align: center;
                color: #1f3b73;
                margin-bottom: 10px;
            }}
            .subtitle {{
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }}
            form {{
                display: flex;
                gap: 10px;
                margin-bottom: 25px;
            }}
            input {{
                flex: 1;
                padding: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 16px;
            }}
            button {{
                padding: 12px 22px;
                border: none;
                background: #2f6fed;
                color: white;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
            }}
            button:hover {{
                background: #1f55c8;
            }}
            .example {{
                color: #777;
                font-size: 14px;
                margin-bottom: 25px;
            }}
            .result {{
                background: #f8fbff;
                border-left: 5px solid #2f6fed;
                padding: 20px;
                border-radius: 8px;
            }}
            .result h2 {{
                margin-top: 0;
                color: #1f3b73;
            }}
            .item {{
                margin: 12px 0;
                line-height: 1.7;
            }}
            .label {{
                font-weight: bold;
                color: #333;
            }}
            .footer {{
                margin-top: 30px;
                text-align: center;
                color: #999;
                font-size: 13px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>云服务学习助手</h1>
            <div class="subtitle">输入云服务产品名称，快速查看它所属的服务层次和主要特点</div>

            <form method="post">
                <input type="text" name="product_name" placeholder="例如：阿里云 ECS、Render、Microsoft 365、阿里云百炼" value="{product_name}">
                <button type="submit">开始分析</button>
            </form>

            <div class="example">
                可测试产品：阿里云 ECS、Amazon EC2、Render、阿里云 SAE、Zapier、简道云、Microsoft 365、钉钉、阿里云百炼、通义听悟
            </div>

            {f'''
            <div class="result">
                <h2>分析结果：{product_name}</h2>
                <div class="item"><span class="label">服务层次：</span>{result["level"]}</div>
                <div class="item"><span class="label">主要功能：</span>{result["function"]}</div>
                <div class="item"><span class="label">优点：</span>{result["advantages"]}</div>
                <div class="item"><span class="label">不足：</span>{result["limits"]}</div>
                <div class="item"><span class="label">适用场景：</span>{result["scenes"]}</div>
            </div>
            ''' if result else ''}

            <div class="footer">
                本系统为云计算课程作业演示版本，主要用于辅助理解 IaaS、PaaS、SaaS、MaaS 等云服务层次。
            </div>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
