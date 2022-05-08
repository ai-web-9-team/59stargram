

# 건들지 마세요 - 동우


from pymongo import MongoClient
import gridfs
client = MongoClient('localhost', 27017)
db = client.db59stargram

users = [
    {
        'UserName': 'kimphysicsman',
        'Password': '1234567890',
        'Email': 'kimphysicsman@gmail.com',
        'Name': 'Dongwoo Kim',
        'RecentEvents': [],
        'PostCnt': 0,
        'FollowerCnt': 0,
        'FollowingCnt': 0
    }, {
        'UserName': 'hee123',
        'Password': '1234567890',
        'Email': 'hee123@gmail.com',
        'Name': 'Heejoeng Kim',
        'RecentEvents': [],
        'PostCnt': 0,
        'FollowerCnt': 0,
        'FollowingCnt': 0
    }, {
        'UserName': 'Joen123',
        'Password': '1234567890',
        'Email': 'Joen123@gmail.com',
        'Name': 'Jinyoung Joen',
        'RecentEvents': [],
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
        'FollowerCnt': 0,
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

def make_follow():
    global follows
    for follow in follows:
        db.Follows.insert_one(follow)


def make_user():
    global users
    for user in users:
        db.Users.insert_one(user)

def insert_image():
    global images, users
    for i in range(len(images)):
        ## GridFs를 통해 파일을 분할하여 DB에 저장하게 된다
        image = images[i]
        image_file = open(image, "rb")

        print(image_file)

        user = users[i]

        fs = gridfs.GridFS(db, 'Profile')
        fs.put(image_file, filename=user['UserName'])

def road_image():
    global users
    for user in users:
        name = user['UserName']
        print(name)
        fs = gridfs.GridFS(db)
        data = db.fs.files.find_one({'filename': name})

        my_id = data['_id']
        outputdata = fs.get(my_id).read()
        output = open('./static/images/' + name + '.jpg', 'wb')
        output.write(outputdata)

make_follow()