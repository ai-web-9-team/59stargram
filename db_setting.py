

# 건들지 마세요 - 동우


from pymongo import MongoClient
import gridfs
from datetime import date, timedelta, datetime

client = MongoClient('localhost', 27017)
db = client.db59stargram

users = [
    {
        'UserName': 'kimphysicsman',
        'Password': '1234567890',
        'Email': 'kimphysicsman@gmail.com',
        'Name': 'Dongwoo Kim',
        'RecentEvents': [],
        'PostCnt': 4,
        'FollowerCnt': 1,
        'FollowingCnt': 3
    }, {
        'UserName': 'hee123',
        'Password': '1234567890',
        'Email': 'hee123@gmail.com',
        'Name': 'Heejoeng Kim',
        'RecentEvents': [],
        'PostCnt': 0,
        'FollowerCnt': 1,
        'FollowingCnt': 1
    }, {
        'UserName': 'joen123',
        'Password': '1234567890',
        'Email': 'Joen123@gmail.com',
        'Name': 'Jinyoung Joen',
        'PostCnt': 0,
        'FollowerCnt': 0,
        'FollowingCnt': 0
    }, {
        'UserName': 'song123',
        'Password': '1234567890',
        'Email': 'song123@gmail.com',
        'Name': 'Songhee Won',
        'RecentEvents': [],
        'PostCnt': 0,
        'FollowerCnt': 1,
        'FollowingCnt': 0,
    }
]

images = [
    'static/images/img_profile.jpg',
    'static/images/img_dongwoo_post_1.jpg',
    'static/images/img_dongwoo_post_2.jpg',
    'static/images/img_songhee_profile.png'
]

follows = [
    {
        'UserName': 'kimphysicsman',
        'FollowingName': 'hee123'
    },
{
        'UserName': 'kimphysicsman',
        'FollowingName': 'song123'
    },
{
        'UserName': 'kimphysicsman',
        'FollowingName': 'joen123'
    },
{
        'UserName': 'hee123',
        'FollowingName': 'kimphysicsman'
    }
]

posts = [
    {
        'PostId': '0',
        'UserName': 'kimphysicsman',
        'Description': '하위1',
        'Date': datetime.now(),
        'LikeCnt': 11,
        'CommentCnt': 1
    },     {
        'PostId': '1',
        'UserName': 'kimphysicsman',
        'Description': '하위2',
        'Date': datetime.now(),
        'LikeCnt': 22,
        'CommentCnt': 2
    },    {
        'PostId': '2',
        'UserName': 'kimphysicsman',
        'Description': '하위3',
        'Date': datetime.now(),
        'LikeCnt': 33,
        'CommentCnt': 3
    }, {
     'PostId': '3',
     'UserName': 'kimphysicsman',
     'Description': '하위4',
     'Date': datetime.now(),
     'LikeCnt': 44,
     'CommentCnt': 4
     }
]

post_images = [
    'static/images/img_dongwoo_post_1.jpg',
    'static/images/img_dongwoo_post_2.jpg',
    'static/images/img_dongwoo_post_3.jpg',
    'static/images/img_dongwoo_post_1.jpg',
    'static/images/img_post.jpg'
]

bookmarks = [
    {
        'UserName': 'kimphysicsman',
        'PostId': '1'
    }, {
        'UserName': 'kimphysicsman',
        'PostId': '3'
    }
]

comments = [
    {
        'CommentId': '0',
        'Desription': '멋잇다',
        'PostId': '0',
        'UserName': 'hee123',
        'Data': datetime.now(),
        'LikeCnt': 0
    },     {
        'CommentId': '1',
        'Desription': '멋잇다123',
        'PostId': '0',
        'UserName': 'hee123',
        'Data': datetime.now(),
        'LikeCnt': 0
    },     {
        'CommentId': '2',
        'Desription': '멋잇다33333',
        'PostId': '0',
        'UserName': 'hee123',
        'Data': datetime.now(),
        'LikeCnt': 0
    }
]

def make_follow():
    global follows
    for follow in follows:
        db.Follows.insert_one(follow)

def make_user():
    global users
    for user in users:
        db.Users.insert_one(user)

def make_post():
    global posts
    for post in posts:
        db.Posts.insert_one(post)

def make_bookmark():
    global bookmarks
    for bookmark in bookmarks:
        db.Bookmarks.insert_one(bookmark)

def make_comment():
    global comments
    for comment in comments:
       db.Comments.insert_one(comment)

def insert_image(images, namespace):
    global posts
    for i in range(len(images)):
        ## GridFs를 통해 파일을 분할하여 DB에 저장하게 된다
        image = images[i]
        image_file = open(image, "rb")

        post = posts[i]

        print(image_file)

        fs = gridfs.GridFS(db, namespace)
        fs.put(image_file, filename=post['PostId'])

make_user()
make_post()
make_bookmark()
make_follow()
make_comment()
insert_image(images, 'Profile')
insert_image(post_images, 'Post')