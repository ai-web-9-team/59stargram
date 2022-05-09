from flask import Flask, redirect, url_for, render_template, jsonify, request
from pymongo import MongoClient
import gridfs

client = MongoClient('localhost', 27017)
db = client.db59stargram

app = Flask(__name__)

# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# 유저 페이지 - 유저 정보 보여주기
@app.route('/user')
def user():
    user_name = request.args.get('user_name')
    if user_name is None:
        return redirect(url_for('home'))
    else:
        # 유저 정보 불러오기
        user_info = db.Users.find_one({"UserName": user_name})

        # 게시글 정보 불러오기
        posts = list(db.Posts.find({"UserName": user_name}))


        # 이미지 불러오기
        images = []
        fs = gridfs.GridFS(db, 'Post')
        for post in posts:
            data = db.Post.files.find_one({'filename': post['PostId']})
            my_id = data['_id']
            outputdata = fs.get(my_id).read()
            print(outputdata.split('\''))

            images.append(outputdata)

        return render_template("user.html", user_info=user_info, posts=posts, images=images)

# 유저 페이지 - 게시글 API
@app.route('/user/posts')
def user_posts():
    msg = '연결 완료'
    return jsonify({"msg": msg})



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