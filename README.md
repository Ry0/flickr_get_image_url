#FlickrのAPIで画像のURLをサイズ毎にゲットするやつ

* FlickrのAPIを使って画像IDからその画像のURLを取ってきます．
* 予め指定した雛形にそってhtmlのスニペットを作成し，クリップボードにコピー．

##前提条件
* requestsがインストールされていること

```bash
pip install requests
```

* FlickrのアカウントとAPIキーを持っていること

> Flickr API  
> [https://www.flickr.com/services/api/](https://www.flickr.com/services/api/)

##準備
FlickrのAPIを手に入れたら，このリポジトリの直下に`FlickrAPI.conf`というファイルを作成し以下の内容で保存．
`abcdefghijklmnopqrstuvwxyz123456`は自分の手に入れたAPIキーをコピペしてください．

```bash
[connect_params]
API_KEY = abcdefghijklmnopqrstuvwxyz123456
```

##スニペットを作成
htmlの雛形を作成します．記述の際，以下のブロックが対応しています．  
このファイルは`snippet.txt`を編集します．

```bash
[Square]
[Large Square]
[Thumbnail]
[Small]
[Small 320]
[Medium]
[Medium 640]
[Medium 800]
[Large]
[Large 1600]
[Large 2048]
[Original]
```

##実行
実行します．

```bash
python flickr_get_image_url.py
```

結果はクリップボードに保存していますので，そのままどこかに貼り付けられます．  
例えば`snippet.txt`を以下のように作成した場合，

```html
<a class="swipebox" href="[Large 1600]" title="">
  <img class="center image-effect" src="[Large]">
</a>
```

実行すると...

```bash
python flickr_get_image_url.py 
画像IDを入力
>>>  19465393524
Largeの画像を取得中...
Large 1600の画像を取得中...
クリップボードにコピーしました
```

```html
<a class="swipebox" href="https://farm1.staticflickr.com/342/19465393524_ff7393bd75_h.jpg" title="">
  <img class="center image-effect" src="https://farm1.staticflickr.com/342/19465393524_545c40623d_b.jpg">
</a>
```

こんな感じになります．  
ブログを書くとき，Flickrにアップロードした画像を載せるのに使えます✌ ('ω' ✌ )三 ✌ ('ω') ✌ 三( ✌ 'ω') ✌

##参考サイト

> Qiita PythonからFlickr APIを使う  
> [http://qiita.com/intermezzo-fr/items/a20a2250411c564b9161](http://qiita.com/intermezzo-fr/items/a20a2250411c564b9161)