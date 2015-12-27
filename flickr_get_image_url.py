#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os.path
import ConfigParser
import xml.dom.minidom as md
from sketch_export import *


class Flickr(object):
    def __init__(self, api_conf):
        self.api_url = 'https://api.flickr.com/services/rest/'
        # FlickrのAPI_KEYを外部ファイルから取ってくる
        self.api_key = self.get_api_param(api_conf)
        # クリップボードに保存するスニペットを取ってくる
        self.snippet = self.get_snippet()
        # スニペットのトリガー
        self.image_snippet = ["[Square]",
                              "[Large Square]",
                              "[Thumbnail]",
                              "[Small]",
                              "[Small 320]",
                              "[Medium]",
                              "[Medium 640]",
                              "[Medium 800]",
                              "[Large]",
                              "[Large 1600]",
                              "[Large 2048]",
                              "[Original]"]
        # Flickrから取ってくるときの画像サイズ指定用
        self.image_size = ["Square",
                           "Large Square",
                           "Thumbnail",
                           "Small",
                           "Small 320",
                           "Medium",
                           "Medium 640",
                           "Medium 800",
                           "Large",
                           "Large 1600",
                           "Large 2048",
                           "Original"]

    # 外部ファイルからAPI_KEYを取ってくる
    def get_api_param(self, api_conf):
        config = ConfigParser.ConfigParser()
        config.read([api_conf])
        api_key = config.get('connect_params', 'API_KEY', 1)
        return api_key

    # 外部ファイルからスニペットを取ってくる
    def get_snippet(self):
        python_script_path = os.path.abspath(os.path.dirname(__file__))
        input_snippet_file = open(python_script_path + "/snippet.txt")
        snippet = input_snippet_file.read()
        input_snippet_file.close()
        return snippet

    # 画像のIDからURLを取ってくる    I
    def get_url_from_photo_id(self, photo_id, image_size):
        # requestの送信
        r = requests.post(self.api_url, {'api_key': self.api_key,
                                         'method': 'flickr.photos.getSizes',
                                         'photo_id': photo_id
                                         })

        # xmlをパースしてdomオブジェクトにする
        dom = md.parseString(r.text.encode('utf-8'))

        # domオブジェクトからURLを探し出す
        result = None
        for elem in dom.getElementsByTagName('size'):
            # 指定された画像サイズのみ取ってくる
            if elem.getAttribute('label') == image_size:
                result = elem.getAttribute('source')
                # オリジナルは1個だと考えて他はスキップ
                break
            else:
                # 何もない場合はNone
                pass
        return result

    # 指定したサイズの画像があるかをチェックしてなかったら指定したサイズよりも小さいサイズでないかを確認する
    # それでもなかったらプログラム終了
    def check_exist_image(self, photo_id, hope_image_size_index):
        flag = False
        for i in reversed(range(0, hope_image_size_index)):
            image_url = self.get_url_from_photo_id(photo_id, self.image_size[i])
            if (image_url != None):
                print self.image_size[hope_image_size_index] + "のサイズは存在しません．" + self.image_size[i] + "サイズを取得します．"
                print image_url + "\n"
                self.snippet = self.snippet.replace(self.image_snippet[hope_image_size_index], image_url)
                flag = True
                break

        if (flag == False):
            print "指定したIDの画像は存在しません"
            exit()

    # 指定したスニペットから指定した画像サイズのURLに置換
    def convert_snippet(self, photo_id):
        # for (num_image_size, num_image_snippet) in zip(self.image_size, self.image_snippet):
        for i in range(0, 11):
            if (self.snippet.find(self.image_snippet[i]) != -1):
                image_url = self.get_url_from_photo_id(photo_id, self.image_size[i])
                if (image_url == None):
                    # 指定したサイズの画像があるかをチェック
                    self.check_exist_image(photo_id, i)
                else:
                    print self.image_size[i] + "の画像を取得中..."
                    print image_url + "\n"
                    self.snippet = self.snippet.replace(self.image_snippet[i], image_url)
        return self.snippet


if __name__ == "__main__":
    # APIキーを格納したファイルを読み込み
    python_script_path = os.path.abspath(os.path.dirname(__file__))
    f = Flickr(python_script_path + "/FlickrAPI.conf")
    #IDを打たせる
    print "画像IDを入力"
    Flickr_ID = raw_input(">>>  ")
    print ""

    # 目的のスニペットをゲット
    f.convert_snippet(Flickr_ID)
    # 結果をクリップボードに格納
    copy_to_clipboard(f.snippet)
    print "クリップボードにコピーしました"
