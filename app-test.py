from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbinsta

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib


#################################
##  HTML을 주는 부분             ##
#################################
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"Email": payload['id']})
        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']
    name_receive = request.form['name_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    email = db.Users.find_one({"Email": id_receive})
    if email == None:
        pass
    else:
        return jsonify({'result': 'fail', 'msg': '중복된 이메일입니다!'})

    nick = db.Users.find_one({"UserName": nickname_receive})
    if nick == None:
        pass
    else:
        return jsonify({'result': 'fail', 'msg': '중복된 사용자 이름입니다'})

    if not (id_receive and pw_receive and nickname_receive and name_receive):
        return jsonify({'result': 'fail', 'msg': '모두 입력해주세요!'})

    pwd2 = request.form['pwd2']

    if pw_receive != pwd2:
        return jsonify({'msg': '비밀번호가 일치하지 않습니다. 재확인해주세요.'})


    else:
        db.Users.insert_one(
            {'Email': id_receive, 'Password': pw_hash, 'UserName': nickname_receive, 'Name': name_receive})
        return jsonify({'result': 'success', 'msg': '회원가입 되었습니다!'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    if id_receive == "":
        return jsonify({'id_receive': 'success', 'msg': '정보를 입력하세요.'})

    email = db.Users.find_one({"Email": id_receive})

    if email == None:
        return jsonify({'email': 'fail', 'msg': '존재하지 않는 이메일입니다.'})

    pw = db.Users.find_one({"Password": pw_hash})

    if pw == None:
        return jsonify({'email': 'fail', 'msg': '비밀번호가 일치하지 않습니다.'})

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.Users.find_one({'Email': id_receive, 'Password': pw_hash})
    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        payload = {'id': id_receive, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({
            'result': 'success', 'msg': '로그인 성공!',
            # 검증된 경우, access 토큰 반환
            'token': token})

    else:
        return jsonify({'result': 'fail', 'msg': '?'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
