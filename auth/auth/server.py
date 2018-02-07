# -*- coding: utf-8 -*-

import tornado.ioloop # ノンブロッキングI/O 入出力中も他の処理を並行して進める
import tornado.web
import tornado.escape
import tornado.options
from tornado.options import define,options

import os
import logging

# defineはコマンドラインからオプションを追加できるメソッド
define("port", default=8888, type=int)
define("username",default="user")
define("password", default="pass")



class Application(tornado.web.Application):
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
            xsrf_cookies= True, # XSRF対策用 / あとで確認する
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
    # BaseHandlerを継承
    # /auth/login にgetされるとlogin.htmlを出力 / postされるとログイン認証を行う

    def get(self):
        self.render("login.html")

    def post(self):
        # 1. xsrfチェック
        # 2. usernameとpasswordをチェック
        # 3. 合っていたらクッキーにusernameをセット
        # 4. リダイレクト


        logging.debug("xsrf_cookie:" + self.get_argument("_xsrf", None))
        
        self.check_xsrf_cookie() # cookieにセットされたxsrfの値とpostで受け取った値をチェックしてダメだったら403を出力してくれるメソッド

        username = self.get_argument("username")
        password = self.get_argument("password")

        logging.debug('AuthLoginHandler:post %s %s' % (username, password))

        if username == options.username and password == options.password:
            self.set_current_user(username)
            self.redirect("/")
        else:
            self.write_error(403)


class AuthLogoutHandler(BaseHandler):
    # /auth/logoutにアクセスがあったらクッキー内のusernameを削除

    def get(self):
        self.clear_current_user()
        self.redirect('/')



def main():
    # server.conf内の設定の読み込み
    # コマンドラインからオプションの読み込み
    # 作成したApplicationクラスからオブジェクト生成
    # 設定したportでlisten
    # サーバー起動

    tornado.options.parse_config_file(os.path.join(os.path.dirname(__file__), 'server.conf')) # defineで追加したオプションをパース
    tornado.options.parse_command_line() # defineで追加したオプションをパース
    app = Application()
    app.listen(options.port)
    logging.debug('run on port %d in %s mode' % (options.port, options.logging))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()











