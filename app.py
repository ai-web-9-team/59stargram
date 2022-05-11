from flask import Flask, redirect, url_for, render_template, jsonify, request
from pymongo import MongoClient
import gridfs
import base64
import jwt
from datetime import date, timedelta, datetime
from functions import main_page_func
db = main_page_func.db

# client = MongoClient('localhost', 27017)
# db = client.db59stargram

app = Flask(__name__)


# HTML 화면 보여주기
@app.route('/')
def home():
    info = db.Users.find_one({"UserName": "hee123"})
    feed_ids=main_page_func.get_feeds("hee123") # 출력할 피드들의 ID 배열
    feeds_info=[] # 피드의 사용자이름, 이름, 피드 사진, 프로필 사진, 사진 설명, 좋아요 수 저장 배열
    for feed_id in feed_ids:
        feeds_info.append(main_page_func.get_feed_info(feed_id))
    recommend_info=main_page_func.recommend_friends("hee123") # 추천할 계정의 사용자이름, 이름, 프로필 사진 저장 배열
    search_info=[]
    return render_template('index.html', info=info, feeds_info=feeds_info, recommend_info=recommend_info)


@app.route('/upload', methods=['POST'])
def FeedUpReceive():
    token_receive = request.cookies.get('token')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.Users.find_one({"Email": payload['id']})
    picture = request.form['picture']
    description = request.form['description']
    user_id_receive = user_info['_id']
    posts = list(db.Posts.find({}))
    post_id=0
    for post in posts:
        post_id+=1
    doc = {
        'PostId': str(post_id),
        'UserName': user_info["UserName"],
        'Description': description,
        'Date': datetime.now(),
        'LikeCnt': 0,
        'CommentCnt': 0
    }
    db.Posts.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '게시물이 업로드 되었습니다.'})

@app.route('/post-like-create', methods=['POST'])
def post_like_create():
    user_id = request.form['user_id']
    post_id = request.form['post_id']

    like_info = db.PostLikes.find_one({'UserName': user_id, 'PostId': post_id})
    if like_info is None:
        try:
            db.PostLikes.insert_one({"UserName": user_id, "PostId": post_id})
            db.Posts.update_one({"PostId": post_id}, {'$inc': {'LikeCnt': 1}})
            target_id = db.Posts.find_one({"PostId": post_id})["UserName"]
            db.RecentEvents.insert_one({"UserName1": user_id, "EventType": "post_like", "UserName2": target_id})
        except:
            msg = '좋아요 실패'
        return jsonify({'msg': msg})
    else:
        msg = '이미 좋아요를 누른 상태입니다.'
        return jsonify({'msg': msg})



# 유저 페이지 - 유저 정보 보여주기
@app.route('/user')
def user():
    user_name = request.args.get('user_name')
    if user_name is None:
        return redirect(url_for('home'))
    else:
        # 유저 정보 불러오기
        user_info = db.Users.find_one({"UserName": user_name})

        # 유저 프로필 사진 불러오기
        fs = gridfs.GridFS(db, 'Profile')
        profile_img = db.Profile.files.find_one({'filename': user_name})

        my_id = profile_img['_id']
        profile_img = fs.get(my_id).read()

        profile_img = base64.b64encode(profile_img)  # convert to base64 as bytes
        profile_img = profile_img.decode()  # convert bytes to string

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

        # 현재 로그인한 유저인지 판단
        ## 현재 접속한 유저의 사용자 이름
        current_user = 'kimphysicsman'
        if user_name == current_user:
            my_page = 1
        else:
            my_page = 0

        return render_template("user.html",
                               user_info=user_info, profile_img=profile_img,
                               posts=posts, post_images=post_images,
                               bookmark_posts=bookmark_posts, bookmark_images=bookmark_images,
                               my_page=my_page)

# 유저 페이지 - 팔로우정보 보여주기
@app.route('/user/follow', methods=['GET'])
def user_follow():
    user_name = request.args.get('user_name')

    # type - 0:팔로워 정보 / 1:팔로잉 정보
    follow_type = request.args.get('type')

    # 정보 불러오기
    follows = []
    users = []
    fs = gridfs.GridFS(db, 'Profile')
    if follow_type == '0':
        follows = list(db.Follows.find({"FollowingName": user_name}, {'_id': False}))
        msg = '팔로워 로딩'
        for follow in follows:
            follower = db.Users.find_one({"UserName": follow['UserName']}, {'_id': False})

            data = db.Profile.files.find_one({'filename': follower['UserName']})
            my_id = data['_id']
            data = fs.get(my_id).read()

            data = base64.b64encode(data)
            data = data.decode()

            follower_info = {
                'UserName': follower['UserName'],
                'Name': follower['Name'],
                'ProfileImage': data
            }

            users.append(follower_info)
    elif follow_type == '1':
        follows = list(db.Follows.find({"UserName": user_name}, {'_id': False}))
        msg = '팔로잉 로딩'
        for follow in follows:
            following = db.Users.find_one({"UserName": follow['FollowingName']}, {'_id': False})

            data = db.Profile.files.find_one({'filename': following['UserName']})
            my_id = data['_id']
            data = fs.get(my_id).read()

            data = base64.b64encode(data)
            data = data.decode()

            following_info = {
                'UserName': following['UserName'],
                'Name': following['Name'],
                'ProfileImage': data
            }
            users.append(following_info)
    else:
        msg = '로딩 실패!'

    return jsonify({'msg': msg, 'users': users})


# 유저 페이지 - 팔로우 삭제
@app.route('/user/follow/delete', methods=['POST'])
def user_follow_delete():
    user_name = request.form['user_name']
    following_name = request.form['following_name']

    try:
        db.Follows.delete_one({'UserName': user_name, 'FollowingName': following_name})
        msg = '삭제 완료'

        # 로그인한 유저의 팔로잉 숫자 업데이트
        # 현재 유저 정보에서 팔로잉 숫자 가져오기
        following_cnt = 10
        db.Users.update_one({'UserName': user_name}, {'$set': {'FollowingCnt': following_cnt - 1}})

        # 팔로잉 유저의 팔로워 숫자 업데이트
        following_user = db.Users.find_one({'UserName': following_name})
        following_user_follower_cnt = following_user['FollowerCnt']
        db.Users.update_one({'UserName': following_name}, {'$set': {'FollowerCnt': following_user_follower_cnt - 1}})

    except:
        msg = '삭제 실패'

    return jsonify({'msg': msg})


# 유저 페이지 - 팔로우 생성
@app.route('/user/follow/create', methods=['POST'])
def user_follow_create():
    user_name = request.form['user_name']
    following_name = request.form['following_name']

    follow_info = db.Follows.find_one({'UserName': user_name, 'FollowingName': following_name})

    if follow_info is None:
        try:
            db.Follows.insert_one({'UserName': user_name, 'FollowingName': following_name})
            msg = '팔로우 완료'

            # 로그인한 유저의 팔로잉 숫자 업데이트
            # 현재 유저 정보에서 팔로잉 숫자 가져오기
            following_cnt = 10
            db.Users.update_one({'UserName': user_name}, {'$set': {'FollowingCnt': following_cnt + 1}})

            # 팔로잉 유저의 팔로워 숫자 업데이트
            following_user = db.Users.find_one({'UserName': following_name})
            following_user_follower_cnt = following_user['FollowerCnt']
            db.Users.update_one({'UserName': following_name}, {'$set': {'FollowerCnt': following_user_follower_cnt + 1}})

        except:
            msg = '팔로우 실패'

        return jsonify({'msg': msg})
    else:
        msg = '이미 팔로우 한 상태입니다.'
        return jsonify({'msg': msg})


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