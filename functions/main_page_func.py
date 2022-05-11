#import db_setting
import certifi
from pymongo import MongoClient
import gridfs
import base64
import random
from flask import Flask, redirect, url_for, render_template, jsonify, request

client = MongoClient('mongodb+srv://test:sparta@cluster0.1idhr.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=certifi.where())
db = client.ogustagram

# 현재 user_id 계정으로 접속중인 상태에서 띄울 수 있는 피드의 Post ID를 리턴하는 함수
def get_feeds(user_id):
    ret = []
    posts = list(db.Posts.find({}))
    follows = list(db.Follows.find({}))
    for post in posts:
        if post["UserName"]==user_id: # 내 자신의 피드는 띄운다
            ret.append(post["PostId"])
        for follow in follows: # 로그인 중인 계정이 팔로우 중인 계정의 피드는 띄운다
            if follow["UserName"]==user_id and follow["FollowingName"]==post["UserName"]:
                ret.append(post["PostId"])
    #날짜 순으로 정렬해서 10개만 출력하자!
    #ret.sort(key=lambda x:x["Date"])
    return ret[:10]


# 내가 좋아요를 눌렀던 피드인지 확인
def did_i_like(user_id, post_id):
    result = db.PostLikes.find_one({"UserName": user_id, "PostId": post_id})
    if result is None:
        return False
    return True


# 피드 내 정보를 리턴하는 함수
def get_feed_info(post_id):
    current_post = db.Posts.find_one({"PostId": post_id})
    # 사용자 이름
    user_name = current_post["UserName"]

    # 진짜 이름
    name = db.Users.find_one({"UserName": user_name})["Name"]

    # 피드 사진
    fs = gridfs.GridFS(db, 'Post')
    data = db.Post.files.find_one({'filename': post_id})
    my_id = data['_id']
    data = fs.get(my_id).read()
    data = base64.b64encode(data)
    data = data.decode()

    # 프로필 사진
    fs2 = gridfs.GridFS(db, 'Profile')
    data2 = db.Profile.files.find_one({'filename': user_name})
    my_id2 = data2['_id']
    data2 = fs2.get(my_id2).read()
    data2 = base64.b64encode(data2)
    data2 = data2.decode()

    # 사진 설명
    description = current_post["Description"]

    # 좋아요 수
    like_cnt = current_post["LikeCnt"]

    # 댓글 수
    comment_cnt = current_post["CommentCnt"]

    # 내가 좋아요를 눌렀는지 확인 (피드에 '나 외에' 문구 출력 여부를 위함)
    my_like = did_i_like(user_name, post_id)

    return [user_name, name, data, data2, description, like_cnt, comment_cnt, my_like, post_id]





# 팔로우 중이 아닌 사람 랜덤으로 5명(혹은 이하)을 추출해서 User의 사용자이름, 이름, 프로필 사진을 추출하는 함수
# 친구 추천 창을 띄우기 위한 부분
# 근데 이제 팔로우 되어있는지 아닌지를 확인해줘야 함
def recommend_friends(user_id):
    users=list(db.Users.find({}))
    follows = list(db.Follows.find({"UserName": user_id}))
    random.shuffle(users)
    ret = []
    cnt = 0
    # 나이거나 이미 팔로우 중인 계정이면 pass
    # 아니면 recommend_user_name에 UserName 정보를 추가하고 cnt 1 증가
    for user in users:
        if cnt == 5:
            return ret
        if user["UserName"]==user_id: # 나 자신인 경우에는 제외한다
            continue
        continue_flag=False
        for follow in follows:  # 로그인 중인 계정이 이미 팔로우 중인 계정은 제외한다
            if follow["UserName"] == user_id and follow["FollowingName"] == user["UserName"]:
                continue_flag=True
                break # for문 탈출용
        if continue_flag:
            continue
        fs = gridfs.GridFS(db, 'Profile')
        data = db.Profile.files.find_one({'filename': user["UserName"]})
        if data is None:
            continue
        my_id = data['_id']
        data = fs.get(my_id).read()
        data = base64.b64encode(data)
        data = data.decode()
        ret.append([user["UserName"], user["Name"], data])
        cnt += 1
    return ret[:5]

# print(recommend_friends("kimphysicsman3"))
# 검색 결과창을 결정하기 위한 함수
# 매개변수로 들어온 user_id가 Users에 있는지 확인
def is_exist_user(user_id):
    collection = db.Users
    result = collection.find_one({"UserName": user_id})
    if result is None:
        return False
    return True


# 검색창에 입력한 값과 가장 유사한 사용자 이름을 가진 계정 5개를 알아내는 함수
# 매개변수로 들어온 search_input이 검색창에 써져 있는 문자열
def during_searching(search_input):
    collection = db.Users
    ret = []  # return할 배열
    users = collection.find({})
    for user in users:  # 전체 다 돌아본다
        if user["UserName"].startswith(search_input):  # 검색어가 포함된 사용자 이름이면
            ret.append([user["UserName"], user["Name"]])  # ret 배열에 추가
    ret.sort()
    return ret[:5]  # 알파벳 순으로 정렬했을 때 앞의 5개(혹은 이하)만 return


# 새로운 알림이 있는지 확인하기 위한 함수
# 매개변수로 들어온 user_id 계정에 대한 알림이 있는지 확인
def any_new_alert(user_id):
    collection = db.RecentEvents
    result = collection.find_one({"UserName2": user_id})
    if result is None:
        return False
    return True


# 알림 내용을 가져오는 함수
# 좀 더 고민해봐야 함
def get_alerts(user_id):
    collection = db.RecentEvents
    ret = []
    alerts = collection.find({"UserName2": user_id})
    for alert in alerts:
        if len(ret) == 5:
            return ret
        ret.append(alert["UserName1"] + "님이 " + alert["EventType"])
    for i in range(5 - len(ret)):
        ret.append("")
    return ret


# 팔로우하는 함수
def follow(user_id, target_id):
    collection = db.Follows
    collection.insert_one({"UserName": user_id, "FollowingName": target_id})
    #recent event 수정하기
    #collection = db.RecentEvents
    #collection.insert_one({"UserName1": user_id, "EventType": "follow", "UserName2": target_id})


# 팔로우 취소하는 함수
def unfollow(user_id, target_id):
    collection = db.Follows
    collection.delete_one({"UserName": user_id, "FollowingName": target_id})
    # recent event 수정하기
    # collection = db.RecentEvents
    # collection.delete_one({"UserName1": user_id, "EventType": "follow", "UserName2": target_id})




# 게시글 좋아요를 취소하는 함수
def cancel_post_like(user_id, post_id):
    collection = db.PostLikes
    collection.delete_one({"UserName": user_id, "PostID": post_id})
    # recent event 수정하기
    # collection = db.RecentEvents
    # collection.delete_one({"UserName1": user_id, "EventType": "post_like", "UserName2": target_id})


# 2명의 좋아요 대표자를 추출해내는 함수
# def get_representative(post_id):
#     collection = db.PostLikes
#     ret=[]
#     representatives = collection.find({"PostID": post_id})


# 댓글 좋아요를 누르는 함수
def click_comment_like(user_id, comment_id):
    collection = db.CommentsLikes
    collection.insert_one({"UserName": user_id, "CommentID": comment_id})
    # recent event 수정하기
    # collection = db.RecentEvents
    # collection.insert_one({"UserName1": user_id, "EventType": "comment_like", "UserName2": target_id})


# 댓글 좋아요를 취소하는 함수
def cancel_comment_like(user_id, comment_id):
    collection = db.CommentsLikes
    collection.delete_one({"UserName": user_id, "CommentID": comment_id})
    # recent event 수정하기
    # collection = db.RecentEvents
    # collection.insert_one({"UserName1": user_id, "EventType": "comment_like", "UserName2": target_id})


# 게시글 북마크를 하는 함수
def click_bookmark(user_id, post_id):
    collection = db.Bookmarks
    collection.insert_one({"UserName": user_id, "PostID": post_id})


# 게시글 북마크를 취소하는 함수
def cancel_bookmark(user_id, post_id):
    collection = db.Bookmarks
    collection.delete_one({"UserName": user_id, "PostID": post_id})