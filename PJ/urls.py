from handlers.auth_handler import LoginHandler, LogoutHandler, SignupHandler
from handlers.index_handler import IndexHandler
from handlers.user_handler import UsersHandler, UserHandler

from tornado.web import url

url_patterns = (
    url(r'/', IndexHandler, name='index'),

    url(r'/auth/login/', LoginHandler, name='login'),
    url(r'/auth/logout/', LogoutHandler, name='logout'),
    url(r'/auth/signup/', SignupHandler, name='signup'),

    url(r'/users/', UsersHandler, name='users'),
    url(r'/users/([0-9]+)/', UserHandler, name='user'),


)
