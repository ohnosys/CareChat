# -*- coding: utf-8 -*-

import tornado.ioloop # ノンブロッキングI/Oの導入 / read,write中に処理がブロックされない、他処理も並行して進める
import tornado.web # 多数の同時非同期処理
import tornado.escape # HTMLやJSON、URL等のエスケープ / アンエスケープ
import tornado.options # コマンドライン解析
from tornado.options import define, options # difine : コマンドラインからオプションを追加できるメソッド

import os
import logging

# ログインしていなければリダイレクト機能も追加したい

# Tornadoサーバー / 全体の流れ
    # Handlerをクラスとして作成
    # ApplicationクラスにルーティングとHandlerクラスを紐付け、設定も書き込む
    # サーバー用のオプションをパースしてPortとか設定してサーバースタート


define("port", default=8888, type=int)
define("username", default="user")
define("password", default="pass")


class Application(tornado.web.Application):
    # ルーティングのhandler / アプリケーションのsettingをセット

    def __init__(self):
        handlers = [
            (r'/', MainHandler), # raw文字列でエスケープシーケンスを無効にする、/を 
            (r'/auth/login', AuthLoginHandler),
            (r'/auth/logout', AuthLogoutHandler),
        ]
        settings = dict(
            cookie_secret='gaofjawpoer940r34823842398429afadfi4iias', # secure_cookieの秘密鍵 / get_secure_cookie()を呼び出すときに使う
            static_path=os.path.join(os.path.dirname(__file__), "static"), # jsやcssを入れておくフォルダの設定
            template_path=os.path.join(os.path.dirname(__file__), "templates"), # htmlテンプレのフォルダの設定
            login_url="/auth/login", # ログイン必須のURLにアクセスしたときに、ログインしてなかった場合に飛ばされる場所
            xsrf_cookies=True, # XSRF対策用（なんでTrue） / Tornadoにはxsrf_form_html()というヘルパーみたいなものがあり、formタグ内に書くと自動的にcookieとフォームタグに乱数をセットしてくれる
            autoescape="xhtml_escape", # テンプレエンジンを使うときに自動でエスケープするかどうかの設定 / templete.htmlの中に出力する部分"{{...}}"のところを自動でエスケープする
            debug=True, # Trueにしておくとファイルを更新したときにリロードしてくれたりエラーが起きた時にブラウザ上にエラーを出力してくれる
            )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):

    cookie_username = "username"
    # cookieは悪意のあるクライアントによって簡単に偽装される / 偽装手法とは
    # 現在ログインしているユーザーのユーザIDの保存をCookieに設定したいとき
    # 偽装防止のためにCookieに署名をする必要がある
    # Tornadoはset_secure_cookie メソッドとget_secure_cookieメソッドでこれをすぐ使えるようにサポートしている
    # これらメソッドを使うためにはアプリケーション作成時に cookie_secretという秘密鍵を指定する必要がある
    # 署名されたCookieにはタイムスタンプに加えてHMAC署名のエンコードされた値が含まれる
    # HNAC : メッセージ送受信の際に成りすましでないかや、途中で改竄されていないかを調べることができる認証符号の一つ。ハッシュ関数を元に算出される。not Salt
    #        メッセージ本体と秘密鍵を一定の規則に従って組み合わせハッシュ関数に与え、算出されたハッシュ値を認証符号とする。 
    # Cookieが古い場合や署名が一致しない場合、get_secure_cookieはCookieが設定されていないものとしてNoneを返す
    # https://sites.google.com/site/tornadowebja/documentation/overview

    def get_current_user(self):
        # ログイン機能
        username = self.get_secure_cookie(self.cookie_username) 
        # get_secure_cookie : ステートレスなHTTPの代わりに状態を管理する方法としてクッキーを使う
        # サーバーがクライアント固有情報をクッキーに収めてクライアントに送る
        # クライアントがサーバーにクッキーを送り返すとサーバーはクライアント固有情報からクライアントを一意に識別することができる

        logging.debug('BaseHandler - username: %s' % username)

        if not username:
            return None

#        if not username: return None
#        print('!!!!!!!!!!!!!!')
#        return tornado.escape.utf8(username)

    def set_current_user(self, username):
        self.set_secure_cookie(self.cookie_username, tornado.escape.utf8(username))

    def clear_current_user(self):
        self.clear_cookie(self.cookie_username)


class MainHandler(BaseHandler):

    # 下記デコレータを付けたメソッドはget_currentuser()で何かしら値を返すとパスできて、何も書いてないとlogin_urlへリダイレクトされる仕組み
    # このデコレータのメソッドが要求された場合にユーザーがろぐいんしていなければlogin_url(アプリケーションの設定による)にリダイレクト
    # どういう仕組み？

    @tornado.web.authenticated
    def get(self):
        # 下記はログインしていればユーザーネームを出力して、ログアウトリンクを表示させている
        self.write("Hello, <b>" + self.get_current_user() + "</b> <br> <a href=/auth/logout>Logout</a>")


class AuthLoginHandler(BaseHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        logging.debug("xsrf_cookie:" + self.get_argument("_xsrf", None))

        # cookieにセットされた_xsrfの値とpostで受け取った値をチェックしてダメだったら403エラーを出力してくれるメソッド
        self.check_xsrf_cookie()

        username = self.get_argument("username")
        password = self.get_argument("password")

        # 入力したusernameとpasswordをロガー出力してみる
        logging.debug('AuthLoginHandler:post %s %s' % (username, password))

        # parse_config_file()はあらかじめ設定ファイルにオプションを記述しておくと option.hogehogeのようにアクセスできる
        # options.usernameとoptions.passwordは上記による記述 / 今回はport username password はオリジナル設定
        if username == options.username and password == options.password:
            self.set_current_user(username)
            self.redirect("/")
        else:
            self.write_error(403)


class AuthLogoutHandler(BaseHandler):

    def get(self):
        self.clear_current_user()
        self.redirect('/')


def main():
    # parse_config_file() は設定ファイルにオプションを記述しておくとoption.hogehogeのようにアクセスできるようにするメソッド
    # parse_command_line()はコマンドラインに書いたオプションを適応してくれるメソッド
    # python server.py --port=1111 みたいにコマンドラインに書くとソースの変更なしにパラメータを変更できる

    tornado.options.parse_config_file(os.path.join(os.path.dirname(__file__), 'setting.conf')) # スクリプトと同じディレクトリのファイル(setting.conf)への相対パス
#    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    
#    app.listen(options.port)
    logging.debug('run on port %d in %s mode' % (options.port, options.logging)) # %d = optins.port / %s = options.logging
    tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":
    main()


