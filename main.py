#!/usr/bin/python3

from biplist import *  # https://bitbucket.org/wooster/biplist
import sqlite3
from datetime import datetime  # https://docs.python.org/3/library/datetime.html  , tzinfo
import json
import base64
# import sqlalchemy

# 参考： https://github.com/Mr0x01/WeChatMomentExport-iOS
# 请先通过工具导出 `wc005_008.db` ，放到此文件夹中，并将下方的 `profile_hash` 替换成你自己的 hash字符串 。
profile_hash = "9152d81be8936d74e43704c77ab3c431"


def deal_with_plist_node(node_, objects_):
    # result_ = None
    if type(node_) == dict:
        result_ = {}
        for ky_ in node_:
            result_[ky_] = deal_with_plist_node(node_[ky_], objects_)
            # if 'NS.data' in result_:
            #     print(result_)
        pass
    elif type(node_) == list:
        result_ = []
        for it_ in node_:
            result_.append(deal_with_plist_node(it_, objects_))
        pass
    elif type(node_) == Uid:
        ref_ = objects_[node_.integer]
        result_ = deal_with_plist_node(ref_, objects_)
    elif type(node_) == Data:
        # print(node_)
        result_ = str(base64.urlsafe_b64encode(node_), 'utf-8')
    else:
        result_ = node_
    return result_
# end_def


def deal_with_users(item_):
    result_ = []
    if type(item_) == dict and 'NS.objects' in item_ and item_['NS.objects']:
        for obj_ in item_['NS.objects']:
            if obj_['type'] == 1:
                xx_ = {
                    'type': obj_['type'],
                    'username': obj_['username'],
                    'nickname': obj_['nickname'],
                    'createTime': obj_['createTime'],
                }
            else:
                xx_ = {
                    'type': obj_['type'],
                    'commentID': obj_['commentID'],
                    'content': obj_['content'],
                    'username': obj_['username'],
                    'nickname': obj_['nickname'],
                    'createTime': obj_['createTime'],
                    'bDeleted': obj_['bDeleted'],
                    # 'isAdvertiserComment': obj_['isAdvertiserComment'],
                    # 'isRefAdvertiserComment': obj_['isRefAdvertiserComment'],
                    'refCommentID': obj_['refCommentID'],
                    'refUserName': obj_['refUserName'],

                    # 'commentFlag': obj_['commentFlag'],
                    'snsEmojiInfoObj': obj_['snsEmojiInfoObj'],
                    # 'isLocalAdded': obj_['isLocalAdded'],
                }
            result_.append(xx_)
    return result_
# end_def


def deal_with_url(item_):
    result_ = {'url': ''}
    if type(item_) == dict:
        result_ = {
            'url': item_['url'],
            'type': item_['type'],
            'md5': item_['md5'],
            'videomd5': item_['videomd5'],
            'token': item_['token'],
        }
    return result_['url']
# end_def


def deal_with_media_list(item_):
    result_ = []
    if type(item_) == dict and 'NS.objects' in item_ and item_['NS.objects']:
        for obj_ in item_['NS.objects']:
            xx_ = {
                # 'tid': obj_['tid'],
                # 'mid': obj_['mid'],
                'type': obj_['type'],
                'title': obj_['title'],
                'attachShareTitle': obj_['attachShareTitle'],
                'imgSize': obj_['imgSize'],
                'songLyric': obj_['songLyric'],
                # 'videoDuration': obj_['videoDuration'],
                # 'attachVideoTotalTime': obj_['attachVideoTotalTime'],

                'source': obj_['source'],
                # 'isAd': obj_['isAd'],
                'dataUrl': deal_with_url(obj_['dataUrl']),
                'songAlbumUrl': deal_with_url(obj_['songAlbumUrl']),
                'lowBandUrl': deal_with_url(obj_['lowBandUrl']),
                'attachUrl': deal_with_url(obj_['attachUrl']),
                'attachThumbUrl': deal_with_url(obj_['attachThumbUrl']),
                'gameSnsVideoThumbUrl': deal_with_url(obj_['gameSnsVideoThumbUrl']),
            }
            result_.append(xx_)
            # if xx_['songAlbumUrl'] and xx_['songAlbumUrl'] != '$null':
            #     print(xx_['songAlbumUrl'])
            # if xx_['songLyric'] and xx_['songLyric'] != '$null':
            #     print(xx_['songLyric'])
            # if xx_['lowBandUrl'] and xx_['lowBandUrl'] != '$null':
            #     print(xx_['lowBandUrl'])
            # if xx_['videoDuration'] and xx_['videoDuration'] != 0:
            #     print(xx_['videoDuration'])
            # if xx_['title'] and xx_['title'] == '':
            #     print(xx_['title'])
    return result_
# end_def


def deal_with_content_obj(item_):
    result_ = {}
    if type(item_) == dict:
        result_ = {
            'title': item_['title'],
            'linkUrl': item_['linkUrl'],
            'desc': item_['desc'],
            'type': item_['type'],
            'mediaList': deal_with_media_list(item_['mediaList']),
            # 'md': f"[{item_['title']}]({item_['linkUrl']})",
        }
    return result_
# end_def


def deal_with_location_info(item_):
    result_ = {}
    if type(item_) == dict:
        result_ = {
            'location_latitude': item_['location_latitude'],
            'poiScale': item_['poiScale'],
            'poiInfoUrl': item_['poiInfoUrl'],
            'location_longitude': item_['location_longitude'],
            'showFlag': item_['showFlag'],

            'poiUrl': item_['poiUrl'],
        }
    return result_
# end_def


def deal_with_app_info(item_):
    result_ = {}
    if type(item_) == dict:
        result_ = {
            'appID': item_['appID'],
            'isForceUpdate': item_['isForceUpdate'],
            'clickable': item_['clickable'],

            'installUrl': item_['installUrl'],
            'appName': item_['appName'],
            'fromUrl': item_['fromUrl'],
            'version': item_['version'],
        }
    return result_
# end_def


def deal_with_wcweapp_info(item_):
    result_ = {}
    if type(item_) == dict:
        result_ = {
            'subType': item_['subType'],
            'pagePath': item_['pagePath'],
            'appUserName': item_['appUserName'],
            'version': item_['version'],
            'debugMode': item_['debugMode'],

            'shareActionId': item_['shareActionId'],
            'messageExtraData': item_['messageExtraData'],
        }
    return result_
# end_def


def deal_with_wcmusic_info(item_):
    if '$null' != item_:
        # print(item_)
        pass
    result_ = item_
    return result_
# end_def


def deal_with_time(item_):
    result_ = datetime.fromtimestamp(item_).strftime(f"%Y%m%d-%H:%M:%S-%w")
    # result_ = datetime.utcfromtimestamp(item_).strftime(f"%Y%m%d-%H:%M:%S-%w")
    # print(result_)
    return result_
# end_def


def deal_with_thing(item_):
    result = {
        'tid': item_['tid'],
        'contentDesc': item_['contentDesc'],
        'contentDescScene': item_['contentDescScene'],
        'createtime': item_['createtime'],
        'createtime_string': deal_with_time(item_['createtime']),
        'username': item_['username'],
        'nickname': item_['nickname'],
        'sourceNickName': item_['sourceNickName'],
        'isPrivate': item_['isPrivate'],
        'realLikeCount': item_['realLikeCount'],
        'realCommentCount': item_['realCommentCount'],
        'withCount': item_['withCount'],

        'likeUsers': deal_with_users(item_['likeUsers']),
        'commentUsers': deal_with_users(item_['commentUsers']),
        'withUsers': deal_with_users(item_['withUsers']),
        'contentObj': deal_with_content_obj(item_['contentObj']),
        # 'locationInfo': deal_with_location_info(item_['locationInfo']),
        # 'appInfo': deal_with_app_info(item_['appInfo']),

        # 'wcweappInfo': deal_with_wcweapp_info(item_['wcweappInfo']),

        # 'selfLikeCount': item_['selfLikeCount'],
        # 'selfCommentCount': item_['selfCommentCount'],
        # 'likeCount': item_['likeCount'],
        # 'commentCount': item_['commentCount'],

        'type': item_['type'],
        # 'flag': item_['flag'],
        # 'extFlag': item_['extFlag'],

        'wcmusicInfo': deal_with_wcmusic_info(item_['wcmusicInfo']),
        'shareOpenUrl': item_['shareOpenUrl'],
        # 'recommendInfo': item_['recommendInfo'],
    }
    return result
# end_def


table_name = f"MyWC01_{profile_hash}"

conn = sqlite3.connect('wc005_008.db')
cursor = conn.cursor()
# cursor.execute("select name from sqlite_master where type='table' order by name")
# table_names = cursor.fetchall()
cursor.execute(f"select Buffer,Id from {table_name}")
the_moments = cursor.fetchall()
print(f"共找到{len(the_moments)}条朋友圈。\n")


# print(f"| time_string | contentDesc | sharedLink | sourceNickName |")
# print(f"| --- | --- | --- | --- |")


moments = []
# idx = 0
for moment in the_moments:
    mmt_bp = moment[0]
    mmt_id = moment[1]
    mmt_plist = readPlistFromString(mmt_bp)
    # details = deal_with_plist_node(mmt_plist['$objects'], mmt_plist['$objects'])
    big_thing = deal_with_plist_node(mmt_plist['$objects'][1], mmt_plist['$objects'])
    thing = deal_with_thing(big_thing)
    moments.append(thing)

moments_json = json.dumps(moments, indent=4, ensure_ascii=False)
# print(moments_json)

json_file_name = f"moments_of_{profile_hash}.json"

with open(json_file_name, 'w') as f:
    f.write(moments_json)
