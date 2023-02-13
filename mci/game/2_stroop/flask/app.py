from flask import Flask, render_template #flask 모듈 import

app = Flask(__name__) # flask name 선언

@app.route("/") #flask 웹 페이지 경로
def hello(): # 경로에서 실행될 기능 선언
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) # host주소와 port number 선언