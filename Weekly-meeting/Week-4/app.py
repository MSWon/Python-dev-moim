from flask import Flask
# 클래스의 인스턴스를 만듭니다. 
# 첫 번째 인수는 응용 프로그램 모듈 또는 패키지의 이름입니다.
app = Flask(__name__)

# route()데코레이터를 사용하여 Flask에게 어떤 URL이 함수를 트리거해야하는지 알려줍니다.
# 함수에는 특정 함수에 대한 URL을 생성하는 데 사용되는 이름이 제공되며 사용자 브라우저에 표시하려는 메시지를 반환합니다.

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

app.run(host='0.0.0.0', port=6006, debug=True)
