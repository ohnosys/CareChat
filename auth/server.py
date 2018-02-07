# -*- coding: utf-8 -*-

import tornado.ioloop # ノンブロッキングI/O 入出力中も他の処理を並行して進める
import tornado.web
import tornado.escape
import tornado.options
from tornado.options import define,options

import os
import logging

define("")
define("")
define("")



class Aplication(tornado.web.Application):
    # tornado.web.Applicationを継承したApplicationクラス
    # ルーティングのhandler / アプリケーションのsettingをセット

    def __init__(self):

        handlers = [
            (r'/', MainHandler), # ルーティングとそのときの処理（Get、Postなど）を書いたクラスを紐付けする / HandlerClass の中身は後で書く
            (r'/auth/login', AuthLoginHandler),
            (r'/auth/logout', AuthLogoutHandler),
            ]

        settings = dict(
            cokkie_secret= 'gaofjawpoer940r34823842398429afadfi4iias', # セキュアクッキーの秘密の合言葉 / get_secret_cokkie()とかを呼び出すときに使う
            static_path= os.path.join(os.path.dirname(__file__), "static"), # js、cssを入れておくフォルダの設定
            template_path= os.path.join(os.path.dirname(__file__), "templates"), # htmlテンプレートのフォルダの設定
            login_url= "/auth/login", #ログイン必須のURLにアクセスしたとき、ログインしてなかったら飛ばされる場所
            xsrf_cookies= True # XSRF対策用 / あとで確認する
            autoescape= "xhtml_escape", # テンプレートエンジンを使うときに自動でエスケープするかどうかの設定 / template.htmlの中に出力する部分"{{...}}"
            debug= True, # ファイルを更新したときにリロードしてくれたりエラーを出力してくれたり
            )

        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    # ログイン機能を付けるためにここにget_current_user()を実装したい
    # tornado.web.RequesrHandler にはget_current_user()が準備されていて、
    # @tornado.web.authenticatedのデコレータを付けたメソッドは、get_current_user()で何かしら値を返すとパスできて、何も書いてないとlogin_urlへリダイレクトされる

    cookie_username= "username"

    def get_current_user(self):
        username = self.get_secure_cookie(self.cookie_username)
        logging.debug('BaseHandler - username: %s' % username)
        if not username: return None
        return tornado.escape.utf8(username)

    def set_current_user(self, username): # 自作メソッド / 利便性を高めてみる
        self.set_secure_cookie(self.cookie_username)

    def clear_current_user(self): # 自作メソッド / 利便性を高めてみる
        self.clear_cookie(self.cookie_username)


class MainHandler(BaseHandler):
    # BaseHandlerを継承
    # Applicationのhandlersで(r'/', MainHandler)と設定しているのでhttp://localhost:5000/にアクセスするとこのクラスで処理される

    @tornado.web.authenticated # このハンドラーでgetされたときにログインしているかチェック / ログインしていなければリダイレクト
    def get(self):
        # ログインしていればusernameを出力してログアウトのリンクが現れる
        self.write("Hello, <b>" + self.get_current_user() + "</b> <br> <a href= /auth/logout> Logout </a>")

class AuthLoginHandler(BaseHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        logging.debug("xsrf_cookie:" + self.get_argument("_xsrf", None))
        
        self.check_xsrf_cookie()

        username = self.get_argument("username")
        password = self.get_argument("password")




    





