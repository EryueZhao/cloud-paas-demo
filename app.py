from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <html>
    <head>
        <title>Cloud PaaS Demo</title>
    </head>
    <body>
        <h1>Hello Cloud PaaS!</h1>
        <p>This is a simple web application deployed on Render.</p>
        <p>It shows how PaaS helps users deploy applications without managing servers directly.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
