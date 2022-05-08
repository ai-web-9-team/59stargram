from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.db59stargram

app = Flask(__name__)

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# 유저 페이지 보여주기
@app.route('/user')
def user():
    user_name = request.args.get('user_name')
    user_info = db.Users.find_one({"UserName": user_name})

    print(user_info)

    return render_template("user.html", user_info=user_info)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/detail')
def detail():
    return render_template('detail.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)