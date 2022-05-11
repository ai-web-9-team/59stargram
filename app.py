from flask import Flask, redirect, url_for, render_template, jsonify, request
import gridfs
import base64
from datetime import date, timedelta, datetime
from functions import main_page_func
import jwt
import hashlib

# client = MongoClient('localhost', 27017)
# db = client.db59stargram

db = main_page_func.db
app = Flask(__name__)
SECRET_KEY = 'SPARTA'


# HTML 화면 보여주기
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    # try:
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    print(payload)
    user_info = db.Users.find_one({"Email": payload['id']})
    print(user_info)
    return render_template('index.html', info=user_info)
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for('login'))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login"))

    # info = db.Users.find_one({"UserName": "hee123"})
    # feed_ids=main_page_func.get_feeds("hee123") # 출력할 피드들의 ID 배열
    # feeds_info=[] # 피드의 사용자이름, 이름, 피드 사진, 프로필 사진, 사진 설명, 좋아요 수 저장 배열
    # for feed_id in feed_ids:
    #     feeds_info.append(main_page_func.get_feed_info(feed_id))
    # recommend_info=main_page_func.recommend_friends("hee123") # 추천할 계정의 사용자이름, 이름, 프로필 사진 저장 배열
    # search_info=[]
    # return render_template('index.html', info=info, feeds_info=feeds_info, recommend_info=recommend_info)


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
                               current_user=current_user,
                               user_info=user_info, profile_img=profile_img,
                               posts=posts, post_images=post_images,
                               bookmark_posts=bookmark_posts, bookmark_images=bookmark_images,
                               my_page=my_page)


# 유저 페이지 - 유저 정보 보여주기
@app.route('/user/summary', methods=['GET'])
def user_summary():
    user_name = request.args.get('user_name')

    # 유저 정보 불러오기
    user_info = db.Users.find_one({"UserName": user_name})

    new_user_info = {
        'UserName': user_info['UserName'],
        'Name': user_info['Name'],
        'PostCnt': user_info['PostCnt'],
        'FollowerCnt': user_info['FollowerCnt'],
        'FollowingCnt': user_info['FollowingCnt']
    }

    # 유저 프로필 사진 불러오기
    fs = gridfs.GridFS(db, 'Profile')
    profile_img = db.Profile.files.find_one({'filename': user_name})

    my_id = profile_img['_id']
    profile_img = fs.get(my_id).read()

    profile_img = base64.b64encode(profile_img)  # convert to base64 as bytes
    profile_img = profile_img.decode()  # convert bytes to string

    # 게시글 정보 불러오기
    posts = list(db.Posts.find({"UserName": user_name}).limit(3))

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

    return jsonify({'user_info': new_user_info,
                    'profile_img': profile_img,
                    'post_images': post_images})


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

@app.route('/get/user', methods=['GET'])
def get_user_name():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"Email": payload['id']})
        msg = '성공'
    except jwt.ExpiredSignatureError:
        msg = '실패'
    except jwt.exceptions.DecodeError:
        msg = '실패'

    return jsonify({'msg': msg})


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


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
        image = 'static/images/img_profile_default.png'
        image_file = open(image, "rb")
        fs = gridfs.GridFS(db, 'Profile')
        fs.put(image_file, filename=nickname_receive)

        db.Users.insert_one(
            {'Email': id_receive, 'Password': pw_hash, 'UserName': nickname_receive, 'Name': name_receive, 'PostCnt': 0,
             'FollowerCnt': 0, 'FollowingCnt': 0})
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
        payload = {'id': id_receive, 'exp': datetime.utcnow() + timedelta(seconds=600)}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({
            'result': 'success', 'msg': '로그인 성공!',
            # 검증된 경우, access 토큰 반환
            'token': token})



@app.route('/details', methods=['GET'])
def details():
    # 3. post_id받아서 post정보

    # 포스트 아이디를 받음
    post_id = request.args.get('post_id')

    # DB에서 post_id로 post데이터를 가져옴
    post = db.Posts.find_one({'PostId': post_id})

    # 필요한 정보만 골라내기
    date = post['Date'].strftime("%c")

    new_post = {
        'UserName': post['UserName'],
        'post_id': post['PostId'],
        'Description': post['Description'],
        'Date': date,
        'LikeCnt': post['LikeCnt'],
    }

    msg = '게시물 정보 보내주기'
    # 보내주면 끝!
    return jsonify({'msg': msg, 'new_post': new_post})


@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/get/userinfo', methods=['GET'])
def get_user_info():
    token_receive = request.cookies.get('mytoken')
    print(token_receive)
    user_info = {}
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        user_info = db.Users.find_one({"Email": payload['id']})
        print(user_info)
        msg = '성공'
    except jwt.ExpiredSignatureError:
        msg = '실패'
    except jwt.exceptions.DecodeError:
        msg = '실패'

    return jsonify({'msg': msg, 'user_info': user_info})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)