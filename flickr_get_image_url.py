#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
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
        self.image_size    = ["Square",
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
        input_snippet_file = open('snippet.txt')
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

    # 指定したスニペットから指定した画像サイズのURLに置換
    def convert_snippet(self, photo_id):
        for (num_image_size, num_image_snippet) in zip(self.image_size, self.image_snippet):

            if self.snippet.find(num_image_snippet)!=-1:
                image_url = f.get_url_from_photo_id(photo_id, num_image_size)
                if(image_url == None):
                    print "指定したIDの画像は存在しません"
                    exit()
                else:
                    print str(num_image_size) + "の画像を取得中..."
                    self.snippet = self.snippet.replace(num_image_snippet, image_url)
        return self.snippet


if __name__ == '__main__':
    # APIキーを格納したファイルを読み込み
    f = Flickr('./FlickrAPI.conf')
    #IDを打たせる
    print '画像IDを入力'
    Flickr_ID = raw_input('>>>  ')

    # 目的のスニペットをゲット
    f.convert_snippet(Flickr_ID)
    # 結果をクリップボードに格納
    copy_to_clipboard(f.snippet)
    print "クリップボードにコピーしました"