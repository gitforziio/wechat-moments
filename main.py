#!/usr/bin/python3

from biplist import *  # https://bitbucket.org/wooster/biplist
import sqlite3
import time
# import datetime  # https://docs.python.org/3/library/datetime.html
# import json
# import sqlalchemy

# profile_hash = "你的hash字符串"
profile_hash = "9152d81be8936d74e43704c77ab3c431"
table_name = f"MyWC01_{profile_hash}"

conn = sqlite3.connect('wc005_008.db')
cursor = conn.cursor()
# cursor.execute("select name from sqlite_master where type='table' order by name")
# table_names = cursor.fetchall()
cursor.execute(f"select Buffer,Id from {table_name}")
the_moments = cursor.fetchall()
print(f"共找到{len(the_moments)}条朋友圈。\n")


def deal_with_plist_node(node_, objects_):
    result_ = None
    if type(node_) == dict:
        result_ = {}
        for ky_ in node_:
            result_[ky_] = deal_with_plist_node(node_[ky_], objects_)
        pass
    elif type(node_) == list:
        result_ = []
        for it_ in node_:
            result_.append(deal_with_plist_node(it_, objects_))
        pass
    elif type(node_) == Uid:
        ref_ = objects_[node_.integer]
        result_ = deal_with_plist_node(ref_, objects_)
    else:
        result_ = node_
    return result_
# end_def


def deal_with_shared_link(item_):
    result = {
        'title': item_['title'],
        'linkUrl': item_['linkUrl'],
        'md': f"[{item_['title']}]({item_['linkUrl']})",
        'desc': item_['desc'],
        'type': item_['type'],
        'subType': item_['subType'],
        'createtime': item_['createtime'],
    }
    return result
# end_def


def deal_with_like_or_comment(item_):
    result = {
        'username': item_['username'],
        'commentID': item_['commentID'],
        'bDeleted': item_['bDeleted'],
        'nickname': item_['nickname'],
        'isRefAdvertiserComment': item_['isRefAdvertiserComment'],
        'refCommentID': item_['refCommentID'],
        'isAdvertiserComment': item_['isAdvertiserComment'],
        'type': item_['type'],
        'commentFlag': item_['commentFlag'],
        'snsEmojiInfoObj': item_['snsEmojiInfoObj'],
        'isLocalAdded': item_['isLocalAdded'],
        'createTime': item_['createTime'],
        'content': item_['content'],
        'refUserName': item_['refUserName'],
    }
    return result
# end_def


print(f"| time_string | contentDesc | sharedLink | sourceNickName |")
print(f"| --- | --- | --- | --- |")

moments = []
# idx = 0
for moment in the_moments:
    mmt_bp = moment[0]
    mmt_id = moment[1]
    mmt_plist = readPlistFromString(mmt_bp)
    timestamp = mmt_plist['$objects'][1]['createtime']
    time_string = time.strftime(f"%Y%m%d-%H:%M:%S-%w-%Z[{time.altzone}]", time.gmtime(timestamp))
    mmt = {
        'id': mmt_id,
        'meta': {
            # 'id': mmt_plist['$objects'][2],
            'createTimeString': time_string,
            'createTime': timestamp,
            'descScene': mmt_plist['$objects'][1]['contentDescScene'],
            'likeCount': mmt_plist['$objects'][1]['realLikeCount'],
            'commentCount': mmt_plist['$objects'][1]['realCommentCount'],
            'userId': mmt_plist['$objects'][3],
            'userName': mmt_plist['$objects'][4],
            'isPrivate': mmt_plist['$objects'][1]['isPrivate'],
        },
        # 'detail': deal_with_plist_node(mmt_plist['$objects'], mmt_plist['$objects']),
    }
    details = deal_with_plist_node(mmt_plist['$objects'], mmt_plist['$objects'])

    mmt['likes'] = []
    mmt['comments'] = []
    mmt['contentDesc'] = None
    mmt['sourceNickName'] = None
    mmt['sharedLink'] = {}

    for item in details:
        # if type(item) == str:
        #     if item == '神经现实':
        #         print(details)
        if type(item) == dict and 'bDeleted' in item:
            if item['type'] == 1:
                mmt['likes'].append(deal_with_like_or_comment(item))
            elif item['type'] == 2:
                mmt['comments'].append(deal_with_like_or_comment(item))
        elif type(item) == dict:
            contentDesc = ''
            sharedLink = ''
            sourceNickName = ''
            if 'contentDesc' in item and item['contentDesc']:
                mmt['contentDesc'] = item['contentDesc']
                contentDesc = mmt['contentDesc'].replace('|', '\\|').replace('\n', '<br/>')
            if 'sourceNickName' in item and item['sourceNickName']:
                mmt['sourceNickName'] = item['sourceNickName']
                sourceNickName = mmt['sourceNickName']
            if 'contentObj' in item and item['contentObj'] \
                    and 'type' in item['contentObj'] and item['contentObj']['type'] == 3:
                mmt['sharedLink'] = (deal_with_shared_link(item['contentObj']))
                sharedLink = mmt['sharedLink']['md'].replace('|', '\\|')
                print(f"| {time_string} | {contentDesc} | {sharedLink} | {sourceNickName} |")
