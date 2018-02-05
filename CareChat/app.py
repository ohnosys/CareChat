#!/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function # Python2系でも動くように
import os # パスを扱うため
import json 
import random
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.web import url

# Tornadoサーバー / 全体の流れ
    # Handlerをクラスとして作成（get post ...）
    # AplicationクラスにルーディングとHandlerクラスを紐づけしつつ設定を書き込む
    # サーバー用のオプションをパースしてPortとか設定してサーバースタート！


class IndexHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs): # *はtuple、**はdictionaryとして変数管理
        face_pics = ['cat1.gif', 'cat2.gif', 'cat3.gif'] # ユーザー管理画面で固有アイコン管理ができるようにしたい
        img_name = random.choice(face_pics) # face_picsからいずれか取り出す
        self.render('index.html', img_path=self.static_url('images/' + img_name)) # 相対パスをURLに変換 /static/images/img_name
        # render テンプレファイルと指定引数をテンプレエンジンに渡して、その結果生成された文字列をレスポンスとして送信

class ChatHandler(tornado.websocket.WebSocketHandler):

    # waitersとmessagesに接続している人と送られてきたメッセージを記録
    waiters = set()
    messages = []

    def open(self, *args, **kwargs):
        # 接続してきた人の登録と、その人に対して今までのログを送信
        self.waiters.add(self)
        self.write_message({'messages': self.messages})

    def on_message(self, message):
        # メッセージが送られてきたときに送られてきたメッセージを自分以外の参加者にブロードキャスト / 送られてきたメッセージはログに追加
        message = json.loads(message)
        self.messages.append(message) # messagesにdic型のmessageを追加
        for waiter in self.waiters:
            if waiter == self:
                continue
            waiter.write_message({'img_path': message['img_path'], 'message': message['message']})

    def on_close(self):
        # 接続が切断されたときにwaitersから接続者を削除 / 切断された人にはメッセージをブロードキャストしないようにする
        self.waiters.remove(self)


class Application(tornado.web.Application):

    def __init__(self):
        # 今回は指定していないけど、SSL通信を行うときはオレオレ証明書と秘密鍵の指定が必要なので後で修正
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # スクリプト実行ディレクトリを絶対パスで取得
        tornado.web.Application.__init__(self,
                                         [
                                         url(r'/', IndexHandler, name='index'), # URLの逆引きができるように chat → /chat
                                         url(r'/chat', ChatHandler, name='chat'),
                                         ],
                                         template_path=os.path.join(BASE_DIR, 'templates'), # htmlテンプレのフォルダの設定 
                                         static_path=os.path.join(BASE_DIR, 'static'), # jsやcssなどを入れておくフォルダの設定
                                         )

if __name__ == '__main__':
    # サーバーを立ち上げる処理
    app = Application() 
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

"""
class PythonHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('python.html')

class PHPHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('php.html')

class RubyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('ruby.html')


BASE_DIR = os.path.dirname(__file__)

# url関数を使って引数nameを渡して、URLの逆引きができるようにする python → /python/
application = tornado.web.Application([
    url(r'/', IndexHandler, name='index'),
    url(r'/python/', PythonHandler, name='python'),
    url(r'/php/', PHPHandler, name='php'),
    url(r'/ruby/', RubyHandler, name='ruby'),
    ],
    template_path=os.path.join(BASE_DIR, 'templates'),
    static_path=os.path.join(BASE_DIR, 'static'),
)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
"""




"""
import os
import tornado.ioloop
import tornado.web

# TrnadoのRequestHandlerクラスには役立つ組み込みメソッドたくさんある！
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name', 'World') #クライアントから渡されたパラメータを受け取る / 第一引数に指定した名前がなければ第二引数の値を返す / 第二引数はデフォルト値
        self.render('index.html', name=name) #各引数をテンプレエンジンに渡して、その結果生成された文字列をレスポンスとして送信

BASE_DIR = os.path.dirname(__file__)

#全体設定 / 引数にtemplate_pathとstatic_pathを渡して各々のディレクトリはどこにあるか教えてあげる
application = tornado.web.Application(
        [ (r'/', MainHandler), ],
        template_path = os.path.join(BASE_DIR, 'templates'),
        static_path = os.path.join(BASE_DIR, 'static'),
        )

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
"""
