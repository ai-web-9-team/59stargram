from flask import Flask, redirect, url_for, render_template, jsonify, request
from pymongo import MongoClient
import gridfs
import base64

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

        # 북마크 정보 불러오기
        bookmarks = list(db.Bookmarks.find({"UserName": user_name}))

        # 포스트 이미지 불러오기
        post_images = []
        fs = gridfs.GridFS(db, 'Post')
        for post in posts:
            data = db.Post.files.find_one({'filename': post['PostId']})
            my_id = data['_id']
            data = fs.get(my_id).read()

            data = base64.b64encode(data)
            data = data.decode()

            post_images.append(data)

        # 북마크 이미지 불러오기
        bookmark_images = []
        bookmark_posts = []
        fs = gridfs.GridFS(db, 'Post')
        for bookmark in bookmarks:
            post_id = bookmark['PostId']

            bookmark_post = db.Posts.find_one({"PostId": post_id})
            data = db.Post.files.find_one({'filename': post_id})

            my_id = data['_id']
            data = fs.get(my_id).read()

            data = base64.b64encode(data)  # convert to base64 as bytes
            data = data.decode()  # convert bytes to string

            bookmark_posts.append(bookmark_post)
            bookmark_images.append(data)

        return render_template("user.html",
                               user_info=user_info,
                               posts=posts, post_images=post_images,
                               bookmark_posts=bookmark_posts, bookmark_images=bookmark_images)

# 유저 페이지 - 팔로우정보 보여주기
@app.route('/user/follow', methods=['GET'])
def user_follow():
    user_name = request.args.get('user_name')

    # type - 0:팔로워 정보 / 1:팔로잉 정보
    follow_type = request.args.get('type')

    # 정보 불러오기
    follows = []
    users = []
    if follow_type == '0':
        follows = list(db.Follows.find({"FollowingName": user_name}, {'_id': False}))
        msg = '팔로워 로딩'
        for follow in follows:
            follower = db.Users.find_one({"UserName": follow['UserName']}, {'_id': False})
            follower_info = {
                'UserName': follower['UserName'],
                'Name': follower['Name'],
            }
            users.append(follower_info)
    elif follow_type == '1':
        follows = list(db.Follows.find({"UserName": user_name}, {'_id': False}))
        msg = '팔로잉 로딩'
        for follow in follows:
            following = db.Users.find_one({"UserName": follow['FollowingName']}, {'_id': False})
            following_info = {
                'UserName': following['UserName'],
                'Name': following['Name'],
            }
            users.append(following_info)
    else:
        msg = '로딩 실패!'

    return jsonify({'msg': msg, 'users': users})



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

